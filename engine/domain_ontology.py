"""
werracle.engine.domain_ontology
===============================
Ontological Domain Lexicon and Semantic Category Classifier for Werracle.
Provides zero-parameter deterministic taxonomic mapping for Web3, DeFi,
Risk Assessment, and Extensible Domain Ontologies.

Zero VRAM, Zero Floating-Point Neural Tensors, 100% Deterministic.
Telemetry: Permanently DISABLED (Privacy-Preserving On-Chain Invariant).
"""

import re
import hashlib
from typing import Dict, List, Tuple, Any, Optional

# Strict Invariant: Werracle operates with ZERO external telemetry
TELEMETRY_ENABLED: bool = False
ALLOW_EXTERNAL_TRACKING: bool = False


class OntologicalDomain:
    """
    Hierarchical Ontological Taxonomy and Vocabulary for Autonomous Decision Oracles.
    """

    # 1. Web3 / DeFi Transaction Intent Taxonomy
    TRANSACTION_INTENTS = {
        "FLASH_LOAN": {
            "keywords": ["flashloan", "flash_loan", "uncollateralized", "borrow_instant", "atomic_borrow"],
            "base_risk": 0.85,
            "category": "capital_intensive"
        },
        "MEV_ARBITRAGE": {
            "keywords": ["sandwich", "frontrun", "backrun", "bundle_mev", "priority_gas", "mempool_snipe"],
            "base_risk": 0.70,
            "category": "market_order"
        },
        "DYNAMIC_SWAP": {
            "keywords": ["swap", "exact_input", "exact_output", "amm_trade", "pool_exchange", "trade"],
            "base_risk": 0.15,
            "category": "standard_liquidity"
        },
        "COLLATERAL_DEPOSIT": {
            "keywords": ["deposit", "supply", "stake", "mint_lp", "add_liquidity", "collateralize"],
            "base_risk": 0.05,
            "category": "liquidity_provision"
        },
        "COLLATERAL_WITHDRAWAL": {
            "keywords": ["withdraw", "redeem", "unstake", "remove_liquidity", "burn_lp", "decollateralize"],
            "base_risk": 0.35,
            "category": "capital_exit"
        },
        "LIQUIDATION_CALL": {
            "keywords": ["liquidate", "seize", "undercollateralized", "health_factor_breach", "margin_call"],
            "base_risk": 0.50,
            "category": "solvency_enforcement"
        },
        "GOVERNANCE_EXECUTION": {
            "keywords": ["propose", "vote", "queue_timelock", "execute_timelock", "upgrade_proxy"],
            "base_risk": 0.40,
            "category": "governance"
        },
        "EMERGENCY_HALT": {
            "keywords": ["pause", "emergency_stop", "freeze_vault", "circuit_breaker", "halt_trading"],
            "base_risk": 0.95,
            "category": "safety_critical"
        }
    }

    # 2. Risk & Threat Topology Taxonomy
    RISK_SIGNATURES = {
        "EXCESSIVE_SLIPPAGE": {
            "pattern": r"\b(slippage\s*>\s*[0-9]+|high_slippage|price_impact_extreme)\b",
            "threat_weight": 0.60
        },
        "RESERVE_DEPLETION": {
            "pattern": r"\b(pool_drain|reserve_exhaustion|drain_liquidity|liquidity_dump)\b",
            "threat_weight": 0.85
        },
        "REENTRANCY_SIGNATURE": {
            "pattern": r"\b(cross_function_reentrancy|recursive_call|reentrant_hook|fallback_loop)\b",
            "threat_weight": 0.95
        },
        "SANCTION_EXPOSURE": {
            "pattern": r"\b(ofac_sdn|tornado_cash|mixer_tainted|sanctioned_entity|illicit_cluster)\b",
            "threat_weight": 0.99
        },
        "SYBIL_SWARM": {
            "pattern": r"\b(high_frequency_burst|bot_swarm|rapid_micro_tx|nonce_flooding)\b",
            "threat_weight": 0.55
        }
    }

    # 3. Regulatory AML Tiering Taxonomy
    AML_TIERS = {
        0: {"name": "CLEAN_TIER_0", "threshold": 0.20, "action": "PERMIT"},
        1: {"name": "RETAIL_TIER_1", "threshold": 0.45, "action": "PERMIT_WITH_FEE"},
        2: {"name": "SUSPICIOUS_TIER_2", "threshold": 0.75, "action": "WARN_AND_RATE_LIMIT"},
        3: {"name": "CRITICAL_TIER_3", "threshold": 1.00, "action": "REVERT_SANCTION"}
    }

    # 4. Extensible Domain Lexicon (Biomedical / General Ontology Adapter)
    EXTENSIBLE_ONTOLOGY = {
        "ONCOLOGY_BIOMARKER": {
            "keywords": ["her2", "egfr", "kras", "brca1", "p53", "carcinoma", "neoplasm", "metastasis"],
            "domain": "biomedical_triaging"
        },
        "GENOMIC_VARIANT": {
            "keywords": ["missense", "nonsense", "frameshift", "pathogenic", "benign", "conservation"],
            "domain": "genomics_variant_impact"
        }
    }

    @classmethod
    def classify_intent(cls, prompt_or_data: str) -> Dict[str, Any]:
        """
        Classifies transaction intent using strict word-boundary matching.
        Returns: { 'intent': str, 'base_risk': float, 'category': str, 'matched_tokens': List[str] }
        """
        text = prompt_or_data.lower()
        best_intent = "DYNAMIC_SWAP"
        max_matches = 0
        matched_tokens = []
        highest_risk = 0.15
        selected_category = "standard_liquidity"

        for intent_name, data in cls.TRANSACTION_INTENTS.items():
            matches = []
            for kw in data["keywords"]:
                pattern = r"\b" + re.escape(kw) + r"\b"
                if re.search(pattern, text):
                    matches.append(kw)
            if len(matches) > max_matches:
                max_matches = len(matches)
                best_intent = intent_name
                highest_risk = data["base_risk"]
                selected_category = data["category"]
                matched_tokens = matches

        return {
            "intent": best_intent,
            "base_risk": highest_risk,
            "category": selected_category,
            "matched_tokens": matched_tokens
        }

    @classmethod
    def evaluate_risk_signatures(cls, text: str) -> Tuple[float, List[str]]:
        """
        Scans input for known exploit signatures and threat topology.
        Returns: (aggregate_threat_score: float, detected_threats: List[str])
        """
        t_lower = text.lower()
        threat_score = 0.0
        detected = []

        for sig_name, sig_data in cls.RISK_SIGNATURES.items():
            if re.search(sig_data["pattern"], t_lower):
                detected.append(sig_name)
                threat_score += sig_data["threat_weight"]

        # Cap aggregate threat score at 1.0
        return min(1.0, threat_score), detected

    @classmethod
    def derive_ontological_seed(
        cls,
        base_cx: float,
        base_cy: float,
        base_zoom: float,
        intent_data: Dict[str, Any],
        threat_score: float
    ) -> Tuple[float, float, float]:
        """
        Synthesizes a deterministic Mandelbrot coordinate perturbation from ontological features.
        Zero parameters stored in VRAM. Pure mathematical projection.
        """
        # Semantic hash from intent name and matched tokens
        seed_str = f"{intent_data['intent']}:{threat_score:.4f}"
        h = int(hashlib.sha256(seed_str.encode('utf-8')).hexdigest()[:8], 16)
        
        # Micro-perturbation scaled by zoom to ensure boundary stability
        scale = 0.05 / max(1.0, base_zoom)
        dx = ((h & 0xFFFF) / 65535.0 - 0.5) * scale
        dy = (((h >> 16) & 0xFFFF) / 65535.0 - 0.5) * scale
        
        # Risk shifts coordinate deeper towards Julia filaments
        risk_shift = threat_score * 0.02 / max(1.0, base_zoom)
        
        target_cx = base_cx + dx + risk_shift
        target_cy = base_cy + dy - risk_shift
        target_zoom = base_zoom * (1.0 + threat_score * 0.5)

        return target_cx, target_cy, target_zoom
