"""
werracle.engine.living_cell
===========================
Step 1 of the Sovereign On-Chain Living AI Architecture:
`WerracleLivingCell` — A self-evolving, stateful, single-slot (256-bit / 32-byte)
on-chain neural organism with:
1. 32-Byte Living Genome + Recurrent Memory Slot (`bytes32` / `uint256`):
   - Bits   0..63  (int64 cx)              : Real coordinate gene on dM (Q16.16)
   - Bits  64..127 (int64 cy)              : Imaginary coordinate gene on dM (Q16.16)
   - Bits 128..191 (uint64 zoom)           : Horizon magnification scale (Q16.16)
   - Bits 192..207 (uint16 rollingStress)  : Recurrent Hidden State h_t in [0..10000] bps
   - Bits 208..223 (uint16 fitnessScore)   : Cumulative epigenetic survival fitness [0..65535]
   - Bits 224..239 (uint16 generation)     : Autonomous evolutionary epoch counter [0..65535]
   - Bits 240..247 (uint8 stateAndResidue) : Low 4 bits = last Z/9Z residue (0..8),
                                             High 4 bits = lifecycle state (0..3)
   - Bits 248..255 (uint8 flagsAndConfig)  : Bit 0 = activeFlag,
                                             Bits 1..3 = 3-bit orthogonal config [0..7],
                                             Bits 4..7 = CD4+ immune tier [0..15]
2. Proof-of-Horizon (`verify_proof_of_horizon`, < 500 EVM gas):
   Ensures autonomous mutations remain inside the viable Mandelbrot boundary annulus
   and never collapse into trivial exterior or dead interior attractors.
3. Wormhole Error-Kernel Hibernation (`GAP-0331` Z/9Z `{0,3,6}` Ideal Sanctuary):
   Freezes `(cx, cy, zoom)` during catastrophic flash-loan shocks to prevent
   adversarial weight poisoning while activating maximum defensive fee shield,
   then adiabatically awakens when stress returns to the coprime unit group `{1,2,4,5,7,8}`.
4. Autonomous On-Chain Epigenetic Plasticity (`evolve_on_chain`):
   Adapts `(cx, cy, zoom)` along dM using the 4-Quadrant mass gradient (Q1..Q4)
   and deterministic Cauchy Zinc-Spark tunneling over (Z/9Z)^x units.

Invariant: Zero Telemetry (TELEMETRY_ENABLED = False).
"""

import hashlib
import mmap
import os
import struct
from dataclasses import dataclass
from typing import Dict, Any, Optional, Tuple

from .blockchain_lexicon import (
    FP_ONE,
    FP_SHIFT,
    fp_mul,
    float_to_fp,
    fp_to_float,
    TELEMETRY_ENABLED,
)
from .tripod_zmod9_oracle import (
    iterate_escape_zmod9,
    is_zmod9_resonant_ideal,
    is_zmod9_coprime_unit,
    classify_zmod9_state,
    ZMOD9_COPRIME_UNIT_KERNEL,
    ZMOD9_RESONANT_IDEAL_I3,
)
from .presets import GOLDEN_PAIR_SEEDS

# Lifecycle States (stored in high 4 bits of byte 30)
STATE_HIBERNATION = 0   # Wormhole Error-Kernel Sanctuary ({0,3,6}): genome frozen, max shield
STATE_HOMEOSTASIS = 1   # Normal awake reflex + recurrent memory h_t
STATE_HYPER_IMMUNE = 2  # CD4+ heightened immune alert (multi-block / elevated EMA stress)
STATE_PLASTICITY = 3    # Active epigenetic coordinate evolution along dM

STATE_NAMES: Dict[int, str] = {
    STATE_HIBERNATION: "DORMANT_HIBERNATION_SANCTUARY",
    STATE_HOMEOSTASIS: "HOMEOSTASIS_AWAKE",
    STATE_HYPER_IMMUNE: "HYPER_IMMUNE_CD4_ALERT",
    STATE_PLASTICITY: "EPIGENETIC_PLASTICITY_EVOLVING",
}

