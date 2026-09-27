"""
werracle.engine
===============
Standalone, Zero-Storage On-Chain AI Decision Engine.
Synchronized with WERR v0.5.1 Core Algorithm Specifications.
"""

from .core import (
    WerracleCoreEngine,
    compute_mandelbrot_patch,
    extract_quadrant_weights,
    extract_bounded_quadrant_weights,
    compute_boundary_correction_weights,
    apply_cadence_bifurcation,
    normal_cdf,
    sigmoid
)
from .defi_gates import (
    DeFiFlashLoanGate,
    AmmDynamicFeeGate,
    RegulatoryComplianceGate
)
from .domain_ontology import (
    OntologicalDomain,
    TELEMETRY_ENABLED
)
from .calibrated_oracle import (
    CalibratedWerracleOracle,
    float_to_fp,
    fp_to_float,
    fp_mul
)
from .blockchain_lexicon import (
    BlockchainVocabulary,
    BlockchainResonanceMatrix,
    BlockchainPillar
)
from .tripod_zmod9_oracle import (
    TripodZMod9Oracle,
    iterate_escape_zmod9
)
from .presets import (
    create_oracle_security_guard,
    create_oracle_smart_router,
    create_oracle_risk_evaluator,
    create_pure_fractal_reflex,
    create_tripod_zmod9_guardian
)

__all__ = [
    "WerracleCoreEngine",
    "compute_mandelbrot_patch",
    "extract_quadrant_weights",
    "extract_bounded_quadrant_weights",
    "compute_boundary_correction_weights",
    "apply_cadence_bifurcation",
    "normal_cdf",
    "sigmoid",
    "DeFiFlashLoanGate",
    "AmmDynamicFeeGate",
    "RegulatoryComplianceGate",
    "OntologicalDomain",
    "TELEMETRY_ENABLED",
    "CalibratedWerracleOracle",
    "float_to_fp",
    "fp_to_float",
    "fp_mul",
    "BlockchainVocabulary",
    "BlockchainResonanceMatrix",
    "BlockchainPillar",
    "TripodZMod9Oracle",
    "iterate_escape_zmod9",
    "create_oracle_security_guard",
    "create_oracle_smart_router",
    "create_oracle_risk_evaluator",
    "create_pure_fractal_reflex",
    "create_tripod_zmod9_guardian",
]
