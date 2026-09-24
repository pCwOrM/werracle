"""
tests/test_blockchain_resonance.py
==================================
Unit verification for Blockchain Semantic Vocabulary & High-Fusion Resonance Matrix.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from engine.blockchain_lexicon import BlockchainVocabulary, BlockchainResonanceMatrix, BlockchainPillar

def test_vocabulary():
    tokens = BlockchainVocabulary.all_tokens()
    print(f"[TEST 1] Registered Tokens Count: {len(tokens)}")
    assert len(tokens) == 40, f"Expected 40 tokens, got {len(tokens)}"

    pillars = set(t.pillar for t in tokens)
    print(f"  Distinct Pillars: {[p.value for p in pillars]}")
    assert len(pillars) == 5, f"Expected 5 pillars, got {len(pillars)}"

    harmonics = set(t.tesla_harmonic for t in tokens)
    print(f"  Tesla Harmonics: {sorted(list(harmonics))}")
    assert harmonics == {3, 6, 9}, f"Expected harmonics {{3, 6, 9}}, got {harmonics}"
    print("  -> PASSED: Vocabulary integrity verified.")

def test_resonance_fusion():
    print("\n[TEST 2] Testing High-Fusion Wave Superposition...")

    scenarios = [
        {
            "name": "Benign Retail Swap",
            "text": "normal_swap executing standard_trade with clean_retail wallet and safe_health_factor",
            "expected_action": "PERMIT_STANDARD_EXECUTION",
            "max_risk": 0.30
        },
        {
            "name": "Turbulent Orderflow / MEV Sandwich",
            "text": "frontrun attempt with predatory sandwich and high tick_velocity causing slippage_breach",
            "expected_action": "DYNAMIC_FEE_SURGE",
            "min_risk": 0.50
        },
        {
            "name": "Catastrophic Flash-Loan Exploit",
            "text": "flashloan_burst with uncollateralized_borrow and pool_drain attempting reentrancy_probe",
            "expected_action": "ATOMIC_REVERT_CIRCUIT_BREAKER",
            "min_risk": 0.85
        },
        {
            "name": "Sanctioned Mixer Inflow",
            "text": "sanctioned_mixer tornado_cash with ofac_sdn and illicit_hop transfer",
            "expected_action": "ATOMIC_REVERT_CIRCUIT_BREAKER",
            "min_risk": 0.90
        }
    ]

    for sc in scenarios:
        res = BlockchainResonanceMatrix.fuse_resonance(sc["text"])
        print(f"\nScenario: {sc['name']}")
        print(f"  Matched: {res['matched_tokens']}")
        print(f"  Dominant: {res['dominant_pillar']} | Risk: {res['composite_risk']}")
        print(f"  Action: {res['recommended_action']} | Suggested Fee: {res['suggested_fee_bps']} bps")
        print(f"  Displacement Q16.16: dx={res['delta_cx_fp']}, dy={res['delta_cy_fp']}")
        print(f"  Tesla Harmonics: {res['tesla_harmonic_distribution']}")

        if "expected_action" in sc:
            assert res["recommended_action"] == sc["expected_action"], (
                f"Action mismatch: expected {sc['expected_action']}, got {res['recommended_action']}"
            )
        if "max_risk" in sc:
            assert res["composite_risk"] <= sc["max_risk"], (
                f"Risk too high: {res['composite_risk']} > {sc['max_risk']}"
            )
        if "min_risk" in sc:
            assert res["composite_risk"] >= sc["min_risk"], (
                f"Risk too low: {res['composite_risk']} < {sc['min_risk']}"
            )

    print("\n[ALL TESTS PASSED] Blockchain Vocabulary and Resonance Matrix successfully verified.")

if __name__ == "__main__":
    test_vocabulary()
    test_resonance_fusion()