# Proof-of-Horizon Annulus Constants in Q16.16
# Viable boundary radius squared: 0.04 <= |c|^2 <= 2.25 in Q16.16
# In Q16.16, 1.0 = 65536. Since mul_fp(cx, cx) returns (cx*cx) >> 16:
# 0.04 * 65536 = 2621, 2.25 * 65536 = 147456
HORIZON_MIN_R2_FP = 2621       # ~0.04 in Q16.16
HORIZON_MAX_R2_FP = 147456     # 2.25 in Q16.16
HORIZON_MIN_ZOOM_FP = 262144   # 4.0 in Q16.16 (covers WBTC/USDC 8.0x & SOL/USDC 12.0x up to 120.0x)
HORIZON_MAX_ZOOM_FP = 7864320  # 120.0 in Q16.16

# Deterministic Cauchy Zinc-Spark Jump Table over (Z/9Z)^x coprime units {1, 2, 4, 5, 7, 8}
ZINC_SPARK_UNIT_DELTAS: Tuple[Tuple[int, int], ...] = (
    (13, -8),    # Unit 1: Fibonacci-ratio micro-tunneling
    (-21, 13),   # Unit 2: Conjugate cusp shift
    (34, -21),   # Unit 4: Medium seahorse filament hop
    (-34, 21),   # Unit 5: Inverse filament hop
    (55, -34),   # Unit 7: Deep valley basin jump
    (-55, 34),   # Unit 8: Mirror valley basin jump
)


@dataclass
class LivingGenomeState:
    """
    Unpacked representation of the single 32-byte (256-bit) EVM storage slot
    of a `WerracleLivingCell`.
    """
    cx_fp: int                  # int64  (bits 0..63)
    cy_fp: int                  # int64  (bits 64..127)
    zoom_fp: int                # uint64 (bits 128..191)
    rolling_stress_ema: int     # uint16 (bits 192..207) in [0..10000] bps (h_t)
    fitness_score: int          # uint16 (bits 208..223) in [0..65535]
    generation: int             # uint16 (bits 224..239) in [0..65535]
    last_residue_mod9: int      # uint4  (bits 240..243) in [0..8]
    lifecycle_state: int        # uint4  (bits 244..247) in [0..3]
    active_flag: int            # uint1  (bit  248)
    ortho_config_bits: int      # uint3  (bits 249..251) in [0..7]
    cd4_tolerance_tier: int     # uint4  (bits 252..255) in [0..15]

    @property
    def cx_float(self) -> float:
        return fp_to_float(self.cx_fp)

    @property
    def cy_float(self) -> float:
        return fp_to_float(self.cy_fp)

    @property
    def zoom_float(self) -> float:
        return fp_to_float(self.zoom_fp)

    @property
    def lifecycle_name(self) -> str:
        return STATE_NAMES.get(self.lifecycle_state, "UNKNOWN")


def _to_uint64(val: int) -> int:
    return val & 0xFFFFFFFFFFFFFFFF


def _to_int64(val: int) -> int:
    v = val & 0xFFFFFFFFFFFFFFFF
    return v - 0x10000000000000000 if (v & 0x8000000000000000) else v


