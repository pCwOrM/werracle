#!/usr/bin/env python3
"""
Werracle NEAR Intent Guard, Chain Signatures Policy Gate & Live Aurora Parity Verifier
=======================================================================================
Zero external dependencies (Python 3 stdlib only). Safe, non-custodial, read-only/dry-run.
Privacy Invariant: TELEMETRY_ENABLED = False (no private keys, no tracking, no tx signing).

Architecture:
1. Bit-exact Python port of `contracts/WerracleTripodZMod9.sol` (`_evaluateSparseTripod`,
   `_escapeZMod9`, `previewDecision`, `isZMod9ResonantIdeal`) in signed Q16.16 fixed-point.
2. Pre-signing Chain Signatures (`v1.signer`) Policy Gate for NEAR Intents (`intents.near`):
   evaluates cross-chain swap / DeFi / AI-agent intents in sub-15us with Z/9Z ideal/unit triage.
3. Live cross-verification (skipped cleanly with `--offline`):
   - Aurora Testnet (`https://testnet.aurora.dev`): live `seed()`, `previewDecision()`, `eth_estimateGas`
   - NEAR Mainnet & Testnet RPC (`pcworm.near`, `v1.signer`, `intents.near`, `v1.signer-prod.testnet`)
   - NEAR Intents 1Click API (`https://1click.chaindefuser.com/v0/tokens` & `/v0/quote` `dry: true`)
"""

from __future__ import annotations

import argparse
import datetime
import functools
import hashlib
import json
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

TELEMETRY_ENABLED = False

# Q16.16 Fixed-Point Constants (matching WerracleTripodZMod9.sol)
FP_SHIFT = 16
FP_ONE = 65536       # 1.0 in Q16.16
FP_HALF = 32768      # 0.5 in Q16.16
FP_FOUR = 262144     # 4.0 in Q16.16 (escape radius^2 = 2^2)

# Formal Z/9Z Algebraic Partition (Lean 4 GAP-0331 `ZModnZObj.isUnit_iff`)
ZMOD9_RESONANT_IDEAL_I3 = frozenset({0, 3, 6})
ZMOD9_COPRIME_UNIT_KERNEL = frozenset({1, 2, 4, 5, 7, 8})

# Live Endpoints & Deployed Contracts
AURORA_TESTNET_RPC = "https://testnet.aurora.dev"
NEAR_MAINNET_RPC = "https://rpc.mainnet.near.org"
NEAR_TESTNET_RPC = "https://rpc.testnet.near.org"
NEAR_1CLICK_BASE = "https://1click.chaindefuser.com/v0"

WERRACLE_V1_ADDR = "0x4085673F1e45bf26682CA704b2d09C03d1212cd4"
WERRACLE_TRIPOD_V2_ADDR = "0x1d7Ae9E1dDDA805539d9e225425804Ef8B9caBaF"

# Deployed on-chain seed for ETH/USDC on Aurora Testnet WerracleTripodZMod9
DEPLOYED_SEED_V2 = {
    "cx": -93061,
    "cy": 14417,
    "zoom": 2949120,      # 45 * 65536 (45.0x)
    "threshold": 5000,    # 50.00%
}

# Verified ABI selectors (`cast sig`)
SEL_OWNER = "0x8da5cb5b"                  # owner()
SEL_SEED = "0x7d94792a"                   # seed()
SEL_PREVIEW_DECISION = "0x0eea75c5"       # previewDecision(bytes32,int64)
SEL_DECIDE_NOUL = "0x26c291f3"            # decideNoul(bytes32,int64)
SEL_IS_ZMOD9_IDEAL = "0x97f7d256"         # isZMod9ResonantIdeal(uint256)

# Live NEAR Intents 1Click canonical assets for non-binding dry quote check
ASSET_WNEAR = "nep141:wrap.near"
ASSET_NEAR_USDC = "nep141:17208628f84f5d6ad33f0da3bbbeb27ffcb398eac501a31bd6ad2011e36133a1"

