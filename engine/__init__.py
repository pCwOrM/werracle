"""
werracle.engine
===============
Standalone, Zero-Storage On-Chain AI Decision Engine.
"""

from .core import (
    WerracleCoreEngine,
    compute_mandelbrot_patch,
    extract_quadrant_weights,
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

__all__ = [
    "WerracleCoreEngine",
    "compute_mandelbrot_patch",
    "extract_quadrant_weights",
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
]