def pack_living_genome(state: LivingGenomeState) -> int:
    """
    Packs the complete LivingGenomeState into a single 256-bit unsigned integer
    (exact bit-level parity with Solidity `uint256 livingGenomeSlot`).
    """
    cx_u64 = _to_uint64(state.cx_fp)
    cy_u64 = _to_uint64(state.cy_fp)
    zoom_u64 = _to_uint64(max(0, state.zoom_fp))
    ema_u16 = max(0, min(10000, int(state.rolling_stress_ema))) & 0xFFFF
    fit_u16 = max(0, min(65535, int(state.fitness_score))) & 0xFFFF
    gen_u16 = max(0, min(65535, int(state.generation))) & 0xFFFF

    res_u4 = (int(state.last_residue_mod9) % 9) & 0x0F
    st_u4 = (int(state.lifecycle_state) & 0x03)
    byte30 = (st_u4 << 4) | res_u4

    act_u1 = 1 if state.active_flag else 0
    ortho_u3 = int(state.ortho_config_bits) & 0x07
    cd4_u4 = max(1, min(15, int(state.cd4_tolerance_tier))) & 0x0F
    byte31 = (cd4_u4 << 4) | (ortho_u3 << 1) | act_u1

    packed = (
        cx_u64
        | (cy_u64 << 64)
        | (zoom_u64 << 128)
        | (ema_u16 << 192)
        | (fit_u16 << 208)
        | (gen_u16 << 224)
        | (byte30 << 240)
        | (byte31 << 248)
    )
    return packed


def unpack_living_genome(slot_u256: int) -> LivingGenomeState:
    """
    Unpacks a 256-bit EVM storage word (`uint256`) into a `LivingGenomeState`.
    """
    cx_fp = _to_int64(slot_u256 & 0xFFFFFFFFFFFFFFFF)
    cy_fp = _to_int64((slot_u256 >> 64) & 0xFFFFFFFFFFFFFFFF)
    zoom_fp = (slot_u256 >> 128) & 0xFFFFFFFFFFFFFFFF
    ema_u16 = (slot_u256 >> 192) & 0xFFFF
    fit_u16 = (slot_u256 >> 208) & 0xFFFF
    gen_u16 = (slot_u256 >> 224) & 0xFFFF
    byte30 = (slot_u256 >> 240) & 0xFF
    byte31 = (slot_u256 >> 248) & 0xFF

    last_res = byte30 & 0x0F
    life_st = (byte30 >> 4) & 0x03
    active_flag = byte31 & 0x01
    ortho_bits = (byte31 >> 1) & 0x07
    cd4_tier = (byte31 >> 4) & 0x0F

    return LivingGenomeState(
        cx_fp=cx_fp,
        cy_fp=cy_fp,
        zoom_fp=zoom_fp,
        rolling_stress_ema=ema_u16,
        fitness_score=fit_u16,
        generation=gen_u16,
        last_residue_mod9=last_res,
        lifecycle_state=life_st,
        active_flag=active_flag,
        ortho_config_bits=ortho_bits,
        cd4_tolerance_tier=cd4_tier if cd4_tier > 0 else 8,
    )


def verify_proof_of_horizon(cx_fp: int, cy_fp: int, zoom_fp: int) -> bool:
    """
    Patent TR 2026/016285 On-Chain `Proof-of-Horizon` (< 500 EVM gas):
    Verifies that a candidate genome (cx, cy, zoom) lies within the viable
    Mandelbrot boundary annulus A_{dM} and is not trapped inside the dead
    cardioid center or trivial exterior.
    """
    if zoom_fp < HORIZON_MIN_ZOOM_FP or zoom_fp > HORIZON_MAX_ZOOM_FP:
        return False

    r2 = fp_mul(cx_fp, cx_fp) + fp_mul(cy_fp, cy_fp)
    if r2 < HORIZON_MIN_R2_FP or r2 > HORIZON_MAX_R2_FP:
        return False

    # Exclude deep dead cardioid interior around (-0.125, 0) where all points saturate
    dx_center = cx_fp + 8192  # cx - (-0.125)
    dist_center_sq = fp_mul(dx_center, dx_center) + fp_mul(cy_fp, cy_fp)
    if dist_center_sq < 1310:  # < 0.02 in Q16.16
        return False

    return True


