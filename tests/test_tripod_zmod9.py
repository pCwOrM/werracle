"""
tests/test_tripod_zmod9.py
==========================
Verification of Multi-Scale Harmonic Tripod (Sparse 12-point) & Z mod 9 Modular Escape.
"""

import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from engine.tripod_zmod9_oracle import TripodZMod9Oracle, float_to_fp

def run_tests():
    print("=" * 70)
    print(" [PHASE 2 LAB] MULTI-SCALE HARMONIC TRIPOD & Z MOD 9 MODULAR VERIFICATION")
    print("=" * 70)

    oracle = TripodZMod9Oracle()

    # 1. Benchmarking raw speed across 1,000 evaluations
    print("\n[TEST 1] Latency Benchmark: 1,000 Sparse Tripod Evaluations...")
    cx_fp = float_to_fp(-0.743643887)
    cy_fp = float_to_fp(0.131825904)
    zoom_fp = float_to_fp(50.0)

    t0 = time.perf_counter()
    for _ in range(1000):
        oracle.evaluate_sparse_tripod(cx_fp, cy_fp, zoom_fp)
    total_time_ms = (time.perf_counter() - t0) * 1000.0
    avg_us = (total_time_ms / 1000.0) * 1000.0

    print(f"  1,000 Evaluations Time : {total_time_ms:.2f} ms")
    print(f"  Average Execution Time : {avg_us:.2f} microseconds per decision")
    assert avg_us < 200.0, f"Latency too high: {avg_us} us"
    print("  -> PASSED: Ultra-sub-millisecond latency confirmed.")

    # 2. End-to-End DeFi Decision Tests
    print("\n[TEST 2] End-to-End High-Fusion DeFi Triage Tests...")
    test_cases = [
        {
            "name": "Benign Retail Pool Swap",
            "text": "normal_swap in Uniswap v4 pool with clean_retail wallet and safe_health_factor",
            "expected_verdict": "PERMIT",
            "max_fee": 1500
        },
        {
            "name": "Moderate Arbitrage Flow",
            "text": "backrun_arbitrage capturing transient twap_drift with range_order_cross",
            "expected_verdict": "PERMIT",
            "max_fee": 3000
        },
        {
            "name": "Predatory Sandwich MEV Attack",
            "text": "mempool_snipe attempting predatory sandwich_frontrun with severe tick_velocity_spike and slippage_breach",
            "expected_verdict": "REVERT_CIRCUIT_BREAKER",
            "min_fee": 3500
        },
        {
            "name": "Catastrophic Uncollateralized Flash-Loan Attack",
            "text": "massive flashloan_burst with uncollateralized_borrow and pool_drain reserve_exhaustion reentrancy_probe",
            "expected_verdict": "REVERT_CIRCUIT_BREAKER",
            "min_fee": 4500
        },
        {
            "name": "Sanctioned Mixer Layering (AML Tier 3)",
            "text": "funds originating from sanctioned_mixer tornado_cash with ofac_sdn_cluster illicit_hop",
            "expected_verdict": "REVERT_CIRCUIT_BREAKER",
            "min_fee": 4500
        }
    ]

    for tc in test_cases:
        res = oracle.decide_transaction(tc["text"])
        print(f"\nScenario: {tc['name']}")
        print(f"  Verdict: {res['verdict']} (Permitted: {res['is_permitted']})")
        print(f"  Risk: {res['composite_risk']:.4f} | Dynamic Fee: {res['suggested_fee_pips']} pips ({res['suggested_fee_pips']/10000:.4f}%)")
        print(f"  Pillar: {res['dominant_pillar']} | Tokens: {res['matched_tokens']}")
        print(f"  Tripod Escapes (Wide, Focus, Deep): {res['tripod_diagnostics']['plane_escapes']}")
        print(f"  Z mod 9 Harmonics: {res['tesla_harmonics']}")

        assert res["verdict"] == tc["expected_verdict"], (
            f"Verdict mismatch: expected {tc['expected_verdict']}, got {res['verdict']}"
        )
        if "max_fee" in tc:
            assert res["suggested_fee_pips"] <= tc["max_fee"], (
                f"Fee too high: {res['suggested_fee_pips']} > {tc['max_fee']}"
            )
        if "min_fee" in tc:
            assert res["suggested_fee_pips"] >= tc["min_fee"], (
                f"Fee too low: {res['suggested_fee_pips']} < {tc['min_fee']}"
            )

    print("\n[ALL 5 DEFI SCENARIOS PERFECTLY CLASSIFIED]")

if __name__ == "__main__":
    run_tests()
