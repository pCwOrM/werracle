"""
werracle.engine.blockchain_lexicon
==================================
High-Fusion Blockchain Semantic Vocabulary & Fractal Resonance Dictionary.

Provides:
1. BlockchainVocabulary: 40+ domain-specific on-chain semantic tokens classified
   into 5 ontological pillars (AMM Dynamics, MEV/Attacks, Solvency, Regulatory, Governance).
2. BlockchainResonanceDictionary: High-order fractal resonance matrix mapping
   semantic tokens to orthogonal phase angles, Tesla 3-6-9 harmonic frequencies,
   and Q16.16 coordinate displacements (delta_cx, delta_cy).
3. High-Order Superposition Fusion: Deterministic vector wave interference
   synthesizing perturbed Mandelbrot seeds without neural weights or external storage.

Privacy: Telemetry is PERMANENTLY DISABLED (TELEMETRY_ENABLED = False).
"""

import math
import re
from enum import Enum
from typing import Dict, List, Tuple, Any, Optional

# Strict Invariant: Zero Telemetry
TELEMETRY_ENABLED: bool = False

FP_SHIFT = 16
FP_ONE = 1 << FP_SHIFT


def float_to_fp(val: float) -> int:
    return int(round(val * FP_ONE))


def fp_to_float(fp: int) -> float:
    return float(fp) / FP_ONE


def fp_mul(a: int, b: int) -> int:
    return (a * b) >> FP_SHIFT


class BlockchainPillar(Enum):
    AMM_LIQUIDITY = "AMM_LIQUIDITY"     # Orderbook, ticks, reserves, LVR
    MEV_ATTACK = "MEV_ATTACK"           # Flash-loans, sandwiches, snipes, frontrunning
    SOLVENCY = "SOLVENCY"               # Undercollateralization, liquidations, health factor
    REGULATORY_AML = "REGULATORY_AML"   # Sanctions, mixers, Sybil clustering, illicit flow
    GOVERNANCE = "GOVERNANCE"           # Circuit breakers, timelocks, pause guards


class SemanticToken:
    """Represents a single semantic token in the Blockchain Vocabulary."""
    def __init__(
        self,
        token_id: int,
        name: str,
        pillar: BlockchainPillar,
        patterns: List[str],
        base_severity: float,
        tesla_harmonic: int,  # 3, 6, or 9
        description: str
    ):
        self.token_id = token_id
        self.name = name
        self.pillar = pillar
        self.patterns = patterns
        self.compiled_regex = [re.compile(p, re.IGNORECASE) for p in patterns]
        self.base_severity = max(0.0, min(1.0, base_severity))
        self.tesla_harmonic = tesla_harmonic if tesla_harmonic in (3, 6, 9) else 3
        self.description = description

        # Orthogonal Phase Angle in radians [0, 2*pi)
        # 40 tokens evenly distributed across unit circle
        self.phase_angle = (2.0 * math.pi * token_id) / 40.0

        # Fractal Coordinate Displacement Vector (base amplitude 0.04)
        # Scaled by severity and harmonic resonance
        amp = 0.04 * (0.5 + 0.5 * self.base_severity)
        self.delta_cx = amp * math.cos(self.phase_angle)
        self.delta_cy = amp * math.sin(self.phase_angle)

        # Fixed-point Q16.16 precomputations
        self.delta_cx_fp = float_to_fp(self.delta_cx)
        self.delta_cy_fp = float_to_fp(self.delta_cy)
        self.severity_fp = float_to_fp(self.base_severity)


class BlockchainVocabulary:
    """Authoritative Lexical Ontology for EVM & DeFi Transactions."""

    _TOKENS: Dict[str, SemanticToken] = {}
    _TOKEN_LIST: List[SemanticToken] = []

    @classmethod
    def _register(cls, token: SemanticToken):
        cls._TOKENS[token.name] = token
        cls._TOKEN_LIST.append(token)

    @classmethod
    def get_token(cls, name: str) -> Optional[SemanticToken]:
        return cls._TOKENS.get(name)

    @classmethod
    def all_tokens(cls) -> List[SemanticToken]:
        return cls._TOKEN_LIST