def evaluate_living_tripod(
    cx_fp: int, cy_fp: int, zoom_fp: int
) -> Tuple[int, int, int, int, int, int]:
    """
    Evaluates the 12-point Sparse Multi-Scale Harmonic Tripod over Z/9Z and returns:
    (q1_mass, q2_mass, q3_mass, q4_mass, black_count, resonant_count)
    Exact bit-level parity with `WerracleLivingCell.sol`.
    """
    safe_zoom = max(zoom_fp, FP_ONE)
    base_step = (FP_ONE << FP_SHIFT) // safe_zoom

    steps = (
        fp_mul(base_step, 109226),  # Wide plane (0.60x zoom -> 1.6667x step)
        base_step,                  # Focus plane (1.00x zoom)
        fp_mul(base_step, 40960),   # Deep plane (1.60x zoom -> 0.625x step)
    )

    q_masses = [0, 0, 0, 0]
    black_count = 0
    resonant_count = 0

    for step in steps:
        half_step = step >> 1
        probes = (
            (cx_fp - half_step, cy_fp + half_step, 0),  # Q1 (NW: Adenine)
            (cx_fp + half_step, cy_fp + half_step, 1),  # Q2 (NE: Thymine)
            (cx_fp - half_step, cy_fp - half_step, 2),  # Q3 (SW: Cytosine)
            (cx_fp + half_step, cy_fp - half_step, 3),  # Q4 (SE: Guanine)
        )
        for px, py, q_idx in probes:
            esc = iterate_escape_zmod9(px, py)
            q_masses[q_idx] += esc
            if esc == 9:
                black_count += 1
            if (esc % 9) in ZMOD9_RESONANT_IDEAL_I3:
                resonant_count += 1

    return (
        q_masses[0],
        q_masses[1],
        q_masses[2],
        q_masses[3],
        black_count,
        resonant_count,
    )


