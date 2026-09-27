"""
werracle.engine.presets
=======================
Pre-calibrated Oracle and Reflex Gate presets aligned with WERR Core v0.5.1 specifications.
Optimized for on-chain decision gates, Uniswap v4 dynamic fee hooks, and EVM gas efficiency.

Zero VRAM, Zero Weights, 100% Deterministic execution.
Privacy: Telemetry is PERMANENTLY DISABLED.
"""

from .calibrated_oracle import CalibratedWerracleOracle
from .tripod_zmod9_oracle import TripodZMod9Oracle
from .core import WerracleCoreEngine


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
