"""
werracle.engine.tripod_zmod9_oracle
===================================
Experimental Phase 2 Decision Engine:
1. Multi-Scale Harmonic Tripod: 3 zoom planes (0.60x Wide, 1.00x Focus, 1.60x Deep)
   evaluated across 12 sparse cardinal points.
2. Z mod 9 Modular Escape Dynamics: Formal Lean 4 specification (ZMod 9)
   checking harmonic convergence milestones up to n = 9.
3. Lean 4 GAP-0331 Algebraic Bridge (`ZModnZObj.isUnit_iff`):
   Partitions Z/9Z into:
   - Resonant Sub-Ideal I_3 = {0, 3, 6} (Unique Maximal Ideal of Non-Units)
   - Non-Dissipative Error-Kernel K_error = {1, 2, 4, 5, 7, 8} (Coprime Unit Group (Z/9Z)^x)
4. High-Fusion Blockchain Lexicon Coupling: Integrates BlockchainResonanceMatrix.

Invariant: Zero Telemetry (TELEMETRY_ENABLED = False).
Formal Mathematical Nomenclature: Z mod 9 / Lean 4 Modular Resonance.
"""

import math
from typing import Dict, List, Tuple, Any, Optional

from .blockchain_lexicon import (
    BlockchainVocabulary,
    BlockchainResonanceMatrix,
    float_to_fp,
    fp_to_float,
    fp_mul,
    FP_ONE,
    FP_SHIFT,
    TELEMETRY_ENABLED
)

# 4.0 in Q16.16
ESCAPE_LIMIT = 4 * FP_ONE

# Formal Z/9Z Algebraic Constants (Lean 4 WerracleProof & GAP-0331 ZModnZObj.isUnit_iff)
ZMOD9_RESONANT_IDEAL_I3 = frozenset({0, 3, 6})
ZMOD9_COPRIME_UNIT_KERNEL = frozenset({1, 2, 4, 5, 7, 8})
ZMOD9_UNIT_INVERSES: Dict[int, int] = {
    1: 1,  # 1 * 1 = 1 (mod 9)
    2: 5,  # 2 * 5 = 10 = 1 (mod 9)
    4: 7,  # 4 * 7 = 28 = 1 (mod 9)
    5: 2,  # 5 * 2 = 10 = 1 (mod 9)
    7: 4,  # 7 * 4 = 28 = 1 (mod 9)
    8: 8,  # 8 * 8 = 64 = 1 (mod 9)
}


def is_zmod9_resonant_ideal(escape_step: int) -> bool:
    """
    Lean 4 Theorem 1A/1B/1E (`IsResonantSubIdeal`):
    Returns True iff `escape_step mod 9` belongs to the unique maximal ideal of non-units I_3 = {0, 3, 6}.
    """
    return (int(escape_step) % 9) in ZMOD9_RESONANT_IDEAL_I3


def is_zmod9_coprime_unit(escape_step: int) -> bool:
    """
    Lean 4 Theorem 1E/1F (`zmod9_error_kernel_iff_coprime_unit` / GAP-0331 `ZModnZObj.isUnit_iff`):
    Returns True iff `escape_step mod 9` is coprime to 9, i.e., belongs to the invertible unit group
    K_error = (Z/9Z)^x = {1, 2, 4, 5, 7, 8}.
    """
    return (int(escape_step) % 9) in ZMOD9_COPRIME_UNIT_KERNEL


def classify_zmod9_state(escape_step: int) -> Dict[str, Any]:
    """
    Exhaustive algebraic classification of any escape count into Z/9Z (GAP-0331 Bridge).
    """
    r = int(escape_step) % 9
    is_unit = r in ZMOD9_COPRIME_UNIT_KERNEL
    inv: Optional[int] = ZMOD9_UNIT_INVERSES.get(r, None)
    return {
        "residue_mod9": r,
        "is_coprime_unit": is_unit,
        "is_resonant_ideal": not is_unit,
        "algebraic_class": "K_ERROR_COPRIME_UNIT" if is_unit else "I3_RESONANT_IDEAL",
        "multiplicative_inverse_mod9": inv,
        "euler_totient_invariant": ((r ** 6) % 9 == 1) if is_unit else False,
        "triadic_projection_mod9": (3 * r) % 9,
    }