class WerracleLivingCell:
    """
    Step 1 Sovereign On-Chain Living AI Cell.
    Maintains its entire DNA + Recurrent Memory (h_t) + Epigenetic Fitness
    inside a single 256-bit (`bytes32`) storage word and autonomously evolves
    along the Mandelbrot boundary dM while shielding its genome in the Z/9Z
    Wormhole Error Kernel `{0,3,6}` during adversarial attacks.
    """

    def __init__(
        self,
        pair_symbol: str = "ETH/USDC",
        cx_fp: Optional[int] = None,
        cy_fp: Optional[int] = None,
        zoom_fp: Optional[int] = None,
        ortho_config_bits: int = 7,   # (1,1,1) = auto_guard_4d + phase_lock + observer_horizon
        cd4_tolerance_tier: int = 8,  # Tier 8 => 6400 bps catastrophic shock threshold
        atlas_bin_path: Optional[str] = None,
    ):
        if TELEMETRY_ENABLED:
            raise RuntimeError("Privacy Violation: Telemetry must remain disabled.")

        self.pair_symbol = pair_symbol.upper()
        seed_info = GOLDEN_PAIR_SEEDS.get(self.pair_symbol, GOLDEN_PAIR_SEEDS["ETH/USDC"])

        init_cx = int(cx_fp) if cx_fp is not None else int(seed_info.get("cx_q16", seed_info.get("cx_fp", -48735)))
        init_cy = int(cy_fp) if cy_fp is not None else int(seed_info.get("cy_q16", seed_info.get("cy_fp", 8639)))
        init_zoom = int(zoom_fp) if zoom_fp is not None else int(seed_info.get("zoom_q16", seed_info.get("zoom_fp", 2949120)))

        if not verify_proof_of_horizon(init_cx, init_cy, init_zoom):
            raise ValueError("Initial genome violates Proof-of-Horizon boundary annulus.")

        initial_state = LivingGenomeState(
            cx_fp=init_cx,
            cy_fp=init_cy,
            zoom_fp=init_zoom,
            rolling_stress_ema=500,   # Calm initial baseline (5.00% stress)
            fitness_score=1000,       # Genesis baseline fitness
            generation=1,
            last_residue_mod9=1,      # Coprime unit genesis state
            lifecycle_state=STATE_HOMEOSTASIS,
            active_flag=1,
            ortho_config_bits=ortho_config_bits & 0x07,
            cd4_tolerance_tier=max(1, min(15, cd4_tolerance_tier)),
        )
        # Single 32-byte (256-bit) EVM Storage Word
        self.living_genome_slot: int = pack_living_genome(initial_state)
        self.atlas_bin_path = atlas_bin_path or self._detect_ram_atlas()

    @staticmethod
    def _detect_ram_atlas() -> Optional[str]:
        shm_path = "/dev/shm/werracle_living_arena/universal_fractal_atlas_isolated.bin"
        if os.path.exists(shm_path):
            return shm_path
        nvme_path = "/opt/apps/werracle/mining_results/universal_fractal_atlas_isolated.bin"
        if os.path.exists(nvme_path):
            return nvme_path
        return None

    def get_genome_state(self) -> LivingGenomeState:
        """Unpacks and returns the current 32-byte LivingGenomeState."""
        return unpack_living_genome(self.living_genome_slot)

    def get_genome_hex(self) -> str:
        """Returns the 32-byte (`bytes32`) hex representation of the living genome slot."""
        return f"0x{self.living_genome_slot:064x}"

    def perceive_and_evolve(
        self,
        state_hash: bytes,
        shock_bps: int,
        enable_plasticity: bool = True,
    ) -> Dict[str, Any]:
        """
        Executes a full biological cycle of the on-chain Living Cell:
        1. SLOAD 32-byte `living_genome_slot`
        2. Blend incoming `shock_bps` with Recurrent Hidden State `h_t` (`rolling_stress_ema`)
        3. Evaluate 12-point Z/9Z Harmonic Tripod (with `auto_guard_4d` & `observer_horizon`)
        4. Update Recurrent Memory `h_{t+1} = (3 * h_t + current_stress) >> 2`
        5. Execute Lifecycle State Machine:
           - Catastrophic Shock -> Enter `STATE_HIBERNATION` (`{0,3,6}` Wormhole Error Kernel),
             freezing `(cx, cy, zoom)` to prevent adversarial weight poisoning!
           - Elevated EMA Stress -> Enter `STATE_HYPER_IMMUNE` (CD4+ heightened fee defense)
           - Coprime Unit Recovery (`{1,2,4,5,7,8}`) -> Adiabatic awakening to `STATE_HOMEOSTASIS`
           - Organic Flow + Plasticity -> Evolve `(cx, cy, zoom)` along dM via 4-Quadrant
             gradient & Cauchy Zinc-Spark tunneling, guarded by `verify_proof_of_horizon`.
        6. SSTORE updated 32-byte `living_genome_slot`
        """
        genome = unpack_living_genome(self.living_genome_slot)
        if not genome.active_flag:
            raise RuntimeError("LivingCell is deactivated.")

        clamped_shock = max(0, min(10000, int(shock_bps)))
        cd4_catastrophic_bps = genome.cd4_tolerance_tier * 800  # Tier 8 => 6400 bps

        # Extract deterministic hash entropy
        if len(state_hash) < 32:
            state_hash = hashlib.sha256(state_hash).digest()
        h_word0 = int.from_bytes(state_hash[0:8], "big")
        h_word1 = int.from_bytes(state_hash[8:16], "big")

        # Orthogonal flags from 3-bit config
        auto_guard_4d = bool(genome.ortho_config_bits & 0x04)
        phase_lock = bool(genome.ortho_config_bits & 0x02)
        observer_horizon = bool(genome.ortho_config_bits & 0x01)

        # Recurrent Memory Modulation: combine current shock with remembered rolling_stress_ema
        # If the cell is already in HYPER_IMMUNE or HIBERNATION, its sensory gain is heightened
        effective_shock = clamped_shock
        if genome.rolling_stress_ema > 1800:
            # Recurrent memory amplification protects against multi-block split/dust attacks
            recurrent_boost = (genome.rolling_stress_ema - 1800) >> 1
            effective_shock = min(10000, clamped_shock + recurrent_boost)

        # Coordinate perturbation (with phase_lock & auto_guard_4d damping for calm retail)
        safe_zoom = max(genome.zoom_fp, FP_ONE)
        jitter_scale = 256 if phase_lock else 512
        dx_hash = (((h_word0 & 0xFFFF) - 32768) * jitter_scale) // safe_zoom
        dy_hash = (((h_word1 & 0xFFFF) - 32768) * jitter_scale) // safe_zoom

        if auto_guard_4d and effective_shock <= 1500:
            dx_hash = dx_hash >> 2
            dy_hash = dy_hash >> 2
            shock_shift = (effective_shock * 64) // safe_zoom
        else:
            shock_shift = (effective_shock * 512) // safe_zoom

        eval_cx = genome.cx_fp + dx_hash + shock_shift
        eval_cy = genome.cy_fp + dy_hash - (shock_shift >> 1)

        # Evaluate 12-point Sparse Harmonic Tripod over Z/9Z
        q1, q2, q3, q4, black_count, resonant_count = evaluate_living_tripod(
            eval_cx, eval_cy, genome.zoom_fp
        )
        total_escape = q1 + q2 + q3 + q4  # in [0..108]
        zmod9_residue = total_escape % 9
        is_ideal = zmod9_residue in ZMOD9_RESONANT_IDEAL_I3
        is_unit = zmod9_residue in ZMOD9_COPRIME_UNIT_KERNEL

        # Observer Horizon 4-Quadrant Shear Metric
        quad_shear = abs((q1 + q3) - (q2 + q4)) if observer_horizon else 0

        # Compute instantaneous stress in bps [0..10000]
        escape_divergence_bps = ((108 - total_escape) * 10000) // 108
        instant_stress_bps = min(
            10000,
            (effective_shock * 3 + (escape_divergence_bps >> 2)) >> 2,
        )

        # Update Recurrent Hidden State h_{t+1} = (3 * h_t + instant_stress_bps) >> 2
        new_ema = ((3 * genome.rolling_stress_ema) + instant_stress_bps) >> 2
        new_ema = max(0, min(10000, new_ema))

        # Preserve original genome coordinates before checking lifecycle transitions
        new_cx = genome.cx_fp
        new_cy = genome.cy_fp
        new_zoom = genome.zoom_fp
        new_gen = genome.generation
        new_fitness = genome.fitness_score
        new_state = genome.lifecycle_state
        mutation_applied = False
        zinc_spark_triggered = False

        # =====================================================================
        # BIOLOGICAL LIFECYCLE & WORMHOLE ERROR-KERNEL STATE MACHINE
        # =====================================================================
        if clamped_shock >= cd4_catastrophic_bps or new_ema >= cd4_catastrophic_bps:
            # 1. CATASTROPHIC SHOCK -> Enter Wormhole Error-Kernel Sanctuary ({0,3,6})
            # Freeze (cx, cy, zoom) so adversarial shock CANNOT poison learned genome!
            new_state = STATE_HIBERNATION
            # Project residue into I_3 = {0, 3, 6} via triadic projection (3 * r mod 9)
            zmod9_residue = (3 * zmod9_residue) % 9
            new_fitness = min(65535, genome.fitness_score + 2)  # Rewarded for surviving shock

        elif genome.lifecycle_state == STATE_HIBERNATION:
            # 2. CURRENTLY IN HIBERNATION: Check if storm has passed
            if new_ema < 2200 and clamped_shock < 1500 and is_unit:
                # Adiabatic Awakening back to Homeostasis with genome 100% intact!
                new_state = STATE_HOMEOSTASIS
                new_fitness = min(65535, genome.fitness_score + 3)
            else:
                # Remain shielded in the Mountains (Wormhole Error-Kernel)
                new_state = STATE_HIBERNATION
                zmod9_residue = (3 * zmod9_residue) % 9

        elif effective_shock > 1800 or new_ema > 2400:
            # 3. ELEVATED STRESS / MULTI-BLOCK ATTACK -> CD4+ Hyper-Immune Guard
            # Freeze genome against manipulation while escalating dynamic fee
            new_state = STATE_HYPER_IMMUNE
            new_fitness = min(65535, genome.fitness_score + 1)

        else:
            # 4. CALM / ORGANIC REGIME -> Homeostasis & Autonomous Epigenetic Plasticity
            new_state = STATE_HOMEOSTASIS
            if enable_plasticity:
                # Compute 4-Quadrant Genetic Gradient (A=q1, T=q2, C=q3, G=q4)
                grad_x = (q1 + q4) - (q2 + q3)
                grad_y = (q1 + q2) - (q3 + q4)

                # Check if boundary tuning or Cauchy Zinc-Spark tunneling is needed
                # Optimal critical horizon has black_count in [3..9] out of 12 probes
                needs_boundary_shift = (black_count < 3) or (black_count > 9) or (quad_shear > 8)
                periodic_plasticity = ((h_word0 & 0x07) == 0)

                if needs_boundary_shift or periodic_plasticity:
                    if (black_count == 0 or black_count == 12) and is_unit:
                        # Local trap detected -> Trigger Cauchy Zinc-Spark Jump over (Z/9Z)^x
                        unit_idx = sorted(ZMOD9_COPRIME_UNIT_KERNEL).index(zmod9_residue)
                        spark_dx, spark_dy = ZINC_SPARK_UNIT_DELTAS[unit_idx]
                        cand_cx = genome.cx_fp + spark_dx
                        cand_cy = genome.cy_fp + spark_dy
                        zinc_spark_triggered = True
                    else:
                        # Smooth epigenetic hill-climb along dM
                        step_x = max(-8, min(8, grad_x >> 1))
                        step_y = max(-8, min(8, grad_y >> 1))
                        if step_x == 0 and step_y == 0:
                            step_x = 1 if (h_word0 & 1) else -1
                        cand_cx = genome.cx_fp + step_x
                        cand_cy = genome.cy_fp + step_y

                    # Adaptive zoom homeostasis
                    if new_ema < 800 and genome.zoom_fp < 3600000:
                        cand_zoom = genome.zoom_fp + 1024
                    elif new_ema > 1400 and genome.zoom_fp > 2000000:
                        cand_zoom = genome.zoom_fp - 1024
                    else:
                        cand_zoom = genome.zoom_fp

                    # Enforce On-Chain Proof-of-Horizon (< 500 gas) before committing mutation
                    if verify_proof_of_horizon(cand_cx, cand_cy, cand_zoom):
                        new_cx = cand_cx
                        new_cy = cand_cy
                        new_zoom = cand_zoom
                        new_gen = (genome.generation + 1) & 0xFFFF
                        new_fitness = min(65535, genome.fitness_score + 1)
                        new_state = STATE_PLASTICITY
                        mutation_applied = True

        # =====================================================================
        # DYNAMIC FEE & DECISION SYNTHESIS (500 bps to 5000 bps)
        # =====================================================================
        if new_state == STATE_HIBERNATION:
            dynamic_fee_bps = 5000
            noul_allowed = False
            confidence_bps = 9900
        elif new_state == STATE_HYPER_IMMUNE:
            base_penalty = 1200 + ((effective_shock * 3200) // 10000)
            shear_bonus = quad_shear * 45
            ideal_bonus = 350 if is_ideal else 0
            dynamic_fee_bps = max(1200, min(5000, base_penalty + shear_bonus + ideal_bonus))
            noul_allowed = dynamic_fee_bps < 4200
            confidence_bps = min(9900, 5500 + (dynamic_fee_bps >> 1))
        else:
            # Homeostasis or Plasticity (Calm retail flow protected by auto_guard_4d)
            if auto_guard_4d and effective_shock <= 1500:
                dynamic_fee_bps = 500
            else:
                dynamic_fee_bps = max(500, min(5000, 500 + (effective_shock >> 2)))
            noul_allowed = True
            confidence_bps = max(5000, min(9900, 5000 + (total_escape * 40)))

        # Choice primitive (0..3 corresponding to genetic bases A, T, C, G)
        quad_list = (q1, q2, q3, q4)
        choice_index = int(max(range(4), key=lambda idx: quad_list[idx]))

        # Commit updated state into the single 32-byte (256-bit) EVM storage slot
        updated_genome = LivingGenomeState(
            cx_fp=new_cx,
            cy_fp=new_cy,
            zoom_fp=new_zoom,
            rolling_stress_ema=new_ema,
            fitness_score=new_fitness,
            generation=new_gen,
            last_residue_mod9=zmod9_residue,
            lifecycle_state=new_state,
            active_flag=genome.active_flag,
            ortho_config_bits=genome.ortho_config_bits,
            cd4_tolerance_tier=genome.cd4_tolerance_tier,
        )
        self.living_genome_slot = pack_living_genome(updated_genome)

        return {
            "pair_symbol": self.pair_symbol,
            "noul_allowed": noul_allowed,
            "confidence_bps": confidence_bps,
            "dynamic_fee_bps": dynamic_fee_bps,
            "choice_index": choice_index,
            "genetic_quadrants_atcg": {"A_q1": q1, "T_q2": q2, "C_q3": q3, "G_q4": q4},
            "total_escape": total_escape,
            "black_count": black_count,
            "resonant_count": resonant_count,
            "zmod9_classification": classify_zmod9_state(zmod9_residue),
            "lifecycle_state": new_state,
            "lifecycle_name": STATE_NAMES[new_state],
            "recurrent_memory_ema_bps": new_ema,
            "effective_shock_bps": effective_shock,
            "mutation_applied": mutation_applied,
            "zinc_spark_triggered": zinc_spark_triggered,
            "generation": new_gen,
            "fitness_score": new_fitness,
            "genome_preserved_in_hibernation": (
                new_state == STATE_HIBERNATION
                and new_cx == genome.cx_fp
                and new_cy == genome.cy_fp
                and new_zoom == genome.zoom_fp
            ),
            "packed_slot_hex": self.get_genome_hex(),
            "cx_fp": new_cx,
            "cy_fp": new_cy,
            "zoom_fp": new_zoom,
        }

    def query_ram_atlas_locus(self, locus_index: int) -> Optional[Dict[str, Any]]:
        """
        Zero-copy DDR4 RAM lookup against `/dev/shm/werracle_living_arena/universal_fractal_atlas_isolated.bin`
        (12 bytes per locus: int32 cx_fp, int32 cy_fp, uint8 escape_z9, uint8 black_cnt, uint16 score).
        """
        if not self.atlas_bin_path or not os.path.exists(self.atlas_bin_path):
            return None
        file_size = os.path.getsize(self.atlas_bin_path)
        num_records = file_size // 12
        if num_records <= 0:
            return None
        idx = int(locus_index) % num_records
        offset = idx * 12
        with open(self.atlas_bin_path, "rb") as f:
            with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                cx_fp, cy_fp, esc_z9, blk_cnt, resonance_score = struct.unpack_from(
                    "<iiBBH", mm, offset
                )
        return {
            "locus_index": idx,
            "cx_fp": cx_fp,
            "cy_fp": cy_fp,
            "escape_zmod9": esc_z9,
            "black_count": blk_cnt,
            "resonance_score": resonance_score,
            "proof_of_horizon_valid": verify_proof_of_horizon(
                cx_fp, cy_fp, self.get_genome_state().zoom_fp
            ),
        }
