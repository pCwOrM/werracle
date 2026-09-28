"""
tests/test_all_states_and_lean4_bridge.py
=========================================
Exhaustive State-Space Verification Suite for Werracle v0.5.1 + Lean 4 (GAP-0331) Bridge:
1. All 9 Residue States of Z/9Z (GAP-0331 ZModnZObj.isUnit_iff Unit Group vs. Maximal Ideal I_3)
   + 109 Multi-Cycle Escape Steps + 81 Additive/Multiplicative Closure Pairs + Euler Totient Order 6
2. All 8 Orthogonal Parameter States (2 x 2 x 2: enable_domain, enable_lexical, enable_resonance)
   Verified against Lean 4 Theorem 1G (`orthogonal_8state_autoguard_invariance`)
3. All 6 Mined 40-Core Golden Coordinate Pools (`ETH/USDC`, `WBTC/USDC`, `UNI/ETH`, `ARB/USDC`, `SOL/USDC`, `AAVE/ETH`)
   x All 8 Orthogonal Parameter States x 4 Market Regimes (192 Full Oracle State Combinations)
4. All 4 Tripod Parameter States (2 x 2: enable_lexical, enable_resonance) x 6 Golden Pools (24 Tripod Combinations)
5. All 40 BlockchainVocabulary Tokens & All 5 BlockchainPillar Categories (Exhaustive Token/Domain Matrix)
6. Formal Lean 4 Proof Package (`formal_proofs/WerracleProof.lean`, 13 Theorems, 0 `sorry`) & Solidity Contract Parity
"""

import os
import re
import sys
import math
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from engine import (
    WerracleCoreEngine,
    CalibratedWerracleOracle,
    TripodZMod9Oracle,
    DeFiFlashLoanGate,
    AmmDynamicFeeGate,
    RegulatoryComplianceGate,
    OntologicalDomain,
    BlockchainVocabulary,
    BlockchainResonanceMatrix,
    BlockchainPillar,
    GOLDEN_PAIR_SEEDS,
    get_golden_pair_seed,
    create_golden_pair_oracle,
    create_golden_pair_tripod,
    is_zmod9_resonant_ideal,
    is_zmod9_coprime_unit,
    classify_zmod9_state,
    ZMOD9_RESONANT_IDEAL_I3,
    ZMOD9_COPRIME_UNIT_KERNEL,
    ZMOD9_UNIT_INVERSES,
    float_to_fp,
    TELEMETRY_ENABLED,
)