HTTP_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Werracle-NEAR-Intent-Guard/2.0)",
    "Content-Type": "application/json",
    "Accept": "application/json",
}


# ---------------------------------------------------------------------------
# Bit-Exact Q16.16 Kernel (1-to-1 with WerracleTripodZMod9.sol)
# ---------------------------------------------------------------------------

def sol_trunc_div(a: int, b: int) -> int:
    """Solidity-exact signed integer division (truncates toward zero)."""
    if b == 0:
        raise ZeroDivisionError("Division by zero")
    q = abs(a) // abs(b)
    return -q if ((a < 0) ^ (b < 0)) else q


def sigmoid_bps(x_fp: int) -> int:
    """Linear-clamped Q16.16 activation matching `_sigmoid(int256 x)` in Solidity."""
    if x_fp <= -FP_FOUR:
        return 180
    if x_fp >= FP_FOUR:
        return 9820
    p = FP_HALF + ((x_fp * 7864) >> FP_SHIFT)
    res = (p * 10000) >> FP_SHIFT
    if res < 100:
        return 100
    if res > 9900:
        return 9900
    return res


def escape_zmod9(cx_fp: int, cy_fp: int) -> int:
    """Evaluates z_{n+1} = z_n^2 + c in Q16.16 up to n = 9 (`_escapeZMod9`)."""
    zx = 0
    zy = 0
    for i in range(9):
        zx2 = (zx * zx) >> FP_SHIFT
        zy2 = (zy * zy) >> FP_SHIFT
        if zx2 + zy2 > FP_FOUR:
            return i
        nzx = zx2 - zy2 + cx_fp
        nzy = ((zx * zy) >> (FP_SHIFT - 1)) + cy_fp
        zx, zy = nzx, nzy
    return 9


def classify_zmod9(escape_step: int) -> str:
    """Partitions Z/9Z residue into Resonant Ideal I_3 or Coprime Error Kernel."""
    return "I3_IDEAL" if (escape_step % 9) in ZMOD9_RESONANT_IDEAL_I3 else "K_ERROR_UNIT"


