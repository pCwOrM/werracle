"""
tests/test_near_intent_guard.py
===============================
Deterministic unit tests for `near/werracle_near_intent_guard.py`:
- Zero external dependencies
- Offline bit-exact regression vectors pinned to live Aurora Testnet WerracleTripodZMod9
- Canonical NEAR Intents PASS/VETO security invariants
- ABI calldata encoding & decoding for previewDecision(bytes32,int64)
"""

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from near.werracle_near_intent_guard import (
    DEPLOYED_SEED_V2,
    FP_ONE,
    SEL_PREVIEW_DECISION,
    TELEMETRY_ENABLED,
    NearIntentPayload,
    WerracleNearIntentGuard,
    canonical_intent_scenarios,
    classify_zmod9,
    decode_preview_decision,
    encode_preview_calldata,
    main,
    run_suite,
    tripod_preview_q16_16,
)


def test_privacy_invariant():
    assert TELEMETRY_ENABLED is False


def test_bit_exact_aurora_v2_vectors():
    """Matches live WerracleTripodZMod9 at 0x1d7Ae9E1dDDA805539d9e225425804Ef8B9caBaF."""
    expected = {
        -65536: (True, 6466),
        -10000: (True, 5449),
        0: (True, 5266),
        5000: (True, 5175),
        65536: (False, 5934),
        163840: (False, 7734),
    }
    for risk_fp, (exp_ok, exp_conf) in expected.items():
        res = tripod_preview_q16_16(risk_fp, DEPLOYED_SEED_V2)
        assert res["allowed"] is exp_ok
        assert res["confidence_bps"] == exp_conf
        assert res["zmod9_ideal_hits"] + res["zmod9_unit_hits"] == 12


def test_canonical_intent_triage_invariants():
    guard = WerracleNearIntentGuard()
    results = {s.intent_id: guard.evaluate_intent(s) for s in canonical_intent_scenarios()}
    assert results["intent_001_clean_swap"]["verdict"] == "PASS"
    assert results["intent_001_clean_swap"]["mpc_policy"] == "ALLOW_MPC_SIGN"
    assert results["intent_004_agent_commerce_micropayment"]["verdict"] == "PASS"
    assert results["intent_002_predatory_sandwich"]["verdict"] == "VETO"
    assert results["intent_002_predatory_sandwich"]["mpc_policy"] == "VETO_MPC_SIGN"
    assert results["intent_003_flashloan_lending_drain"]["verdict"] == "VETO"
    for r in results.values():
        assert r["latency_us"] < 50.0


def test_adversarial_monotone_veto():
    guard = WerracleNearIntentGuard()
    attack = NearIntentPayload(
        intent_id="test_extreme_slip",
        sender="mev.near",
        target_chain="Base",
        intent_type="SWAP",
        amount_usd=250_000.0,
        volatility_bps=1200,
        slippage_bps=400,
        is_flashloan=True,
    )
    res = guard.evaluate_intent(attack)
    assert res["verdict"] == "VETO"
    assert res["allowed"] is False


def test_abi_calldata_and_decode_roundtrip():
    neg_call = encode_preview_calldata(-FP_ONE)
    assert neg_call.startswith(SEL_PREVIEW_DECISION)
    assert len(neg_call) == 2 + 8 + 64 + 64
    assert neg_call.endswith("f" * 60 + "0000")

    allowed_hex = "0x" + ("0" * 63 + "1") + format(5266, "064x")
    ok, conf = decode_preview_decision(allowed_hex)
    assert ok is True
    assert conf == 5266


def test_zmod9_classification():
    for step in (0, 3, 6, 9, 12, 18):
        assert classify_zmod9(step) == "I3_IDEAL"
    for step in (1, 2, 4, 5, 7, 8):
        assert classify_zmod9(step) == "K_ERROR_UNIT"


def test_cli_offline_json_exit_zero(capsys=None):
    if capsys is not None:
        rc = main(["--offline", "--json"])
        assert rc == 0
        out = json.loads(capsys.readouterr().out)
    else:
        out = run_suite(offline=True)
    assert out["telemetry_enabled"] is False
    assert out["live"]["mode"] == "OFFLINE"
    assert len(out["scenarios"]) == 4


if __name__ == "__main__":
    test_privacy_invariant()
    test_bit_exact_aurora_v2_vectors()
    test_canonical_intent_triage_invariants()
    test_adversarial_monotone_veto()
    test_abi_calldata_and_decode_roundtrip()
    test_zmod9_classification()
    test_cli_offline_json_exit_zero()
    print("[PASS] All 7 NEAR Intent Guard unit tests passed.")
