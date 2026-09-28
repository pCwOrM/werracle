"""
werracle.engine.presets
=======================
Pre-calibrated Oracle and Reflex Gate presets aligned with WERR Core v0.5.1 specifications
and 40-Core Dual Xeon Mined Golden Coordinate Seeds (v2.1).
Optimized for on-chain decision gates, Uniswap v4 dynamic fee hooks, and EVM gas efficiency.

Zero VRAM, Zero Weights, 100% Deterministic execution.
Privacy: Telemetry is PERMANENTLY DISABLED.
"""

from typing import Dict, Any
from .calibrated_oracle import CalibratedWerracleOracle
from .tripod_zmod9_oracle import TripodZMod9Oracle
from .core import WerracleCoreEngine


# 40-Core Dual Xeon Mined Golden Coordinates (Q16.16 & Float) across 6 DeFi / Web3 Pools
GOLDEN_PAIR_SEEDS: Dict[str, Dict[str, Any]] = {
    "ETH/USDC": {
        "cx": -1.420000,
        "cy": 0.220000,
        "zoom": 45.0,
        "cx_q16": -93061,
        "cy_q16": 14417,
        "zoom_q16": 2949120,
        "region": "Myrberg-Feigenbaum Horizon",
        "zmod9_class": "K_ERROR_COPRIME_UNIT",
        "tripod_boundedness_bps": 6111,
        "lvr_protection_pct": 49.89,
        "sensitivity_ratio": 5.48,
    },
    "WBTC/USDC": {
        "cx": 0.360000,
        "cy": 0.680000,
        "zoom": 8.0,
        "cx_q16": 23592,
        "cy_q16": 44564,
        "zoom_q16": 524288,
        "region": "Observer Horizon North",
        "zmod9_class": "I3_RESONANT_IDEAL",
        "tripod_boundedness_bps": 6874,
        "lvr_protection_pct": 46.06,
        "sensitivity_ratio": 5.13,
    },
    "UNI/ETH": {
        "cx": -1.420000,
        "cy": 0.163333,
        "zoom": 45.0,
        "cx_q16": -93061,
        "cy_q16": 10704,
        "zoom_q16": 2949120,
        "region": "Myrberg-Feigenbaum Horizon",
        "zmod9_class": "I3_RESONANT_IDEAL",
        "tripod_boundedness_bps": 8194,
        "lvr_protection_pct": 53.72,
        "sensitivity_ratio": 5.81,
    },
    "ARB/USDC": {
        "cx": -1.420000,
        "cy": 0.220000,
        "zoom": 45.0,
        "cx_q16": -93061,
        "cy_q16": 14417,
        "zoom_q16": 2949120,
        "region": "Myrberg-Feigenbaum Horizon",
        "zmod9_class": "K_ERROR_COPRIME_UNIT",
        "tripod_boundedness_bps": 6111,
        "lvr_protection_pct": 50.56,
        "sensitivity_ratio": 5.55,
    },
    "SOL/USDC": {
        "cx": 0.334286,
        "cy": 0.680000,
        "zoom": 12.0,
        "cx_q16": 21907,
        "cy_q16": 44564,
        "zoom_q16": 786432,
        "region": "Observer Horizon North",
        "zmod9_class": "K_ERROR_COPRIME_UNIT",
        "tripod_boundedness_bps": 7291,
        "lvr_protection_pct": 57.83,
        "sensitivity_ratio": 6.14,
    },
    "AAVE/ETH": {
        "cx": 0.308571,
        "cy": 0.680000,
        "zoom": 25.0,
        "cx_q16": 20222,
        "cy_q16": 44564,
        "zoom_q16": 1638400,
        "region": "Observer Horizon North",
        "zmod9_class": "K_ERROR_COPRIME_UNIT",
        "tripod_boundedness_bps": 8402,
        "lvr_protection_pct": 55.11,
        "sensitivity_ratio": 5.95,
    },
}


def get_golden_pair_seed(pair_name: str) -> Dict[str, Any]:
    """
    Returns the 40-Core Dual Xeon Mined Golden Seed metadata for the given DeFi pool.
    Normalizes separators (e.g. 'ETH-USDC', 'eth_usdc', 'ETH/USDC').
    """
    norm = pair_name.strip().upper().replace("-", "/").replace("_", "/")
    if norm not in GOLDEN_PAIR_SEEDS:
        raise KeyError(f"Unknown pool pair '{pair_name}'. Available pools: {list(GOLDEN_PAIR_SEEDS.keys())}")
    return dict(GOLDEN_PAIR_SEEDS[norm])


def create_golden_pair_oracle(
    pair_name: str = "ETH/USDC",
    resolution: int = 36,
    max_iter: int = 36,
    enable_domain: bool = True,
    enable_lexical: bool = True,
    enable_resonance: bool = True,
) -> CalibratedWerracleOracle:
    """
    Instantiates a CalibratedWerracleOracle initialized at the 40-Core Mined Golden Seed
    for the specified liquidity pool (`ETH/USDC`, `WBTC/USDC`, `UNI/ETH`, `ARB/USDC`, `SOL/USDC`, `AAVE/ETH`).
    """
    seed = get_golden_pair_seed(pair_name)
    return CalibratedWerracleOracle(
        base_cx=seed["cx"],
        base_cy=seed["cy"],
        base_zoom=seed["zoom"],
        resolution=resolution,
        max_iter=max_iter,
        enable_domain=enable_domain,
        enable_lexical=enable_lexical,
        enable_resonance=enable_resonance,
        cadence_lambda=0.10,
        cadence_beta=0.15,
        cadence_alpha=0.50,
        temp_choice=1.25,
    )


