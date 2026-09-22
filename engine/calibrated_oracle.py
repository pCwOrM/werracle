"""
werracle.engine.calibrated_oracle
=================================
Production Calibrated On-Chain Decision Oracle Engine.
Bridges ontological domain categorization, temperature-calibrated sigmoid
probabilities, and EVM 32-byte slot Q16.16 fixed-point math.

Privacy & Security:
- WERR Telemetry is PERMANENTLY DISABLED.
- Zero external API/network connections.
- 100% Deterministic, local execution.
"""

import math
from typing import Dict, List, Tuple, Any, Optional

from .core import WerracleCoreEngine, sigmoid
from .domain_ontology import OntologicalDomain, TELEMETRY_ENABLED

# Q16.16 Fixed Point constants matching Solidity contracts
FP_SHIFT = 16
FP_ONE = 1 << FP_SHIFT


def float_to_fp(val: float) -> int:
    return int(round(val * FP_ONE))


def fp_to_float(fp: int) -> float:
    return float(fp) / FP_ONE


def fp_mul(a: int, b: int) -> int:
    return (a * b) >> FP_SHIFT


class CalibratedWerracleOracle:
    """
    Calibrated Werracle Oracle with domain ontology and strict zero-telemetry invariant.
    """
    def __init__(
        self,
        base_cx: float = -0.7436438870371587,
        base_cy: float = 0.13182590420531197,
        base_zoom: float = 50.0,
        temperature: float = 1.05,
        decision_threshold: float = 0.50
    ):
        # Strict privacy invariant
        if TELEMETRY_ENABLED:
            raise RuntimeError("CRITICAL_SECURITY_VIOLATION: Telemetry must remain disabled in Werracle.")

        self.cx = base_cx
        self.cy = base_cy
        self.zoom = base_zoom
        self.temperature = max(0.1, temperature)
        self.decision_threshold = decision_threshold
        self.core = WerracleCoreEngine(
            base_cx=base_cx, base_cy=base_cy, base_zoom=base_zoom
        )
        self.ontology = OntologicalDomain()

    def evaluate_mandelbrot_fixed_point_microgrid(
        self,
        cx_fp: int,
        cy_fp: int,
        zoom_fp: int
    ) -> Tuple[int, int, float, List[int]]:
        """
        Exact integer emulation of Solidity Werracle.sol 16-point Pareto micro-grid.
        Returns:
            total_escapes (int): [0 .. 192]
            synthesized_noul (int): [0 .. 255]
            normalized_score (float): [0.0 .. 1.0]
            quadrant_escapes (List[int]): [Q1, Q2, Q3, Q4]
        """
        delta_fp = (float_to_fp(0.04) << FP_SHIFT) // (zoom_fp // 10 if zoom_fp >= 10 else 1)
        grid_offsets = [-2, -1, 1, 2]
        
        total_escapes = 0
        q_escapes = [0, 0, 0, 0] # Q1, Q2, Q3, Q4
        ESCAPE_LIMIT = 4 * FP_ONE

        for dx in grid_offsets:
            for dy in grid_offsets:
                pt_cx = cx_fp + dx * delta_fp
                pt_cy = cy_fp + dy * delta_fp
                
                # 12-iteration quadratic escape
                zx = 0
                zy = 0
                count = 0
                for _ in range(12):
                    zx2 = fp_mul(zx, zx)
                    zy2 = fp_mul(zy, zy)
                    if zx2 + zy2 > ESCAPE_LIMIT:
                        break
                    next_zy = 2 * fp_mul(zx, zy) + pt_cy
                    next_zx = zx2 - zy2 + pt_cx
                    zx = next_zx
                    zy = next_zy
                    count += 1
                
                total_escapes += count
                if dx > 0 and dy > 0:
                    q_escapes[0] += count
                elif dx < 0 and dy > 0:
                    q_escapes[1] += count
                elif dx < 0 and dy < 0:
                    q_escapes[2] += count
                else:
                    q_escapes[3] += count

        noul = total_escapes % 256
        max_possible = 16 * 12 # 192
        score = total_escapes / float(max_possible)

        return total_escapes, noul, score, q_escapes

    def triage_transaction(
        self,
        intent_text: str,
        borrow_eth: float,
        reserve_eth: float,
        slippage_pct: float,
        wallet_age_days: int = 180,
        tx_per_min: float = 0.5,
        is_sanctioned: bool = False
    ) -> Dict[str, Any]:
        """
        Full-Spectrum Calibrated Web3 Transaction Triage.
        Combines intent ontology, threat scanning, pool ratio, and fixed-point execution.
        """
        # 1. Ontological Intent Classification
        intent_info = self.ontology.classify_intent(intent_text)
        threat_score, detected_threats = self.ontology.evaluate_risk_signatures(intent_text)

        # 2. Financial / Pool Risk Metrics
        borrow_ratio = (borrow_eth / reserve_eth) if reserve_eth > 0 else 1.0
        slippage_ratio = slippage_pct / 100.0

        if borrow_ratio > 0.40 or slippage_ratio > 0.10:
            threat_score = max(threat_score, 0.85)
            detected_threats.append("CRITICAL_FLASH_LOAN_DRAIN")
        elif borrow_ratio > 0.15 or slippage_ratio > 0.03:
            threat_score = max(threat_score, 0.45)
            detected_threats.append("ELEVATED_MEV_PRESSURE")

        # 3. Regulatory / AML Risk
        if is_sanctioned:
            threat_score = 1.0
            detected_threats.append("OFAC_SANCTION_MATCH")
        elif wallet_age_days < 7 and tx_per_min > 20.0:
            threat_score = max(threat_score, 0.60)
            detected_threats.append("HIGH_VELOCITY_SYBIL_BOT")

        threat_score = min(1.0, max(0.0, threat_score))

        # 4. Ontological Seed Derivation
        target_cx, target_cy, target_zoom = self.ontology.derive_ontological_seed(
            self.cx, self.cy, self.zoom, intent_info, threat_score
        )

        # 5. Fixed-Point Microgrid Execution
        cx_fp = float_to_fp(target_cx)
        cy_fp = float_to_fp(target_cy)
        zoom_fp = float_to_fp(target_zoom)

        total_esc, noul, raw_score, q_escapes = self.evaluate_mandelbrot_fixed_point_microgrid(
            cx_fp, cy_fp, zoom_fp
        )

        # 6. Temperature-Calibrated Decision
        logit = (raw_score - threat_score) / self.temperature
        calibrated_confidence = sigmoid(logit * 4.0)

        # Determine actionable smart contract command based on calibrated tiers
        if threat_score >= 0.75:
            action = "REVERT_TRANSACTION"
            is_allowed = False
            tier = 3
        elif threat_score >= 0.40:
            action = "APPLY_SURCHARGE_FEE"
            is_allowed = True
            tier = 2
        elif threat_score >= 0.20:
            action = "MONITOR_FLOW"
            is_allowed = True
            tier = 1
        else:
            action = "EXECUTE_IMMEDIATE"
            is_allowed = True
            tier = 0

        # EVM gas estimation (~18,000 base + 12 gas per escape step)
        estimated_gas = 18000 + (total_esc * 12)

        return {
            "is_allowed": is_allowed,
            "action": action,
            "aml_tier": tier,
            "intent": intent_info["intent"],
            "threat_score": round(threat_score, 4),
            "detected_threats": detected_threats,
            "calibrated_confidence": round(calibrated_confidence, 4),
            "synthesized_noul": f"0x{noul:02X}",
            "raw_mandelbrot_score": round(raw_score, 4),
            "estimated_gas": estimated_gas,
            "coordinates": {
                "cx": round(target_cx, 6),
                "cy": round(target_cy, 6),
                "zoom": round(target_zoom, 2)
            }
        }

    def calculate_dynamic_fee(
        self,
        volatility: float,
        imbalance_pct: float
    ) -> int:
        """
        Uniswap v4 dynamic fee calculation: returns pips in range [500, 5000] (0.05% .. 0.50%).
        """
        # Baseline fee = 3000 pips (0.30%)
        base_pips = 3000
        vol_factor = int(round(volatility * 1000))
        imb_factor = int(round(imbalance_pct * 25))

        fee_pips = base_pips + (vol_factor - 1000) + imb_factor
        return max(500, min(5000, fee_pips))
