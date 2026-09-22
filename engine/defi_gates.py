"""
werracle.engine.defi_gates
==========================
Specialized Web3 & DeFi Domain Gates for On-Chain Risk, Optimization, and Compliance.
Provides programmatic triage for:
1. Flash-Loan & MEV Sandwich Attack Defense
2. AMM Volatility-Weighted Dynamic Fee Optimization
3. Regulatory & Anti-Money Laundering (AML) Compliance Triage
4. Spot-to-TWAP Oracle Manipulation Shield
"""

import math
from typing import Dict, Any, Tuple
from .core import WerracleCoreEngine


class DeFiFlashLoanGate:
    """
    Intra-Block Flash-Loan & Sandwich Attack Defense Gate.
    Evaluates borrow-to-reserve ratios, pool drain percentage, and atomic slippage.
    """
    def __init__(self, engine: WerracleCoreEngine = None):
        self.engine = engine or WerracleCoreEngine()

    def evaluate_transaction(
        self,
        borrow_amount: float,
        pool_liquidity: float,
        price_impact_pct: float,
        is_flash_loan: bool = False
    ) -> Dict[str, Any]:
        """
        Evaluates transaction risk.
        Returns:
            allowed (bool): True if transaction is safe to execute, False to REVERT.
            risk_signal (float): Computed risk metric [-2.0 .. +3.0].
            recommended_action (str): 'EXECUTE', 'WARN_SLIPPAGE', 'REVERT_FLASH_LOAN_ATTACK'.
        """
        borrow_ratio = (borrow_amount / pool_liquidity) if pool_liquidity > 0 else 1.0

        # Baseline risk
        risk = -1.2  # Default safe

        if is_flash_loan:
            risk += 1.0
        
        # Heavy liquidity drain (>20% of pool) is severe anomaly
        if borrow_ratio > 0.20:
            risk += (borrow_ratio - 0.20) * 8.0
        
        # Severe slippage (>3%) indicates possible sandwich attack
        if price_impact_pct > 3.0:
            risk += (price_impact_pct - 3.0) * 0.8

        decision = self.engine.decide_noul(risk_signal=risk, context_name="defi_flashloan")

        action = "EXECUTE"
        if not decision["allowed"]:
            action = "REVERT_FLASH_LOAN_ATTACK"
        elif price_impact_pct > 2.0:
            action = "WARN_SLIPPAGE"

        return {
            "allowed": decision["allowed"],
            "action": action,
            "risk_signal": round(risk, 4),
            "confidence_pct": round(decision["confidence"] * 100, 2),
            "borrow_ratio": round(borrow_ratio, 4)
        }


class AmmDynamicFeeGate:
    """
    Uniswap v4 Dynamic Fee Optimization Gate.
    Adjusts liquidity pool swap fee dynamically [0.05% to 0.50%] based on intra-block volatility.
    """
    def __init__(self, engine: WerracleCoreEngine = None):
        self.engine = engine or WerracleCoreEngine()

    def calculate_fee_pips(
        self,
        volatility_index: float,
        volume_imbalance_pct: float
    ) -> Dict[str, Any]:
        """
        Returns fee in pips (1 pip = 0.0001%, 500 pips = 0.05%, 5000 pips = 0.50%).
        """
        # Risk metric [-2.0 .. +2.0]
        risk = (volatility_index - 1.0) * 1.5 + (volume_imbalance_pct / 50.0)
        severity = self.engine.decide_score(risk_signal=risk, max_score=3)

        fee_schedule = {
            0: 500,   # 0.05% - Calm, deep liquidity
            1: 1500,  # 0.15% - Normal volume
            2: 3000,  # 0.30% - Elevated Volatility
            3: 5000   # 0.50% - Extreme Volatility / Defensive Mode
        }
        fee_pips = fee_schedule.get(severity, 5000)

        return {
            "fee_pips": fee_pips,
            "fee_pct": fee_pips / 10000.0,
            "severity_level": severity,
            "risk_metric": round(risk, 4)
        }


class RegulatoryComplianceGate:
    """
    Web3 Regulatory & Sanction Compliance Gate.
    Assesses wallet history, mixer interaction, and transaction frequency for AML/KYC triage.
    """
    def __init__(self, engine: WerracleCoreEngine = None):
        self.engine = engine or WerracleCoreEngine()

    def check_compliance(
        self,
        wallet_age_days: int,
        tx_frequency_per_minute: float,
        interacted_with_mixer: bool,
        is_sanction_flagged: bool = False
    ) -> Dict[str, Any]:
        """
        Evaluates regulatory compliance risk.
        Returns:
            status (str): 'APPROVED', 'MANUAL_REVIEW', 'BLOCKED_SANCTION'.
            compliance_tier (int): 0 (Clean) to 3 (Prohibited).
        """
        if is_sanction_flagged or interacted_with_mixer:
            risk = 3.0  # Immediate block
        else:
            risk = -1.5  # Clean
            if wallet_age_days < 7:
                risk += 1.0  # New wallet scrutiny
            if tx_frequency_per_minute > 30.0:
                risk += 1.5  # High frequency bot activity

        tier = self.engine.decide_score(risk_signal=risk, max_score=3)
        decision = self.engine.decide_noul(risk_signal=risk, context_name="regulatory_aml")

        status = "APPROVED"
        if tier >= 3 or not decision["allowed"]:
            status = "BLOCKED_SANCTION"
        elif tier == 2:
            status = "MANUAL_REVIEW"

        return {
            "status": status,
            "tier": tier,
            "allowed": decision["allowed"],
            "risk_signal": round(risk, 4),
            "confidence_pct": round(decision["confidence"] * 100, 2)
        }
