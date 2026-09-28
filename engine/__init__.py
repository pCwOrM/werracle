"""
werracle.engine
===============
Standalone, Zero-Storage On-Chain AI Decision Engine.
Synchronized with WERR v0.5.1 Core Algorithm Specifications & Lean 4 GAP-0331 Z/9Z Invariants.
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
    iterate_escape_zmod9,
    is_zmod9_resonant_ideal,
    is_zmod9_coprime_unit,
    classify_zmod9_state,
    ZMOD9_RESONANT_IDEAL_I3,
    ZMOD9_COPRIME_UNIT_KERNEL,
    ZMOD9_UNIT_INVERSES
)
from .presets import (
    GOLDEN_PAIR_SEEDS,
    get_golden_pair_seed,
    create_golden_pair_oracle,
    create_golden_pair_tripod,
    create_oracle_security_guard,
    create_oracle_smart_router,
    create_oracle_risk_evaluator,
    create_pure_fractal_reflex,
    create_tripod_zmod9_guardian
)
from .living_cell import (
    WerracleLivingCell,
    LivingGenomeState,
    pack_living_genome,
    unpack_living_genome,
    verify_proof_of_horizon,
    evaluate_living_tripod,
    STATE_HIBERNATION,
    STATE_HOMEOSTASIS,
    STATE_HYPER_IMMUNE,
    STATE_PLASTICITY,
    STATE_NAMES,
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
    "is_zmod9_resonant_ideal",
    "is_zmod9_coprime_unit",
    "classify_zmod9_state",
    "ZMOD9_RESONANT_IDEAL_I3",
    "ZMOD9_COPRIME_UNIT_KERNEL",
    "ZMOD9_UNIT_INVERSES",
    "GOLDEN_PAIR_SEEDS",
    "get_golden_pair_seed",
    "create_golden_pair_oracle",
    "create_golden_pair_tripod",
    "create_oracle_security_guard",
    "create_oracle_smart_router",
    "create_oracle_risk_evaluator",
    "create_pure_fractal_reflex",
    "create_tripod_zmod9_guardian",
    "WerracleLivingCell",
    "LivingGenomeState",
    "pack_living_genome",
    "unpack_living_genome",
    "verify_proof_of_horizon",
    "evaluate_living_tripod",
    "STATE_HIBERNATION",
    "STATE_HOMEOSTASIS",
    "STATE_HYPER_IMMUNE",
    "STATE_PLASTICITY",
    "STATE_NAMES",
]

