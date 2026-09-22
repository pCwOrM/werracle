"""
werracle.sim.defi_flashloan_sim
===============================
Complete Local DeFi Flash-Loan & Volatility Defense Simulator.
Demonstrates Werracle's sub-millisecond intra-block atomic protection
and dynamic fee optimization without any external dependencies.
"""

import sys
import os

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Ensure werracle is in sys.path
_SIM_DIR = os.path.dirname(os.path.abspath(__file__))
_WERRACLE_DIR = os.path.dirname(_SIM_DIR)
if _WERRACLE_DIR not in sys.path:
    sys.path.insert(0, _WERRACLE_DIR)

from engine.defi_gates import (
    DeFiFlashLoanGate,
    AmmDynamicFeeGate,
    RegulatoryComplianceGate
)


def run_defi_simulation():
    print("\n" + "=" * 70)
    print(" 🛡️  WERRACLE ON-CHAIN DEFI & COMPLIANCE DEFENSE SIMULATOR")
    print("=" * 70)

    flashloan_gate = DeFiFlashLoanGate()
    fee_gate = AmmDynamicFeeGate()
    compliance_gate = RegulatoryComplianceGate()

    # --- Scenario 1: Flash-Loan & MEV Attack Simulation ---
    print("\n[1] FLASH-LOAN & SANDWICH ATTACK TRIAGE (Pool Liquidity = 10,000 ETH):")
    print("-" * 70)
    print(f"{'TX TYPE':<24} | {'BORROW':<10} | {'SLIPPAGE':<10} | {'DECISION':<10} | {'ACTION'}")
    print("-" * 70)

    scenarios = [
        {"name": "Standard User Swap",    "amount": 5.0,     "slippage": 0.08, "is_flash": False},
        {"name": "Whale Swap (Moderate)", "amount": 450.0,   "slippage": 1.20, "is_flash": False},
        {"name": "Sandwich Attack (MEV)", "amount": 1800.0,  "slippage": 4.50, "is_flash": False},
        {"name": "Hostile Flash-Loan",    "amount": 5500.0,  "slippage": 14.8, "is_flash": True},
        {"name": "Critical Exploit Drain","amount": 9200.0,  "slippage": 38.0, "is_flash": True},
    ]

    for sc in scenarios:
        res = flashloan_gate.evaluate_transaction(
            borrow_amount=sc["amount"],
            pool_liquidity=10000.0,
            price_impact_pct=sc["slippage"],
            is_flash_loan=sc["is_flash"]
        )
        dec_str = "ALLOWED" if res["allowed"] else "DENIED"
        print(f"{sc['name']:<24} | {sc['amount']:<6} ETH | {sc['slippage']:<5}%    | {dec_str:<10} | {res['action']}")

    # --- Scenario 2: Uniswap v4 Dynamic Fee Hook ---
    print("\n\n[2] UNISWAP v4 DYNAMIC FEE HOOK ADAPTATION:")
    print("-" * 70)
    print(f"{'MARKET CONDITION':<25} | {'VOLATILITY':<12} | {'IMBALANCE':<12} | {'FEE RATE'}")
    print("-" * 70)

    vol_scenarios = [
        {"name": "Deep Liquidity / Calm", "vol": 0.8, "imb": 2.0},
        {"name": "Normal Trading Day",    "vol": 1.2, "imb": 12.0},
        {"name": "Elevated Turbulence",   "vol": 2.1, "imb": 35.0},
        {"name": "Extreme Flash Crash",   "vol": 3.8, "imb": 78.0},
    ]

    for vs in vol_scenarios:
        fee_res = fee_gate.calculate_fee_pips(vs["vol"], vs["imb"])
        print(f"{vs['name']:<25} | {vs['vol']:<12} | {vs['imb']:<5}%       | {fee_res['fee_pct']:.2f}% ({fee_res['fee_pips']} pips)")

    # --- Scenario 3: Web3 Regulatory & AML Compliance ---
    print("\n\n[3] REGULATORY COMPLIANCE & AML FILTERING:")
    print("-" * 70)
    print(f"{'WALLET CATEGORY':<25} | {'AGE (DAYS)':<12} | {'TX/MIN':<8} | {'STATUS':<16} | {'TIER'}")
    print("-" * 70)

    wallets = [
        {"name": "Verified Protocol Treasury", "age": 820, "freq": 0.2, "mixer": False, "sanction": False},
        {"name": "Regular Active Retailer",    "age": 140, "freq": 1.5, "mixer": False, "sanction": False},
        {"name": "Brand New Suspicious Bot",   "age": 2,   "freq": 45.0,"mixer": False, "sanction": False},
        {"name": "Tornado Cash Interactor",    "age": 95,  "freq": 4.0, "mixer": True,  "sanction": False},
        {"name": "OFAC Sanctioned Entity",     "age": 410, "freq": 0.1, "mixer": False, "sanction": True},
    ]

    for w in wallets:
        comp_res = compliance_gate.check_compliance(
            wallet_age_days=w["age"],
            tx_frequency_per_minute=w["freq"],
            interacted_with_mixer=w["mixer"],
            is_sanction_flagged=w["sanction"]
        )
        print(f"{w['name']:<25} | {w['age']:<12} | {w['freq']:<8} | {comp_res['status']:<16} | Tier {comp_res['tier']}")

    print("\n" + "=" * 70)
    print(" [OK] ALL DEFI DEFENSE & REGULATORY SIMULATIONS COMPLETED SUCCESSFULLY")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    run_defi_simulation()