# Initialize the 40 Semantic Tokens across 5 Pillars
_RAW_DEFINITIONS = [
    # -------------------------------------------------------------
    # Pillar 1: AMM & Liquidity Dynamics (Token IDs 0 - 7)
    # -------------------------------------------------------------
    (0, "LIQUIDITY_IMBALANCE", BlockchainPillar.AMM_LIQUIDITY,
     [r"\bliquidity_imbalance\b", r"\bpool_skew\b", r"\bunbalanced_ratio\b"],
     0.45, 3, "Severe ratio asymmetry between token0 and token1 reserves"),

    (1, "TICK_VELOCITY_SPIKE", BlockchainPillar.AMM_LIQUIDITY,
     [r"\btick_velocity\b", r"\brapid_tick_cross\b", r"\btick_spike\b"],
     0.60, 6, "Extreme rate of tick traversal per second in concentrated AMM"),

    (2, "SLIPPAGE_BREACH", BlockchainPillar.AMM_LIQUIDITY,
     [r"\bslippage_breach\b", r"\bexcessive_slippage\b", r"\bprice_impact_limit\b"],
     0.70, 6, "Swap execution price impact exceeds safe pool tolerance"),

    (3, "RESERVE_EXHAUSTION", BlockchainPillar.AMM_LIQUIDITY,
     [r"\breserve_exhaustion\b", r"\bpool_drain\b", r"\bdepleted_reserve\b"],
     0.85, 9, "Imminent total drain of one side of pool liquidity"),

    (4, "LVR_LEAKAGE", BlockchainPillar.AMM_LIQUIDITY,
     [r"\blvr_leakage\b", r"\bloss_versus_rebalancing\b", r"\barbitrage_loss\b"],
     0.55, 6, "Toxic orderflow extracting value from passive liquidity providers"),

    (5, "STALE_POOL_PRICE", BlockchainPillar.AMM_LIQUIDITY,
     [r"\bstale_price\b", r"\blatent_pool_feed\b", r"\blagging_tick\b"],
     0.50, 3, "AMM spot price lagging behind external consolidated reference"),

    (6, "DEPTH_SHOCK", BlockchainPillar.AMM_LIQUIDITY,
     [r"\bdepth_shock\b", r"\bliquidity_pull\b", r"\bflash_liquidity_drop\b"],
     0.75, 9, "Sudden evaporation of active tick ranges around current price"),

    (7, "RANGE_ORDER_CROSS", BlockchainPillar.AMM_LIQUIDITY,
     [r"\brange_order_cross\b", r"\blimit_order_fill\b", r"\bconcentrated_fill\b"],
     0.25, 3, "Standard order crossing narrow liquidity band"),

    # -------------------------------------------------------------
    # Pillar 2: MEV & Attack Vectors (Token IDs 8 - 15)
    # -------------------------------------------------------------
    (8, "FLASHLOAN_BURST", BlockchainPillar.MEV_ATTACK,
     [r"\bflashloan_burst\b", r"\buncollateralized_borrow\b", r"\batomic_loan\b", r"\bflash_loan\b"],
     0.90, 9, "Large uncollateralized atomic borrow within a single block transaction"),

    (9, "SANDWICH_FRONTRUN", BlockchainPillar.MEV_ATTACK,
     [r"\bsandwich\b", r"\bfrontrun\b", r"\bpredatory_sandwich\b"],
     0.80, 9, "Coordinated transaction pair sandwiching victim swap in mempool"),

    (10, "MEMPOOL_SNIPE", BlockchainPillar.MEV_ATTACK,
     [r"\bmempool_snipe\b", r"\bgas_bribe\b", r"\bpriority_snipe\b"],
     0.65, 6, "Aggressive priority fee manipulation to reorder pending block execution"),

    (11, "BACKRUN_ARBITRAGE", BlockchainPillar.MEV_ATTACK,
     [r"\bbackrun\b", r"\barbitrage_backrun\b", r"\batomic_arbitrage\b"],
     0.40, 3, "Benign or market-clearing atomic backrun capturing price discrepancy"),

    (12, "REENTRANCY_PROBE", BlockchainPillar.MEV_ATTACK,
     [r"\breentrancy_probe\b", r"\brecursive_hook_call\b", r"\bfallback_cycle\b"],
     0.95, 9, "Suspicious repeated callback invocation before external state finalization"),

    (13, "JIT_LIQUIDITY_DRAIN", BlockchainPillar.MEV_ATTACK,
     [r"\bjit_liquidity\b", r"\bjust_in_time_mev\b", r"\btick_sandwich\b"],
     0.60, 6, "Single-block liquidity insertion and withdrawal frontrunning swap"),

    (14, "UNCOLLATERALIZED_SPEC", BlockchainPillar.MEV_ATTACK,
     [r"\buncollateralized_spec\b", r"\binstant_mint_exploit\b"],
     0.88, 9, "Capital synthesis exploit exploiting transient accounting invariants"),

    (15, "ORACLE_MANIPULATION", BlockchainPillar.MEV_ATTACK,
     [r"\boracle_manipulation\b", r"\bspot_manipulation\b", r"\btwap_distortion\b"],
     0.92, 9, "Artificial temporary skewing of AMM spot price to exploit dependent lending"),

    # -------------------------------------------------------------
    # Pillar 3: Solvency & Collateralization (Token IDs 16 - 23)
    # -------------------------------------------------------------
    (16, "UNDERCOLLATERALIZED_LOAN", BlockchainPillar.SOLVENCY,
     [r"\bundercollateralized\b", r"\bbreached_margin\b", r"\binsolvent_position\b"],
     0.85, 9, "Borrower debt exceeding protocol-mandated liquidation threshold"),

    (17, "HEALTH_FACTOR_BREACH", BlockchainPillar.SOLVENCY,
     [r"\bhealth_factor_breach\b", r"\bhf\s*<\s*1\.0\b", r"\bhealth_factor_low\b"],
     0.80, 9, "Collateral to debt ratio falling below 1.0 critical parity"),

    (18, "LIQUIDATION_CASCADE", BlockchainPillar.SOLVENCY,
     [r"\bliquidation_cascade\b", r"\bcascade_dump\b", r"\bchain_liquidation\b"],
     0.90, 9, "Self-reinforcing series of automated liquidations depleting buy depth"),

    (19, "ORACLE_DIVERGENCE", BlockchainPillar.SOLVENCY,
     [r"\boracle_divergence\b", r"\bfeed_mismatch\b", r"\bchainlink_divergence\b"],
     0.75, 6, "Significant discrepancy between on-chain AMM and off-chain index feeds"),

    (20, "BAD_DEBT_ACCUMULATION", BlockchainPillar.SOLVENCY,
     [r"\bbad_debt\b", r"\bshortfall_event\b", r"\bprotocol_deficit\b"],
     0.85, 9, "Unrecoverable debt left in pool following underwater liquidation failure"),

    (21, "TWAP_SPOT_DRIFT", BlockchainPillar.SOLVENCY,
     [r"\btwap_drift\b", r"\bspot_twap_spread\b", r"\bdrift_exceeded\b"],
     0.50, 3, "Spread between geometric mean TWAP and instantaneous spot price"),

    (22, "COLLATERAL_HAIRCUT", BlockchainPillar.SOLVENCY,
     [r"\bcollateral_haircut\b", r"\bltv_reduction\b", r"\brisk_discount\b"],
     0.40, 3, "Protocol risk engine discounting high-beta collateral asset value"),

    (23, "SOLVENCY_HEALTHY", BlockchainPillar.SOLVENCY,
     [r"\bsolvency_healthy\b", r"\bovercollateralized\b", r"\bsafe_health_factor\b"],
     0.05, 3, "High-margin overcollateralized position in optimal standing"),

    # -------------------------------------------------------------
    # Pillar 4: Regulatory, Identity & Taint (Token IDs 24 - 31)
    # -------------------------------------------------------------
    (24, "SANCTIONED_MIXER", BlockchainPillar.REGULATORY_AML,
     [r"\bsanctioned_mixer\b", r"\btornado_cash\b", r"\bofac_mixer\b", r"\btornado\b"],
     0.98, 9, "Direct or 1-hop fund transfer origin from OFAC-sanctioned mixer contract"),

    (25, "OFAC_SDN_CLUSTER", BlockchainPillar.REGULATORY_AML,
     [r"\bofac_sdn\b", r"\bsanctioned_address\b", r"\bblocked_national\b"],
     1.00, 9, "Direct match with designated global sanctions / terrorist financing list"),

    (26, "SYBIL_SWARM", BlockchainPillar.REGULATORY_AML,
     [r"\bsybil_swarm\b", r"\bcoordinated_botnet\b", r"\bdistributed_dust\b"],
     0.60, 6, "Automated cluster of ephemeral addresses executing synchronized micro-actions"),

    (27, "RAPID_MICRO_CHURN", BlockchainPillar.REGULATORY_AML,
     [r"\brapid_micro_churn\b", r"\bnonce_flooding\b", r"\bhigh_frequency_churn\b"],
     0.55, 6, "Anomalously high transaction count with negligible value transfer"),

    (28, "ILLICIT_HOP", BlockchainPillar.REGULATORY_AML,
     [r"\billicit_hop\b", r"\bpeeling_chain\b", r"\bmoney_laundering_hop\b"],
     0.82, 9, "Graph analysis indicates high-risk multi-hop layering topology"),

    (29, "MIXER_TAINT_FLOW", BlockchainPillar.REGULATORY_AML,
     [r"\bmixer_taint\b", r"\btainted_balance\b", r"\btaint_score_high\b"],
     0.78, 6, "Partial wallet balance tracing to privacy pools or compromised custody"),

    (30, "FRESH_STEALTH_WALLET", BlockchainPillar.REGULATORY_AML,
     [r"\bfresh_stealth_wallet\b", r"\bzero_history_funded\b", r"\bnew_funded_contract\b"],
     0.45, 3, "Brand-new address receiving immediate large funding from unverified bridge"),

    (31, "VERIFIED_CLEAN_RETAIL", BlockchainPillar.REGULATORY_AML,
     [r"\bclean_retail\b", r"\bkyc_verified\b", r"\blong_standing_wallet\b"],
     0.02, 3, "Established high-reputation address with zero illicit cluster proximity"),

    # -------------------------------------------------------------
    # Pillar 5: Governance & Protocol Guardrails (Token IDs 32 - 39)
    # -------------------------------------------------------------
    (32, "CIRCUIT_BREAKER_TRIP", BlockchainPillar.GOVERNANCE,
     [r"\bcircuit_breaker_trip\b", r"\bvolatility_halt\b", r"\bautomated_trip\b"],
     0.95, 9, "Emergency algorithmic trigger halting pool swaps due to extreme chaos"),

    (33, "EMERGENCY_PAUSE", BlockchainPillar.GOVERNANCE,
     [r"\bemergency_pause\b", r"\bglobal_halt\b", r"\bprotocol_freeze\b"],
     0.98, 9, "Administrative multisig or timelock invoking total system freeze"),

    (34, "TIMELOCK_BYPASS", BlockchainPillar.GOVERNANCE,
     [r"\btimelock_bypass\b", r"\bunauthorized_upgrade\b", r"\binstant_admin_change\b"],
     0.99, 9, "Anomalous contract state transition attempting to skip voting delay"),

    (35, "UNAUTHORIZED_HOOK", BlockchainPillar.GOVERNANCE,
     [r"\bunauthorized_hook\b", r"\bhook_permission_breach\b", r"\bmalicious_hook\b"],
     0.92, 9, "Uniswap v4 pool initialization with unverified or hostile callback permissions"),

    (36, "REBALANCING_VETO", BlockchainPillar.GOVERNANCE,
     [r"\brebalancing_veto\b", r"\bvault_rebalance_revert\b"],
     0.50, 3, "Vault guardian rejecting suboptimal asset rebalancing order"),

    (37, "FEE_GOVERNOR_OVERRIDE", BlockchainPillar.GOVERNANCE,
     [r"\bfee_override\b", r"\bdynamic_fee_clamp\b", r"\bmax_fee_applied\b"],
     0.65, 6, "Automated hook forcing maximum swap fee (0.50%) to penalize toxic flow"),

    (38, "PARAMETER_UPDATE_SAFE", BlockchainPillar.GOVERNANCE,
     [r"\bsafe_parameter_update\b", r"\btimelock_queued\b", r"\broutine_maintenance\b"],
     0.10, 3, "Standard DAO proposal undergoing formal timelock review"),

    (39, "NORMAL_TRANSACTION_FLOW", BlockchainPillar.GOVERNANCE,
     [r"\bnormal_swap\b", r"\bstandard_trade\b", r"\broutine_liquidity\b"],
     0.05, 3, "Healthy everyday decentralized exchange interaction")
]