class TestExhaustiveAllStatesAndLean4Bridge(unittest.TestCase):
    """
    Tests every possible algebraic, parametric, pool, token, and domain state of Werracle.
    """

    def test_01_exhaustive_zmod9_gap0331_all_9_residues_and_closure(self):
        """
        Exhaustive test of all 9 elements in Z/9Z, 109 escape steps [0..108],
        81 ring operations, and 6 invertible units (Lean 4 Theorems 1A-1F & GAP-0331).
        """
        self.assertEqual(ZMOD9_RESONANT_IDEAL_I3, frozenset({0, 3, 6}))
        self.assertEqual(ZMOD9_COPRIME_UNIT_KERNEL, frozenset({1, 2, 4, 5, 7, 8}))
        self.assertEqual(len(ZMOD9_RESONANT_IDEAL_I3) + len(ZMOD9_COPRIME_UNIT_KERNEL), 9)
        self.assertEqual(ZMOD9_RESONANT_IDEAL_I3 & ZMOD9_COPRIME_UNIT_KERNEL, frozenset())

        # Test all 109 escape steps (12 full Z/9Z cycles)
        for step in range(109):
            info = classify_zmod9_state(step)
            r = step % 9
            coprime = (math.gcd(r, 9) == 1)
            self.assertEqual(info["residue_mod9"], r)
            self.assertEqual(is_zmod9_coprime_unit(step), coprime)
            self.assertEqual(is_zmod9_resonant_ideal(step), not coprime)
            self.assertEqual(info["is_coprime_unit"], coprime)
            self.assertEqual(info["is_resonant_ideal"], not coprime)
            self.assertIn(info["triadic_projection_mod9"], ZMOD9_RESONANT_IDEAL_I3)

            if coprime:
                inv = info["multiplicative_inverse_mod9"]
                self.assertIsNotNone(inv)
                self.assertIn(inv, ZMOD9_COPRIME_UNIT_KERNEL)
                self.assertEqual((r * inv) % 9, 1)
                self.assertTrue(info["euler_totient_invariant"])
                self.assertEqual(pow(r, 6, 9), 1)
            else:
                self.assertIsNone(info["multiplicative_inverse_mod9"])
                self.assertFalse(info["euler_totient_invariant"])

        # Exhaustive 9x9 = 81 ring operations in Z/9Z
        for a in range(9):
            for b in range(9):
                # Theorem 1A: Additive closure of I_3
                if a in ZMOD9_RESONANT_IDEAL_I3 and b in ZMOD9_RESONANT_IDEAL_I3:
                    self.assertTrue(is_zmod9_resonant_ideal(a + b))
                # Theorem 1B: Ideal absorption of I_3 under multiplication by any r in Z/9Z
                if b in ZMOD9_RESONANT_IDEAL_I3:
                    self.assertTrue(is_zmod9_resonant_ideal(a * b))
                # Theorem 1F: Multiplicative closure of Coprime Unit Group K_error = (Z/9Z)^x
                if a in ZMOD9_COPRIME_UNIT_KERNEL and b in ZMOD9_COPRIME_UNIT_KERNEL:
                    self.assertTrue(is_zmod9_coprime_unit(a * b))

    def test_02_exhaustive_8state_orthogonal_cube_theorem_1g(self):
        """
        Tests all 8 states of the (enable_domain, enable_lexical, enable_resonance) cube
        against Lean 4 Theorem 1G (`orthogonal_8state_autoguard_invariance`).
        """
        active_count = 0
        for d in (False, True):
            for l in (False, True):
                for r in (False, True):
                    core = WerracleCoreEngine(enable_domain=d, enable_lexical=l, enable_resonance=r)
                    oracle = CalibratedWerracleOracle(enable_domain=d, enable_lexical=l, enable_resonance=r)

                    eff_l = l if d else False
                    eff_r = r if d else False
                    eff_d = True if (d and (eff_l or eff_r)) else False

                    self.assertEqual(core.enable_lexical, eff_l)
                    self.assertEqual(core.enable_resonance, eff_r)
                    self.assertEqual(core.effective_domain_active, eff_d)

                    self.assertEqual(oracle.enable_lexical, eff_l)
                    self.assertEqual(oracle.enable_resonance, eff_r)
                    self.assertEqual(oracle.effective_domain_active, eff_d)

                    if eff_d:
                        active_count += 1

                    # Verify decide_noul returns all required keys including latency_us
                    res_noul = core.decide_noul(risk_signal=-0.8, context_name=f"state_{int(d)}_{int(l)}_{int(r)}")
                    for req_key in ("allowed", "probability", "confidence", "black_ratio", "fractal_bias", "latency_us"):
                        self.assertIn(req_key, res_noul)

        self.assertEqual(active_count, 3, "Theorem 1G: Exactly 3 of 8 states must activate specialized domain routing")

    def test_03_exhaustive_6_golden_pools_x_8_states_x_4_regimes_192_combinations(self):
        """
        Tests all 6 Mined Golden Coordinate Pools x 8 Orthogonal States x 4 Market Regimes = 192 combinations.
        """
        expected_pools = ["ETH/USDC", "WBTC/USDC", "UNI/ETH", "ARB/USDC", "SOL/USDC", "AAVE/ETH"]
        self.assertEqual(list(GOLDEN_PAIR_SEEDS.keys()), expected_pools)

        regimes = [
            ("Calm Retail", "normal_swap in Uniswap v4 pool with clean_retail wallet", 10.0, 1000.0, 0.2, False, True),
            ("Moderate Arbitrage", "arbitrage rebalancing in liquidity pool", 180.0, 1000.0, 2.5, False, True),
            ("MEV Sandwich", "sandwich_attack frontrun with slippage exploit", 300.0, 1000.0, 6.0, False, False),
            ("Flashloan Attack", "flash_loan exploit pool_drain reentrancy", 650.0, 1000.0, 15.0, True, False),
        ]

        total_evaluated = 0
        for pool_name in expected_pools:
            seed_info = get_golden_pair_seed(pool_name)
            self.assertIn(seed_info["zmod9_class"], ("I3_RESONANT_IDEAL", "K_ERROR_COPRIME_UNIT"))
            self.assertGreater(seed_info["sensitivity_ratio"], 5.0)

            for d in (False, True):
                for l in (False, True):
                    for r in (False, True):
                        oracle = create_golden_pair_oracle(
                            pool_name,
                            resolution=24,
                            max_iter=24,
                            enable_domain=d,
                            enable_lexical=l,
                            enable_resonance=r,
                        )
                        for regime_name, tx_text, borrow, reserve, slip, sanctioned, expected_allow in regimes:
                            res = oracle.triage_transaction(
                                intent_text=tx_text,
                                borrow_eth=borrow,
                                reserve_eth=reserve,
                                slippage_pct=slip,
                                is_sanctioned=sanctioned,
                            )
                            total_evaluated += 1
                            self.assertIn("is_allowed", res)
                            self.assertIn("action", res)
                            self.assertIn("calibrated_confidence", res)
                            self.assertIn("coordinates", res)

                            # Verify Auto-Guard coordinate lock when effective_domain_active is False
                            if not (d and (l or r)):
                                self.assertAlmostEqual(res["coordinates"]["cx"], round(seed_info["cx"], 6), places=5)
                                self.assertAlmostEqual(res["coordinates"]["cy"], round(seed_info["cy"], 6), places=5)

                            if regime_name == "Calm Retail":
                                self.assertTrue(res["is_allowed"])
                            elif regime_name == "Flashloan Attack":
                                self.assertFalse(res["is_allowed"])

        self.assertEqual(total_evaluated, 192)

    def test_04_exhaustive_6_golden_pools_x_4_tripod_states_24_combinations(self):
        """
        Tests TripodZMod9Oracle across all 6 Golden Coordinate Pools x 4 (lexical, resonance) states = 24 combinations,
        verifying the GAP-0331 Z/9Z partition diagnostics across all 12 Tripod points.
        """
        combos = 0
        for pool_name in GOLDEN_PAIR_SEEDS.keys():
            seed_info = get_golden_pair_seed(pool_name)
            for l in (False, True):
                for r in (False, True):
                    tripod = create_golden_pair_tripod(
                        pool_name,
                        enable_lexical=l,
                        enable_resonance=r,
                    )
                    res_benign = tripod.decide_transaction(
                        "normal_swap in Uniswap v4 pool with clean_retail wallet and safe_health_factor"
                    )
                    res_attack = tripod.decide_transaction(
                        "massive flashloan_burst with uncollateralized_borrow and pool_drain reserve_exhaustion"
                    )
                    combos += 1

                    for res in (res_benign, res_attack):
                        part = res["tripod_diagnostics"]["zmod9_gap0331_partition"]
                        self.assertEqual(
                            part["resonant_ideal_i3_pts"] + part["coprime_unit_k_error_pts"],
                            12,
                            "All 12 Tripod points must partition strictly into I_3 U K_error"
                        )
                        self.assertIn(
                            part["dominant_algebraic_phase"],
                            ("I3_RESONANT_IDEAL", "K_ERROR_COPRIME_UNIT")
                        )

                    # When lexical is active, verify benign vs attack fee & verdict separation
                    if l:
                        self.assertLess(res_benign["suggested_fee_pips"], res_attack["suggested_fee_pips"])
                        self.assertEqual(res_attack["verdict"], "REVERT_CIRCUIT_BREAKER")
                    else:
                        # When lexical is OFF, both fall back to NORMAL_TRANSACTION_FLOW
                        self.assertEqual(res_benign["matched_tokens"], ["NORMAL_TRANSACTION_FLOW"])
                        self.assertEqual(res_attack["matched_tokens"], ["NORMAL_TRANSACTION_FLOW"])

                    # When resonance is OFF, target coordinates must remain locked to base seed
                    if not r:
                        self.assertAlmostEqual(res_attack["target_coords"]["cx"], seed_info["cx"], places=5)
                        self.assertAlmostEqual(res_attack["target_coords"]["cy"], seed_info["cy"], places=5)

        self.assertEqual(combos, 24)

    def test_05_exhaustive_40_vocabulary_tokens_and_5_pillars(self):
        """
        Tests all 40 BlockchainVocabulary tokens individually and all 5 BlockchainPillar categories.
        """
        self.assertFalse(TELEMETRY_ENABLED)
        all_tokens = BlockchainVocabulary.all_tokens()
        self.assertEqual(len(all_tokens), 40, "BlockchainVocabulary must contain all 40 canonical tokens")

        oracle = TripodZMod9Oracle()
        seen_pillars = set()

        for tok in all_tokens:
            seen_pillars.add(tok.pillar)
            self.assertIn(tok.tesla_harmonic, (3, 6, 9))
            # Evaluate token by its canonical name through Resonance Matrix and TripodZMod9Oracle
            res = oracle.decide_transaction(tok.name.lower())
            self.assertIn(tok.name, res["matched_tokens"], f"Token {tok.name} failed self-match")
            self.assertGreaterEqual(res["suggested_fee_pips"], 500)
            self.assertLessEqual(res["suggested_fee_pips"], 5000)

        self.assertEqual(len(seen_pillars), 5, "All 5 BlockchainPillar categories must be covered")

        # Also test all 3 specialized DeFi Gates across edge cases
        fl_gate = DeFiFlashLoanGate()
        self.assertTrue(fl_gate.evaluate_transaction(1000, 1000000, 0.1, False)["allowed"])
        self.assertFalse(fl_gate.evaluate_transaction(800000, 1000000, 8.5, True)["allowed"])

        fee_gate = AmmDynamicFeeGate()
        self.assertEqual(fee_gate.calculate_fee_pips(0.0, 0.0)["fee_pips"], 500)
        self.assertEqual(fee_gate.calculate_fee_pips(3.5, 80.0)["fee_pips"], 5000)

        aml_gate = RegulatoryComplianceGate()
        self.assertEqual(aml_gate.check_compliance(365, 1.0, False, False)["status"], "APPROVED")
        self.assertEqual(aml_gate.check_compliance(1, 100.0, True, True)["status"], "BLOCKED_SANCTION")

    def test_06_lean4_proof_package_and_solidity_contract_parity(self):
        """
        Verifies that `formal_proofs/WerracleProof.lean` (13 theorems, 0 sorry) and Solidity contracts
        (`WerracleTripodZMod9.sol` and `WerracleFeeHook.sol`) contain all 6 Golden Seeds and GAP-0331 helpers.
        """
        lean_file = PROJECT_ROOT / "formal_proofs" / "WerracleProof.lean"
        self.assertTrue(lean_file.is_file(), "formal_proofs/WerracleProof.lean must exist in werracle")
        lean_code = lean_file.read_text(encoding="utf-8")

        clean_code = re.sub(r"/-\![\s\S]*?-\/", "", lean_code)
        clean_code = re.sub(r"/-[\s\S]*?-\/", "", clean_code)
        clean_code = re.sub(r"--.*$", "", clean_code, flags=re.MULTILINE)
        self.assertIsNone(re.search(r"\bsorry\b", clean_code), "Lean 4 proof must have zero sorry placeholders")

        required_theorems = [
            "zmod9_resonant_additive_closure",
            "zmod9_resonant_ideal_absorption",
            "zmod9_triadic_projection",
            "zmod9_partition_cardinality",
            "zmod9_error_kernel_iff_coprime_unit",
            "zmod9_unit_group_closure_and_totient",
            "orthogonal_8state_autoguard_invariance",
            "escape_zmod9_bounded",
            "escape_werracle_bounded",
            "q16_16_square_no_int64_overflow",
            "escape_zmod9_non_constant_spectrum",
            "observer_horizon_quadrant_sensitivity",
            "evm_gas_parametric_bound",
        ]
        for thm in required_theorems:
            self.assertIn(f"theorem {thm}", lean_code, f"Missing theorem {thm} in WerracleProof.lean")

        sol_tripod = (PROJECT_ROOT / "contracts" / "WerracleTripodZMod9.sol").read_text(encoding="utf-8")
        for fn_name in (
            "getSeedEthUsdc",
            "getSeedWbtcUsdc",
            "getSeedUniEth",
            "getSeedArbUsdc",
            "getSeedSolUsdc",
            "getSeedAaveEth",
            "isZMod9ResonantIdeal",
            "isZMod9CoprimeUnit",
        ):
            self.assertIn(f"function {fn_name}", sol_tripod, f"Missing {fn_name} in WerracleTripodZMod9.sol")

        sol_hook = (PROJECT_ROOT / "contracts" / "hooks" / "WerracleFeeHook.sol").read_text(encoding="utf-8")
        for pool_const in (
            "POOL_ETH_USDC",
            "POOL_WBTC_USDC",
            "POOL_UNI_ETH",
            "POOL_ARB_USDC",
            "POOL_SOL_USDC",
            "POOL_AAVE_ETH",
            "getGoldenPoolSeed",
        ):
            self.assertIn(pool_const, sol_hook, f"Missing {pool_const} in WerracleFeeHook.sol")


if __name__ == "__main__":
    print("=" * 75)
    print(" [ALL-STATES MATRIX] WERRACLE v0.5.1 + LEAN 4 (GAP-0331) EXHAUSTIVE SUITE")
    print("=" * 75)
    unittest.main(verbosity=2)
