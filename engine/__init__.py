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

__all__ = [
    "WerracleCoreEngine",
    "compute_mandelbrot_patch",
    "extract_quadrant_weights",
    "sigmoid",
    "DeFiFlashLoanGate",
    "AmmDynamicFeeGate",
    "RegulatoryComplianceGate",
]