for item in _RAW_DEFINITIONS:
    tok = SemanticToken(
        token_id=item[0],
        name=item[1],
        pillar=item[2],
        patterns=item[3],
        base_severity=item[4],
        tesla_harmonic=item[5],
        description=item[6]
    )
    BlockchainVocabulary._register(tok)


# =============================================================================
# HIGH-FUSION BLOCKCHAIN RESONANCE MATRIX
# =============================================================================

class BlockchainResonanceMatrix:
    """
    Mathematical Fractal Resonance Engine for Blockchain Semantics.
    Synthesizes composite perturbation vectors (delta_cx, delta_cy) via
    constructive and destructive harmonic wave superposition.
    """

    @classmethod
    def match_tokens(cls, text: str) -> List[Tuple[SemanticToken, float]]:
        """
        Scans transaction input text for all matching semantic tokens.
        Checks both original and underscore-normalized text to support snake_case and prose.
        Returns: List of (SemanticToken, match_intensity: [0.0 .. 1.0])
        """
        matches = []
        text_norm = text.replace('_', ' ')
        for token in BlockchainVocabulary.all_tokens():
            hit_count = 0
            for rx in token.compiled_regex:
                # Search in original text
                found = rx.findall(text)
                if found:
                    hit_count += len(found)
                # Search in space-normalized text
                found_norm = rx.findall(text_norm)
                if found_norm:
                    hit_count += len(found_norm)
                # Also check exact token name (lowercase, with or without underscores)
                name_snake = token.name.lower()
                name_space = name_snake.replace('_', ' ')
                if name_snake in text.lower() or name_space in text_norm.lower():
                    hit_count += 1
            if hit_count > 0:
                # Intensity saturates with multiple hits
                intensity = min(1.0, 0.6 + 0.2 * hit_count)
                matches.append((token, intensity))
        return matches

    @classmethod
    def fuse_resonance(
        cls,
        text_or_data: str,
        base_cx: float = -0.7436438870371587,
        base_cy: float = 0.13182590420531197,
        base_zoom: float = 50.0
    ) -> Dict[str, Any]:
        """
        Computes the High-Fusion Fractal Resonance Vector from input text.
        Superposes token frequencies with Tesla 3-6-9 harmonic scaling.
        """
        matches = cls.match_tokens(text_or_data)
        
        if not matches:
            # Default to benign routine flow
            token_default = BlockchainVocabulary.get_token("NORMAL_TRANSACTION_FLOW")
            matches = [(token_default, 0.5)]

        # 1. Superposition Vector Synthesis
        sum_dx = 0.0
        sum_dy = 0.0
        total_weight = 0.0
        pillar_energies = {p: 0.0 for p in BlockchainPillar}
        harmonic_counts = {3: 0, 6: 0, 9: 0}
        severities = []

        scale = 1.0 / max(10.0, base_zoom)

        for token, intensity in matches:
            w = intensity * (0.5 + 0.5 * token.base_severity)
            severities.append(token.base_severity * intensity)

            # Tesla Harmonic Factor (Tesla 3-6-9 resonance scaling)
            # Harmonic 9 provides steepest perturbation towards boundary cusp
            harmonic_mult = token.tesla_harmonic / 6.0  # 3->0.5x, 6->1.0x, 9->1.5x
            harmonic_counts[token.tesla_harmonic] += 1

            # Directional displacement with harmonic modulation
            dx = token.delta_cx * harmonic_mult * w * scale
            dy = token.delta_cy * harmonic_mult * w * scale

            sum_dx += dx
            sum_dy += dy
            total_weight += w

            pillar_energies[token.pillar] += w

        # Normalize displacement
        if total_weight > 0:
            eff_dx = sum_dx / math.sqrt(max(1.0, len(matches)))
            eff_dy = sum_dy / math.sqrt(max(1.0, len(matches)))
        else:
            eff_dx, eff_dy = 0.0, 0.0

        # Composite Risk: RMS severity
        if severities:
            comp_risk = math.sqrt(sum(s**2 for s in severities) / len(severities))
            max_risk = max(severities)
            # Blend RMS and max
            final_risk = 0.4 * comp_risk + 0.6 * max_risk
        else:
            final_risk = 0.05

        final_risk = max(0.01, min(1.0, final_risk))

        # Target Coordinates
        target_cx = base_cx + eff_dx
        target_cy = base_cy + eff_dy
        # Zoom increases with threat severity to resolve fine fractal filaments
        target_zoom = base_zoom * (1.0 + final_risk * 0.8)

        # Dominant Pillar
        dominant_pillar = max(pillar_energies.items(), key=lambda x: x[1])[0]

        # Recommended Action
        if final_risk >= 0.80:
            recommended_action = "ATOMIC_REVERT_CIRCUIT_BREAKER"
            suggested_fee_bps = 5000  # 0.50% max fee
            verdict_allowed = False
        elif final_risk >= 0.45:
            recommended_action = "DYNAMIC_FEE_SURGE"
            suggested_fee_bps = int(500 + (final_risk - 0.45) * 8000)  # scale up
            verdict_allowed = True
        else:
            recommended_action = "PERMIT_STANDARD_EXECUTION"
            suggested_fee_bps = 500   # 0.05% min fee
            verdict_allowed = True

        return {
            "matched_tokens": [t.name for t, _ in matches],
            "token_count": len(matches),
            "dominant_pillar": dominant_pillar.value,
            "tesla_harmonic_distribution": harmonic_counts,
            "composite_risk": round(final_risk, 4),
            "composite_risk_fp": float_to_fp(final_risk),
            "delta_cx": round(eff_dx, 8),
            "delta_cy": round(eff_dy, 8),
            "delta_cx_fp": float_to_fp(eff_dx),
            "delta_cy_fp": float_to_fp(eff_dy),
            "target_cx": round(target_cx, 8),
            "target_cy": round(target_cy, 8),
            "target_zoom": round(target_zoom, 4),
            "suggested_fee_bps": suggested_fee_bps,
            "recommended_action": recommended_action,
            "verdict_allowed": verdict_allowed
        }