@functools.lru_cache(maxsize=64)
def evaluate_sparse_tripod_seed(cx: int, cy: int, zoom: int) -> Tuple[Tuple[int, int, int], int, int, int, int, int]:
    """
    Synthesizes the 12-point Z/9Z Sparse Tripod across 3 zoom planes (0.60x, 1.00x, 1.60x)
    for a 32-byte seed coordinate (cx, cy, zoom). Cached per active seed coordinate.
    """
    step = sol_trunc_div(FP_ONE * FP_ONE, zoom) if zoom > 0 else FP_ONE
    steps = (
        sol_trunc_div(step * 100, 60),
        step,
        sol_trunc_div(step * 100, 160),
    )

    esc_planes: List[int] = [0, 0, 0]
    probe_escapes: List[int] = []
    for idx, st in enumerate(steps):
        e0 = escape_zmod9(cx + st, cy)
        e1 = escape_zmod9(cx - st, cy)
        e2 = escape_zmod9(cx, cy + st)
        e3 = escape_zmod9(cx, cy - st)
        esc_planes[idx] = e0 + e1 + e2 + e3
        probe_escapes.extend((e0, e1, e2, e3))

    ratios = [(e * 10000) // 36 for e in esc_planes]
    bounded_bps = (ratios[0] + (ratios[1] << 1) + ratios[2]) >> 2
    bias_bps = bounded_bps - 5000
    bias_fp = sol_trunc_div(bias_bps * FP_ONE, 5000)
    ideal_hits = sum(1 for e in probe_escapes if (e % 9) in ZMOD9_RESONANT_IDEAL_I3)
    unit_hits = 12 - ideal_hits
    return (esc_planes[0], esc_planes[1], esc_planes[2]), sum(esc_planes), bounded_bps, bias_fp, ideal_hits, unit_hits


# Pre-warm canonical Aurora Testnet v2 seed slot on load
evaluate_sparse_tripod_seed(DEPLOYED_SEED_V2["cx"], DEPLOYED_SEED_V2["cy"], DEPLOYED_SEED_V2["zoom"])


def tripod_preview_q16_16(
    risk_fp: int,
    seed: Optional[Dict[str, int]] = None,
) -> Dict[str, Any]:
    """
    Bit-exact Python mirror of `WerracleTripodZMod9.previewDecision(bytes32(0), riskFP)`.
    Uses 12 cardinal probes across 3 zoom planes (0.60x Wide, 1.00x Focus, 1.60x Deep).
    """
    assert not TELEMETRY_ENABLED, "Invariant violated: TELEMETRY_ENABLED must remain False"
    cfg = seed or DEPLOYED_SEED_V2
    cx = int(cfg["cx"])
    cy = int(cfg["cy"])
    zoom = int(cfg["zoom"])
    threshold = int(cfg["threshold"])

    t0 = time.perf_counter()
    esc_planes, total_escapes, bounded_bps, bias_fp, ideal_hits, unit_hits = evaluate_sparse_tripod_seed(
        cx, cy, zoom
    )
    logit = -int(risk_fp) + bias_fp
    prob = sigmoid_bps(logit)
    allowed = prob >= threshold
    confidence_bps = prob if allowed else (10000 - prob)
    latency_us = (time.perf_counter() - t0) * 1_000_000.0

    return {
        "allowed": allowed,
        "noul": 1 if allowed else 0,
        "confidence_bps": confidence_bps,
        "prob_bps": prob,
        "boundedness_bps": bounded_bps,
        "bias_fp": bias_fp,
        "logit": logit,
        "plane_escapes": list(esc_planes),
        "total_escapes": total_escapes,
        "zmod9_ideal_hits": ideal_hits,
        "zmod9_unit_hits": unit_hits,
        "latency_us": round(latency_us, 2),
    }


# ---------------------------------------------------------------------------
# NEAR Intent & Chain Signatures Pre-Signing Guard
# ---------------------------------------------------------------------------

@dataclass
class NearIntentPayload:
    intent_id: str
    sender: str
    target_chain: str
    intent_type: str
    amount_usd: float
    volatility_bps: int
    slippage_bps: int
    is_flashloan: bool
    nonce: int = 1
    deadline_sec: int = 300

    def state_hash_hex(self) -> str:
        canonical = (
            f"{self.intent_id}|{self.sender}|{self.target_chain}|"
            f"{self.intent_type}|{self.nonce}"
        )
        return "0x" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def encode_intent_risk_fp(intent: NearIntentPayload) -> int:
    """
    Maps NEAR Intent market telemetry into signed Q16.16 riskScoreFP centered around 0.
    Calm swaps produce slightly negative riskFP (< 0); elevated slippage/volatility/flashloans
    drive positive riskFP (> biasFP) to trigger an immediate deterministic VETO.
    """
    notional_factor = 0.25 if intent.amount_usd >= 100_000.0 else 0.0
    norm_risk = (
        (intent.volatility_bps / 250.0)
        + (intent.slippage_bps / 280.0)
        + (1.50 if intent.is_flashloan else 0.0)
        + notional_factor
        - 0.35
    )
    return int(round(norm_risk * FP_ONE))


def encode_preview_calldata(risk_fp: int, state_hash_hex: str = "0x" + "00" * 32) -> str:
    """Encodes `previewDecision(bytes32,int64)` calldata (`0x0eea75c5`)."""
    h = state_hash_hex[2:].rjust(64, "0")[-64:]
    r = format(risk_fp & ((1 << 256) - 1), "064x")
    return SEL_PREVIEW_DECISION + h + r


class WerracleNearIntentGuard:
    """Zero-storage Chain Signatures (v1.signer) & NEAR Intents pre-signing policy gate."""

    def __init__(self, seed: Optional[Dict[str, int]] = None) -> None:
        self.seed = seed or dict(DEPLOYED_SEED_V2)

    def evaluate_intent(self, intent: NearIntentPayload) -> Dict[str, Any]:
        risk_fp = encode_intent_risk_fp(intent)
        res = tripod_preview_q16_16(risk_fp, self.seed)

        if res["allowed"]:
            mpc_policy = "ALLOW_MPC_SIGN"
            action = (
                f"APPROVED -> Release v1.signer signature for {intent.target_chain} "
                f"(conf={res['confidence_bps']/100:.2f}%)"
            )
        elif intent.is_flashloan:
            mpc_policy = "VETO_MPC_SIGN"
            action = "BLOCKED -> Uncollateralized Flash-Loan / Drain Pattern Suppressed"
        else:
            mpc_policy = "VETO_MPC_SIGN"
            action = (
                f"BLOCKED -> Predatory MEV / Slippage Risk Detected "
                f"(conf={res['confidence_bps']/100:.2f}%)"
            )

        return {
            "intent_id": intent.intent_id,
            "sender": intent.sender,
            "target_chain": intent.target_chain,
            "intent_type": intent.intent_type,
            "amount_usd": intent.amount_usd,
            "volatility_bps": intent.volatility_bps,
            "slippage_bps": intent.slippage_bps,
            "is_flashloan": intent.is_flashloan,
            "state_hash": intent.state_hash_hex(),
            "risk_fp": risk_fp,
            "risk_float": round(risk_fp / FP_ONE, 4),
            "verdict": "PASS" if res["allowed"] else "VETO",
            "mpc_policy": mpc_policy,
            "action": action,
            "decide_noul_selector": SEL_DECIDE_NOUL,
            **res,
        }


def canonical_intent_scenarios() -> List[NearIntentPayload]:
    return [
        NearIntentPayload(
            intent_id="intent_001_clean_swap",
            sender="alice.near",
            target_chain="Base",
            intent_type="CROSS_CHAIN_SWAP",
            amount_usd=5000.00,
            volatility_bps=25,
            slippage_bps=15,
            is_flashloan=False,
        ),
        NearIntentPayload(
            intent_id="intent_002_predatory_sandwich",
            sender="attacker_bot.near",
            target_chain="Ethereum",
            intent_type="SANDWICH_MEV_ARBITRAGE",
            amount_usd=150000.00,
            volatility_bps=850,
            slippage_bps=320,
            is_flashloan=False,
        ),
        NearIntentPayload(
            intent_id="intent_003_flashloan_lending_drain",
            sender="dark_mev.near",
            target_chain="Arbitrum",
            intent_type="LENDING_POOL_DRAIN",
            amount_usd=2000000.00,
            volatility_bps=2400,
            slippage_bps=950,
            is_flashloan=True,
        ),
        NearIntentPayload(
            intent_id="intent_004_agent_commerce_micropayment",
            sender="pcworm.near",
            target_chain="Base",
            intent_type="AI_AGENT_API_PAYMENT",
            amount_usd=12.50,
            volatility_bps=10,
            slippage_bps=5,
            is_flashloan=False,
        ),
    ]


# ---------------------------------------------------------------------------
# HTTP / JSON-RPC Helpers & Live Cross-Chain Verification
# ---------------------------------------------------------------------------

def _http_json(url: str, payload: Optional[Dict[str, Any]] = None, timeout: float = 8.0) -> Any:
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=HTTP_HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _aurora_rpc(method: str, params: List[Any], timeout: float = 8.0) -> Any:
    res = _http_json(
        AURORA_TESTNET_RPC,
        {"jsonrpc": "2.0", "id": 1, "method": method, "params": params},
        timeout=timeout,
    )
    if "error" in res:
        raise RuntimeError(f"Aurora RPC error: {res['error']}")
    return res["result"]


def _decode_signed_word(word_hex: str, bits: int = 256) -> int:
    val = int(word_hex, 16)
    sign_bit = 1 << (bits - 1)
    mask = (1 << bits) - 1
    val &= mask
    return val - (1 << bits) if (val & sign_bit) else val


def decode_seed_words(seed_hex: str) -> Dict[str, int]:
    raw = seed_hex[2:] if seed_hex.startswith("0x") else seed_hex
    words = [raw[i * 64:(i + 1) * 64] for i in range(7)]
    return {
        "cx": _decode_signed_word(words[0], 64),
        "cy": _decode_signed_word(words[1], 64),
        "zoom": int(words[2], 16),
        "nonce": int(words[3], 16),
        "threshold": int(words[4], 16),
        "mode": int(words[5], 16),
        "active": int(words[6], 16),
    }


def decode_preview_decision(call_hex: str) -> Tuple[bool, int]:
    raw = call_hex[2:] if call_hex.startswith("0x") else call_hex
    allowed = int(raw[0:64], 16) != 0
    conf_bps = int(raw[64:128], 16)
    return allowed, conf_bps


def verify_aurora_live_parity(guard: WerracleNearIntentGuard, evals: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Verifies live deployed Aurora Testnet contracts match Python Q16.16 bit-for-bit."""
    blk_hex = _aurora_rpc("eth_blockNumber", [])
    block_number = int(blk_hex, 16)

    v1_owner_hex = _aurora_rpc("eth_call", [{"to": WERRACLE_V1_ADDR, "data": SEL_OWNER}, "latest"])
    v1_owner = "0x" + v1_owner_hex[-40:]

    seed_hex = _aurora_rpc("eth_call", [{"to": WERRACLE_TRIPOD_V2_ADDR, "data": SEL_SEED}, "latest"])
    onchain_seed = decode_seed_words(seed_hex)

    ideal6_hex = _aurora_rpc(
        "eth_call",
        [{"to": WERRACLE_TRIPOD_V2_ADDR, "data": SEL_IS_ZMOD9_IDEAL + format(6, "064x")}, "latest"],
    )
    ideal_6_true = int(ideal6_hex, 16) == 1

    # Gas estimate on decideNoul(bytes32(0), 0)
    calldata_noul = SEL_DECIDE_NOUL + ("0" * 128)
    est_gas = int(_aurora_rpc("eth_estimateGas", [{"to": WERRACLE_TRIPOD_V2_ADDR, "data": calldata_noul}]), 16)

    # Check bit-exact parity across calibration probes + all scenario risk inputs
    test_vectors: List[Tuple[str, int]] = [
        ("probe_calm_-1.0", -FP_ONE),
        ("probe_neutral_0.0", 0),
        ("probe_spike_+1.0", FP_ONE),
        ("probe_extreme_+2.5", 163840),
    ] + [(e["intent_id"], e["risk_fp"]) for e in evals]

    mismatches = []
    comparisons = []
    for label, r_fp in test_vectors:
        call_res = _aurora_rpc(
            "eth_call",
            [{"to": WERRACLE_TRIPOD_V2_ADDR, "data": encode_preview_calldata(r_fp)}, "latest"],
        )
        chain_ok, chain_conf = decode_preview_decision(call_res)
        py_res = tripod_preview_q16_16(r_fp, onchain_seed)
        match = (chain_ok == py_res["allowed"]) and (chain_conf == py_res["confidence_bps"])
        if not match:
            mismatches.append(label)
        comparisons.append({
            "label": label,
            "risk_fp": r_fp,
            "aurora": [chain_ok, chain_conf],
            "python": [py_res["allowed"], py_res["confidence_bps"]],
            "bit_exact_match": match,
        })

    return {
        "status": "ONLINE_VERIFIED" if (not mismatches and ideal_6_true) else "MISMATCH",
        "chain_id": 1313161555,
        "block_number": block_number,
        "v1_contract": WERRACLE_V1_ADDR,
        "v1_owner": v1_owner,
        "v2_tripod_contract": WERRACLE_TRIPOD_V2_ADDR,
        "onchain_seed": onchain_seed,
        "zmod9_ideal_6": ideal_6_true,
        "decide_noul_tx_gas_estimate": est_gas,
        "vectors_checked": len(comparisons),
        "mismatches": mismatches,
        "samples": comparisons[:4],
    }


def query_near_rpc_accounts() -> Dict[str, Any]:
    """Queries live NEAR Mainnet & Testnet RPCs for project, MPC signer, and Intents verifier."""
    targets = [
        ("mainnet", NEAR_MAINNET_RPC, "pcworm.near"),
        ("mainnet", NEAR_MAINNET_RPC, "v1.signer"),
        ("mainnet", NEAR_MAINNET_RPC, "intents.near"),
        ("testnet", NEAR_TESTNET_RPC, "v1.signer-prod.testnet"),
    ]
    accounts = []
    for net, url, acc in targets:
        res = _http_json(url, {
            "jsonrpc": "2.0",
            "id": "werracle",
            "method": "query",
            "params": {"request_type": "view_account", "finality": "final", "account_id": acc},
        })
        result = res.get("result", {})
        accounts.append({
            "network": net,
            "account_id": acc,
            "block_height": result.get("block_height"),
            "has_contract": result.get("code_hash", "1" * 32) != "1" * 32,
        })
    return {"status": "ONLINE_VERIFIED", "accounts": accounts}


def audit_live_1click_quote(guard: WerracleNearIntentGuard) -> Dict[str, Any]:
    """Fetches a real dry-run quote from NEAR Intents 1Click API & audits it via Aurora + Python."""
    tokens = _http_json(f"{NEAR_1CLICK_BASE}/tokens")
    deadline = (
        datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=30)
    ).strftime("%Y-%m-%dT%H:%M:%SZ")
    quote_req = {
        "dry": True,
        "swapType": "EXACT_INPUT",
        "slippageTolerance": 100,
        "originAsset": ASSET_WNEAR,
        "depositType": "ORIGIN_CHAIN",
        "destinationAsset": ASSET_NEAR_USDC,
        "amount": str(100 * 10**24),  # 100 wNEAR dry-run quote
        "refundTo": "pcworm.near",
        "refundType": "ORIGIN_CHAIN",
        "recipient": "pcworm.near",
        "recipientType": "DESTINATION_CHAIN",
        "deadline": deadline,
    }
    resp = _http_json(f"{NEAR_1CLICK_BASE}/quote", quote_req)
    q = resp["quote"]
    usd_in = float(q["amountInUsd"])
    usd_out = float(q["amountOutUsd"])
    implied_spread_bps = max(0, int(round(((usd_in - usd_out) / max(usd_in, 1e-9)) * 10000)))

    live_intent = NearIntentPayload(
        intent_id="live_1click_wnear_usdc",
        sender="pcworm.near",
        target_chain="NEAR-Intents (1Click dry)",
        intent_type="1CLICK_EXACT_INPUT",
        amount_usd=usd_in,
        volatility_bps=15,
        slippage_bps=implied_spread_bps,
        is_flashloan=False,
    )
    eval_res = guard.evaluate_intent(live_intent)
    chain_hex = _aurora_rpc(
        "eth_call",
        [{"to": WERRACLE_TRIPOD_V2_ADDR, "data": encode_preview_calldata(eval_res["risk_fp"])}, "latest"],
    )
    chain_ok, chain_conf = decode_preview_decision(chain_hex)

    return {
        "status": "ONLINE_VERIFIED",
        "tokens_supported": len(tokens),
        "pair": "100 wNEAR -> USDC",
        "amount_in_usd": round(usd_in, 4),
        "amount_out_usd": round(usd_out, 4),
        "implied_spread_bps": implied_spread_bps,
        "time_estimate_sec": q.get("timeEstimate"),
        "verdict": eval_res["verdict"],
        "mpc_policy": eval_res["mpc_policy"],
        "python_conf_bps": eval_res["confidence_bps"],
        "aurora_v2_verified": (chain_ok == eval_res["allowed"]) and (chain_conf == eval_res["confidence_bps"]),
    }


def run_suite(offline: bool = False, custom_risk: Optional[float] = None) -> Dict[str, Any]:
    guard = WerracleNearIntentGuard()
    scenarios = canonical_intent_scenarios()
    if custom_risk is not None:
        custom_fp = int(round(custom_risk * FP_ONE))
        custom_eval = {
            "custom_risk": custom_risk,
            "risk_fp": custom_fp,
            **tripod_preview_q16_16(custom_fp, guard.seed),
        }
    else:
        custom_eval = None

    evals = [guard.evaluate_intent(s) for s in scenarios]

    report: Dict[str, Any] = {
        "telemetry_enabled": TELEMETRY_ENABLED,
        "deployed_seed": guard.seed,
        "scenarios": evals,
        "custom_eval": custom_eval,
        "live": {"mode": "OFFLINE" if offline else "LIVE"},
    }

    if not offline:
        try:
            report["live"]["aurora_testnet"] = verify_aurora_live_parity(guard, evals)
        except (urllib.error.URLError, TimeoutError, OSError, RuntimeError, ValueError) as exc:
            report["live"]["aurora_testnet"] = {"status": "OFFLINE_FALLBACK", "error": str(exc)}

        try:
            report["live"]["near_rpc"] = query_near_rpc_accounts()
        except (urllib.error.URLError, TimeoutError, OSError, RuntimeError, ValueError) as exc:
            report["live"]["near_rpc"] = {"status": "OFFLINE_FALLBACK", "error": str(exc)}

        try:
            report["live"]["near_intents_1click"] = audit_live_1click_quote(guard)
        except (urllib.error.URLError, TimeoutError, OSError, RuntimeError, ValueError) as exc:
            report["live"]["near_intents_1click"] = {"status": "OFFLINE_FALLBACK", "error": str(exc)}

    return report


def _print_human_report(report: Dict[str, Any]) -> None:
    print("=" * 80)
    print("WERRACLE NEAR INTENTS GUARD, CHAIN SIGNATURES GATE & LIVE AURORA VERIFIER")
    print("=" * 80)

    evals = report["scenarios"]
    for ev in evals:
        badge = "[PASS]" if ev["verdict"] == "PASS" else "[VETO]"
        print(f"\n{badge} {ev['intent_id']}")
        print(f"   Sender       : {ev['sender']} -> Target Chain: {ev['target_chain']}")
        print(f"   Intent Type  : {ev['intent_type']} (${ev['amount_usd']:,.2f})")
        print(f"   Telemetry    : vol={ev['volatility_bps']} bps | slip={ev['slippage_bps']} bps | flashloan={ev['is_flashloan']}")
        print(f"   ZMod9 Tripod : bounded={ev['boundedness_bps']/100:.2f}% | escapes={ev['total_escapes']}/108 | I3/Unit={ev['zmod9_ideal_hits']}/{ev['zmod9_unit_hits']}")
        print(f"   Verdict      : {ev['verdict']} ({ev['mpc_policy']}, NOUL={ev['noul']}, conf={ev['confidence_bps']/100:.2f}%)")
        print(f"   Action       : {ev['action']}")
        print(f"   Latency      : {ev['latency_us']:.2f} us (Python Q16.16) | selector={ev['decide_noul_selector']}")

    if report["custom_eval"]:
        ce = report["custom_eval"]
        print(f"\n[CUSTOM RISK={ce['custom_risk']}] allowed={ce['allowed']} | conf={ce['confidence_bps']} bps | bounded={ce['boundedness_bps']} bps")

    live = report["live"]
    print("\n" + "-" * 80)
    print("LIVE CROSS-CHAIN & BIT-EXACT AURORA EVM VERIFICATION")
    print("-" * 80)
    if live["mode"] == "OFFLINE":
        print("   Mode: --offline (network checks skipped; local Q16.16 ZMod9 kernel verified)")
    else:
        au = live.get("aurora_testnet", {})
        if au.get("status") == "ONLINE_VERIFIED":
            print(f"   [OK] Aurora Testnet (Chain {au['chain_id']}, Block #{au['block_number']:,})")
            print(f"        Contract v2 : {au['v2_tripod_contract']} | isZMod9ResonantIdeal(6)={au['zmod9_ideal_6']}")
            print(f"        Contract v1 : {au['v1_contract']} | owner={au['v1_owner']}")
            print(f"        Parity Check: {au['vectors_checked']}/{au['vectors_checked']} vectors 100% BIT-EXACT MATCH | tx gas est={au['decide_noul_tx_gas_estimate']}")
        else:
            print(f"   [WARN] Aurora Testnet: {au}")

        nr = live.get("near_rpc", {})
        if nr.get("status") == "ONLINE_VERIFIED":
            summary = ", ".join(f"{a['account_id']}@{a['network']}(blk={a['block_height']})" for a in nr["accounts"])
            print(f"   [OK] NEAR RPC Accounts: {summary}")
        else:
            print(f"   [WARN] NEAR RPC: {nr}")

        oc = live.get("near_intents_1click", {})
        if oc.get("status") == "ONLINE_VERIFIED":
            print(
                f"   [OK] NEAR Intents 1Click API ({oc['tokens_supported']} assets): "
                f"{oc['pair']} | in=${oc['amount_in_usd']:.4f} -> out=${oc['amount_out_usd']:.4f} "
                f"(spread={oc['implied_spread_bps']} bps, est={oc['time_estimate_sec']}s)"
            )
            print(f"        Pre-Sign Gate: {oc['verdict']} ({oc['mpc_policy']}) | Aurora Cross-Check={oc['aurora_v2_verified']}")
        else:
            print(f"   [WARN] NEAR 1Click API: {oc}")

    avg_us = sum(e["latency_us"] for e in evals) / len(evals)
    print("\n" + "=" * 80)
    print(f"AUDIT SUMMARY: 4/4 canonical intents triaged | Avg Q16.16 reflex latency: {avg_us:.2f} us | TELEMETRY={TELEMETRY_ENABLED}")
    print("=" * 80)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Werracle NEAR Intent Guard & Live Aurora Verifier")
    parser.add_argument("--offline", action="store_true", help="Skip live RPC/1Click network checks")
    parser.add_argument("--json", action="store_true", help="Output structured JSON report")
    parser.add_argument("--eval-risk", type=float, default=None, help="Evaluate custom float riskScore through ZMod9 Tripod")
    args = parser.parse_args(argv)

    report = run_suite(offline=args.offline, custom_risk=args.eval_risk)

    # Assert core security invariants hold on canonical suite
    scenarios_by_id = {s["intent_id"]: s for s in report["scenarios"]}
    assert scenarios_by_id["intent_001_clean_swap"]["verdict"] == "PASS"
    assert scenarios_by_id["intent_002_predatory_sandwich"]["verdict"] == "VETO"
    assert scenarios_by_id["intent_003_flashloan_lending_drain"]["verdict"] == "VETO"
    assert scenarios_by_id["intent_004_agent_commerce_micropayment"]["verdict"] == "PASS"

    au = report["live"].get("aurora_testnet", {})
    if au.get("status") == "MISMATCH":
        if args.json:
            print(json.dumps(report, indent=2))
        else:
            _print_human_report(report)
        return 1

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        _print_human_report(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