def iterate_escape_zmod9(cx_fp: int, cy_fp: int) -> int:
    """
    Evaluates quadratic recurrence z_{n+1} = z_n^2 + c up to n = 9 in Z mod 9.
    Returns escape count (0 to 9).
    """
    zx = 0
    zy = 0

    for i in range(9):
        zx2 = (zx * zx) >> FP_SHIFT
        zy2 = (zy * zy) >> FP_SHIFT

        if zx2 + zy2 > ESCAPE_LIMIT:
            return i

        next_zx = zx2 - zy2 + cx_fp
        next_zy = ((zx * zy) >> (FP_SHIFT - 1)) + cy_fp
        zx = next_zx
        zy = next_zy

    return 9


class TripodZMod9Oracle:
    """
    Multi-Scale Harmonic Tripod Oracle with Z mod 9 Modular Dynamics & GAP-0331 Unit/Ideal Bridge.
    """

    def __init__(
        self,
        base_cx: float = -0.7436438870371587,
        base_cy: float = 0.13182590420531197,
        base_zoom: float = 50.0,
        decision_threshold: float = 0.50,
        enable_lexical: bool = True,
        enable_resonance: bool = True
    ):
        assert not TELEMETRY_ENABLED, "Invariant: Telemetry must be False"
        self.base_cx = base_cx
        self.base_cy = base_cy
        self.base_zoom = base_zoom
        self.threshold_bps = int(decision_threshold * 10000)
        self.enable_lexical = enable_lexical
        self.enable_resonance = enable_resonance

    def evaluate_sparse_tripod(
        self,
        cx_fp: int,
        cy_fp: int,
        zoom_fp: int
    ) -> Tuple[int, int, float, Dict[str, Any]]:
        """
        Evaluates 12-point Sparse Tripod across 3 zoom planes:
        - Wide  (0.60x): 4 cardinal points (Weight: 0.25)
        - Focus (1.00x): 4 cardinal points (Weight: 0.50)
        - Deep  (1.60x): 4 cardinal points (Weight: 0.25)

        Returns:
            composite_ratio_bps (int): [0 .. 10000]
            synthesized_noul (int): [0 .. 255]
            normalized_score (float): [0.0 .. 1.0]
            diagnostics (dict): per-plane escape statistics & GAP-0331 Z/9Z partition
        """
        z_wide = max(FP_ONE, (zoom_fp * 60) // 100)
        z_focus = max(FP_ONE, zoom_fp)
        z_deep = max(FP_ONE, (zoom_fp * 160) // 100)

        step_wide = (FP_ONE << FP_SHIFT) // z_wide
        step_focus = (FP_ONE << FP_SHIFT) // z_focus
        step_deep = (FP_ONE << FP_SHIFT) // z_deep

        # 1. Wide Plane (0.60x) - 4 cardinal points
        wide_pts = [
            iterate_escape_zmod9(cx_fp + step_wide, cy_fp),
            iterate_escape_zmod9(cx_fp - step_wide, cy_fp),
            iterate_escape_zmod9(cx_fp, cy_fp + step_wide),
            iterate_escape_zmod9(cx_fp, cy_fp - step_wide),
        ]
        esc_wide = sum(wide_pts)
        ratio_wide_bps = (esc_wide * 10000) // 36

        # 2. Focus Plane (1.00x) - 4 cardinal points
        focus_pts = [
            iterate_escape_zmod9(cx_fp + step_focus, cy_fp),
            iterate_escape_zmod9(cx_fp - step_focus, cy_fp),
            iterate_escape_zmod9(cx_fp, cy_fp + step_focus),
            iterate_escape_zmod9(cx_fp, cy_fp - step_focus),
        ]
        esc_focus = sum(focus_pts)
        ratio_focus_bps = (esc_focus * 10000) // 36

        # 3. Deep Plane (1.60x) - 4 cardinal points
        deep_pts = [
            iterate_escape_zmod9(cx_fp + step_deep, cy_fp),
            iterate_escape_zmod9(cx_fp - step_deep, cy_fp),
            iterate_escape_zmod9(cx_fp, cy_fp + step_deep),
            iterate_escape_zmod9(cx_fp, cy_fp - step_deep),
        ]
        esc_deep = sum(deep_pts)
        ratio_deep_bps = (esc_deep * 10000) // 36

        # Weighted Harmonic Fusion: 0.25 Wide + 0.50 Focus + 0.25 Deep
        composite_boundedness_bps = (ratio_wide_bps + 2 * ratio_focus_bps + ratio_deep_bps) >> 2

        # Synthesized Noul Byte (0..255)
        synthesized_noul = (composite_boundedness_bps * 255) // 10000
        normalized_score = composite_boundedness_bps / 10000.0

        # GAP-0331 Z/9Z Algebraic Partition across all 12 Tripod Points
        all_12_pts = wide_pts + focus_pts + deep_pts
        ideal_i3_count = sum(1 for p in all_12_pts if is_zmod9_resonant_ideal(p))
        unit_kernel_count = 12 - ideal_i3_count

        diagnostics = {
            "plane_escapes": {
                "wide_0_60x": esc_wide,
                "focus_1_00x": esc_focus,
                "deep_1_60x": esc_deep,
                "total_12pts": esc_wide + esc_focus + esc_deep
            },
            "plane_ratios_bps": {
                "wide": ratio_wide_bps,
                "focus": ratio_focus_bps,
                "deep": ratio_deep_bps
            },
            "composite_boundedness_bps": composite_boundedness_bps,
            "zmod9_gap0331_partition": {
                "resonant_ideal_i3_pts": ideal_i3_count,
                "coprime_unit_k_error_pts": unit_kernel_count,
                "ideal_ratio_bps": (ideal_i3_count * 10000) // 12,
                "unit_ratio_bps": (unit_kernel_count * 10000) // 12,
                "dominant_algebraic_phase": (
                    "I3_RESONANT_IDEAL" if ideal_i3_count >= unit_kernel_count else "K_ERROR_COPRIME_UNIT"
                )
            }
        }

        return composite_boundedness_bps, synthesized_noul, normalized_score, diagnostics

    def decide_transaction(self, transaction_text: str) -> Dict[str, Any]:
        """
        End-to-End High-Fusion Transaction Triage:
        1. Blockchain Lexicon Superposition (Resonance Matrix) -> (delta_cx, delta_cy, risk)
        2. Sparse Multi-Scale Harmonic Tripod Evaluation (Z mod 9) -> Boundedness ratio
        3. Automated Decision & Dynamic Fee Clamping (Uniswap v4 pips: 500 to 5000)
        """
        fused = BlockchainResonanceMatrix.fuse_resonance(
            transaction_text,
            base_cx=self.base_cx,
            base_cy=self.base_cy,
            base_zoom=self.base_zoom,
            enable_lexical=self.enable_lexical,
            enable_resonance=self.enable_resonance
        )

        cx_fp = float_to_fp(fused["target_cx"])
        cy_fp = float_to_fp(fused["target_cy"])
        zoom_fp = float_to_fp(fused["target_zoom"])

        composite_bps, noul_byte, norm_score, diag = self.evaluate_sparse_tripod(
            cx_fp, cy_fp, zoom_fp
        )

        # Net decision: If composite risk >= 0.70 OR composite boundedness < 5000 -> Revert
        is_safe = (fused["composite_risk"] < 0.70) and (diag["composite_boundedness_bps"] >= 5000)
        
        # Dynamic fee scaling between 0.05% (500 pips) and 0.50% (5000 pips)
        calculated_fee_pips = int(500 + fused["composite_risk"] * 4500)
        calculated_fee_pips = max(500, min(5000, calculated_fee_pips))

        return {
            "is_permitted": is_safe,
            "verdict": "PERMIT" if is_safe else "REVERT_CIRCUIT_BREAKER",
            "suggested_fee_pips": calculated_fee_pips,
            "composite_risk": fused["composite_risk"],
            "dominant_pillar": fused["dominant_pillar"],
            "matched_tokens": fused["matched_tokens"],
            "tesla_harmonics": fused["tesla_harmonic_distribution"],
            "tripod_diagnostics": diag,
            "target_coords": {
                "cx": fused["target_cx"],
                "cy": fused["target_cy"],
                "zoom": fused["target_zoom"]
            }
        }