def create_golden_pair_tripod(
    pair_name: str = "ETH/USDC",
    decision_threshold: float = 0.50,
    enable_lexical: bool = True,
    enable_resonance: bool = True,
) -> TripodZMod9Oracle:
    """
    Instantiates a TripodZMod9Oracle initialized at the 40-Core Mined Golden Seed
    for the specified liquidity pool (`ETH/USDC`, `WBTC/USDC`, `UNI/ETH`, `ARB/USDC`, `SOL/USDC`, `AAVE/ETH`).
    """
    seed = get_golden_pair_seed(pair_name)
    return TripodZMod9Oracle(
        base_cx=seed["cx"],
        base_cy=seed["cy"],
        base_zoom=seed["zoom"],
        decision_threshold=decision_threshold,
        enable_lexical=enable_lexical,
        enable_resonance=enable_resonance,
    )


def create_oracle_security_guard(
    resolution: int = 36,
    max_iter: int = 36
) -> CalibratedWerracleOracle:
    """
    Pre-calibrated Security & Exploit Defense Oracle Gate.
    Optimal for Flash-Loan attacks, MEV frontrunning prevention, and atomic circuit breakers.
    Coordinates: Deep filament cusp in Seahorse Valley (cx=-0.74364..., cy=0.13182..., zoom=120.0).
    """
    return CalibratedWerracleOracle(
        base_cx=-0.7436438870371587,
        base_cy=0.1318259042053119,
        base_zoom=120.0,
        resolution=resolution,
        max_iter=max_iter,
        mode="hybrid",
        domain_mode="multi",
        enable_domain=True,
        enable_lexical=True,
        enable_resonance=True,
        cadence_lambda=0.10,
        cadence_beta=0.15,
        cadence_alpha=0.50,
        temp_choice=1.25
    )


def create_oracle_smart_router(
    resolution: int = 36,
    max_iter: int = 36
) -> CalibratedWerracleOracle:
    """
    Pre-calibrated DEX & AMM Smart Routing Oracle.
    Optimal for multi-hop liquidity routing, tick slippage estimation, and dynamic fee adjustment.
    Coordinates: High-curvature boundary filament (cx=-0.10109..., cy=0.95628..., zoom=45.0).
    """
    return CalibratedWerracleOracle(
        base_cx=-0.10109636384562,
        base_cy=0.95628651080914,
        base_zoom=45.0,
        resolution=resolution,
        max_iter=max_iter,
        mode="hybrid",
        domain_mode="multi",
        enable_domain=True,
        enable_lexical=True,
        enable_resonance=True,
        cadence_lambda=0.10,
        cadence_beta=0.15,
        cadence_alpha=0.50,
        temp_choice=1.25
    )


def create_oracle_risk_evaluator(
    resolution: int = 36,
    max_iter: int = 36
) -> CalibratedWerracleOracle:
    """
    Pre-calibrated Lending, Solvency & Regulatory AML Risk Evaluator.
    Optimal for loan health factor monitoring, liquidation cascades, and OFAC/sanctions classification.
    Coordinates: Boundary cusp valley (cx=-0.75, cy=0.1, zoom=25.0).
    """
    return CalibratedWerracleOracle(
        base_cx=-0.75,
        base_cy=0.1,
        base_zoom=25.0,
        resolution=resolution,
        max_iter=max_iter,
        mode="hybrid",
        domain_mode="multi",
        enable_domain=True,
        enable_lexical=True,
        enable_resonance=True,
        cadence_lambda=0.10,
        cadence_beta=0.15,
        cadence_alpha=0.50,
        temp_choice=1.25
    )


def create_pure_fractal_reflex(
    resolution: int = 32,
    max_iter: int = 30
) -> CalibratedWerracleOracle:
    """
    Pure Fractal Universal Cusp Reflex Gate [0, 0, 0].
    Domainless baseline: zero semantic dictionary dependencies, 100% collision-free determinism.
    Auto-guarded against uncalibrated coordinate shifts.
    """
    return CalibratedWerracleOracle(
        base_cx=-0.7436438870371587,
        base_cy=0.13182590420531197,
        base_zoom=50.0,
        resolution=resolution,
        max_iter=max_iter,
        mode="pure_fractal",
        domain_mode="none",
        enable_domain=False,
        enable_lexical=False,
        enable_resonance=False,
        cadence_lambda=0.10,
        cadence_beta=0.15,
        cadence_alpha=0.50,
        temp_choice=1.25
    )


def create_tripod_zmod9_guardian(
    decision_threshold: float = 0.50
) -> TripodZMod9Oracle:
    """
    Sparse Multi-Scale Harmonic Tripod Oracle (Phase 2 Candidate).
    Evaluates 12 sparse cardinal points across 3 zoom planes (0.60x, 1.00x, 1.60x)
    with Z mod 9 Lean 4 harmonic escape recurrence and Tesla 3-6-9 resonance coupling.
    """
    return TripodZMod9Oracle(
        base_cx=-0.7436438870371587,
        base_cy=0.13182590420531197,
        base_zoom=50.0,
        decision_threshold=decision_threshold,
        enable_lexical=True,
        enable_resonance=True
    )
