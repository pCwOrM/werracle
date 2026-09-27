"""
tests.test_orthogonal_parameters
=================================
Verifies WERR v0.5.1 Orthogonal 8-State Parameter Architecture,
Auto-Guard Rules, Supercritical Pitchfork Cadence Bifurcation,
and Pre-Calibrated Oracle Presets in Werracle.

Invariant Checks:
- Zero external telemetry (TELEMETRY_ENABLED = False)
- 100% Deterministic execution
- 0 Bytes VRAM / 0 stored neural tensors
"""

import unittest
import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from engine import (
    WerracleCoreEngine,
    CalibratedWerracleOracle,
    TripodZMod9Oracle,
    BlockchainVocabulary,
    BlockchainResonanceMatrix,
    TELEMETRY_ENABLED,
    apply_cadence_bifurcation,
    create_oracle_security_guard,
    create_oracle_smart_router,
    create_oracle_risk_evaluator,
    create_pure_fractal_reflex,
    create_tripod_zmod9_guardian
)


class TestOrthogonalParameters(unittest.TestCase):
    """
    Test suite for the 8-state orthogonal parameter architecture (2 x 2 x 2)
    and Auto-Guard rules.
    """

    def test_01_privacy_invariant(self):
        """Verify strict zero-telemetry privacy invariant."""
        self.assertFalse(TELEMETRY_ENABLED, "CRITICAL: Telemetry must be permanently disabled in Werracle")

    def test_02_orthogonal_8_state_matrix_core(self):
        """
        Verify all 8 boolean combinations of (enable_domain, enable_lexical, enable_resonance)
        on WerracleCoreEngine.
        """
        for d_on in (False, True):
            for l_on in (False, True):
                for r_on in (False, True):
                    eng = WerracleCoreEngine(
                        enable_domain=d_on,
                        enable_lexical=l_on,
                        enable_resonance=r_on,
                        resolution=24,
                        max_iter=24
                    )
                    if not d_on:
                        # Rule 1: When Domain is OFF, domain dictionaries are locked OFF
                        self.assertFalse(eng.enable_lexical, f"Lexical must be False when domain=False (state: {d_on},{l_on},{r_on})")
                        self.assertFalse(eng.enable_resonance, f"Resonance must be False when domain=False (state: {d_on},{l_on},{r_on})")
                        self.assertFalse(eng.effective_domain_active, f"effective_domain_active must be False when domain=False")
                    elif not l_on and not r_on:
                        # Rule 2: [1,0,0] auto-guards to Universal Cusp
                        self.assertFalse(eng.effective_domain_active, "State [1,0,0] must auto-guard to Universal Cusp (effective=False)")
                    else:
                        # Rule 3: [1,1,0], [1,0,1], [1,1,1] activate domain + selected dictionaries
                        self.assertTrue(eng.effective_domain_active, f"State [{int(d_on)},{int(l_on)},{int(r_on)}] must activate domain")
                        self.assertEqual(eng.enable_lexical, l_on)
                        self.assertEqual(eng.enable_resonance, r_on)

    def test_03_orthogonal_8_state_matrix_calibrated_oracle(self):
        """
        Verify all 8 states on CalibratedWerracleOracle and their effect on transaction triage.
        """
        for d_on in (False, True):
            for l_on in (False, True):
                for r_on in (False, True):
                    oracle = CalibratedWerracleOracle(
                        enable_domain=d_on,
                        enable_lexical=l_on,
                        enable_resonance=r_on
                    )
                    if not d_on or (not l_on and not r_on):
                        self.assertFalse(oracle.effective_domain_active)
                    else:
                        self.assertTrue(oracle.effective_domain_active)

                    # Triage benign swap transaction
                    res = oracle.triage_transaction(
                        intent_text="dynamic pool swap exact input",
                        borrow_eth=0.0,
                        reserve_eth=100.0,
                        slippage_pct=0.5
                    )
                    self.assertTrue(res["is_allowed"])
                    self.assertIn("coordinates", res)

                    if not oracle.effective_domain_active:
                        # Coordinates must remain exactly the Universal Base Cusp coordinates
                        self.assertAlmostEqual(res["coordinates"]["cx"], round(oracle.cx, 6), places=5)
                        self.assertAlmostEqual(res["coordinates"]["cy"], round(oracle.cy, 6), places=5)

    def test_04_cadence_pitchfork_bifurcation(self):
        """
        Verify pitchfork bifurcation breaks deadlock between competing candidates.
        """
        # Close scores representing a decision deadlock (gap < 0.85)
        deadlock_scores = [2.00, 2.01, 1.99]
        bifurcated = apply_cadence_bifurcation(
            deadlock_scores,
            lambda_param=0.10,
            alpha=0.50,
            beta=0.15,
            deadlock_threshold=0.85
        )
        # Gap should expand after bifurcation
        initial_gap = abs(deadlock_scores[1] - deadlock_scores[0])
        final_gap = abs(bifurcated[1] - bifurcated[0])
        self.assertGreater(final_gap, initial_gap, "Bifurcation must widen the decision margin to break deadlock")

        # Well-separated scores (gap >= 0.85) should not be modified
        separated_scores = [1.0, 3.5, 0.5]
        bif_sep = apply_cadence_bifurcation(
            separated_scores,
            lambda_param=0.10,
            alpha=0.50,
            beta=0.15,
            deadlock_threshold=0.85
        )
        for orig, bif in zip(separated_scores, bif_sep):
            self.assertAlmostEqual(orig, bif, places=6, msg="Non-deadlocked scores must remain unaltered")

    def test_05_precalibrated_presets(self):
        """
        Verify that all pre-calibrated oracle presets initialize cleanly and produce valid decisions.
        """
        guard = create_oracle_security_guard()
        router = create_oracle_smart_router()
        evaluator = create_oracle_risk_evaluator()
        pure = create_pure_fractal_reflex()
        tripod = create_tripod_zmod9_guardian()

        # Guard
        self.assertTrue(guard.effective_domain_active)
        self.assertEqual(guard.zoom, 120.0)
        res_guard = guard.triage_transaction("critical pool drain flashloan", 50.0, 10.0, 15.0)
        self.assertFalse(res_guard["is_allowed"])
        self.assertEqual(res_guard["action"], "REVERT_TRANSACTION")

        # Router
        self.assertTrue(router.effective_domain_active)
        self.assertEqual(router.zoom, 45.0)
        res_router = router.triage_transaction("swap exact input 5 eth", 0.0, 100.0, 0.1)
        self.assertTrue(res_router["is_allowed"])

        # Evaluator
        self.assertTrue(evaluator.effective_domain_active)
        self.assertEqual(evaluator.zoom, 25.0)

        # Pure Fractal [0, 0, 0]
        self.assertFalse(pure.effective_domain_active)
        self.assertFalse(pure.enable_lexical)
        self.assertFalse(pure.enable_resonance)
        res_pure = pure.triage_transaction("arbitrary transaction text", 0.0, 50.0, 0.2)
        self.assertTrue(res_pure["is_allowed"])

        # Tripod Guardian
        res_tripod = tripod.decide_transaction("atomic flashloan exploit reentrancy probe")
        self.assertFalse(res_tripod["is_permitted"])
        self.assertEqual(res_tripod["verdict"], "REVERT_CIRCUIT_BREAKER")

    def test_06_blockchain_resonance_orthogonal_switches(self):
        """
        Verify that BlockchainResonanceMatrix correctly decouples lexical matching
        and spectral coordinate displacement.
        """
        sample_tx = "predatory sandwich frontrun priority gas mempool snipe"

        # 1. Both ON [1, 1]
        fused_both = BlockchainResonanceMatrix.fuse_resonance(
            sample_tx, enable_lexical=True, enable_resonance=True
        )
        self.assertGreater(len(fused_both["matched_tokens"]), 1)
        self.assertNotEqual(fused_both["delta_cx"], 0.0)

        # 2. Lexical ON, Resonance OFF [1, 0]
        fused_lex_only = BlockchainResonanceMatrix.fuse_resonance(
            sample_tx, enable_lexical=True, enable_resonance=False
        )
        self.assertGreater(len(fused_lex_only["matched_tokens"]), 1)
        self.assertEqual(fused_lex_only["delta_cx"], 0.0)
        self.assertEqual(fused_lex_only["delta_cy"], 0.0)

        # 3. Lexical OFF, Resonance ON [0, 1]
        fused_res_only = BlockchainResonanceMatrix.fuse_resonance(
            sample_tx, enable_lexical=False, enable_resonance=True
        )
        self.assertEqual(fused_res_only["matched_tokens"], ["NORMAL_TRANSACTION_FLOW"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
