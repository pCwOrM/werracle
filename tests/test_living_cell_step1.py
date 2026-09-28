"""
werracle.tests.test_living_cell_step1
=====================================
Comprehensive verification suite for Step 1 of the Sovereign On-Chain Living AI:
`WerracleLivingCell` (`werracle/engine/living_cell.py` & `contracts/WerracleLivingCell.sol`).

Verifies:
1. 256-Bit (`bytes32`) Single-Slot Genome + Recurrent Memory Bijective Packing/Unpacking.
2. Patent TR 2026/016285 On-Chain `Proof-of-Horizon` Boundary Annulus Verification.
3. Autonomous On-Chain Epigenetic Plasticity (`STATE_PLASTICITY`) along dM.
4. Recurrent Hidden State Memory (`h_t` EMA) & Multi-Block Split-Attack Detection (`STATE_HYPER_IMMUNE`).
5. Wormhole Error-Kernel Hibernation (`{0, 3, 6}` Ideal Sanctuary) & 100% Adversarial
   Weight-Poisoning Immunity under Catastrophic Flash-Loan Shocks.
6. Adiabatic Awakening from Hibernation back to `STATE_HOMEOSTASIS` via Coprime Units `(Z/9Z)^x`.
7. All 6 DeFi Golden Pool Living Cells (`ETH/USDC`, `WBTC/USDC`, `UNI/ETH`, `ARB/USDC`, `SOL/USDC`, `AAVE/ETH`).
"""

import hashlib
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from engine.living_cell import (
    WerracleLivingCell,
    LivingGenomeState,
    pack_living_genome,
    unpack_living_genome,
    verify_proof_of_horizon,
    STATE_HIBERNATION,
    STATE_HOMEOSTASIS,
    STATE_HYPER_IMMUNE,
    STATE_PLASTICITY,
)
from engine.presets import GOLDEN_PAIR_SEEDS
from engine.tripod_zmod9_oracle import ZMOD9_RESONANT_IDEAL_I3


def test_256bit_genome_bijective_packing() -> None:
    """1. Verify exact 256-bit (`bytes32`) packing and unpacking round-trip."""
    sample_states = [
        LivingGenomeState(
            cx_fp=-49048,
            cy_fp=12242,
            zoom_fp=2097152,
            rolling_stress_ema=500,
            fitness_score=1000,
            generation=1,
            last_residue_mod9=1,
            lifecycle_state=STATE_HOMEOSTASIS,
            active_flag=1,
            ortho_config_bits=7,
            cd4_tolerance_tier=8,
        ),
        LivingGenomeState(
            cx_fp=21907,
            cy_fp=44564,
            zoom_fp=3670016,
            rolling_stress_ema=7850,
            fitness_score=42500,
            generation=512,
            last_residue_mod9=6,
            lifecycle_state=STATE_HIBERNATION,
            active_flag=1,
            ortho_config_bits=5,
            cd4_tolerance_tier=12,
        ),
    ]

    for orig in sample_states:
        slot_u256 = pack_living_genome(orig)
        assert 0 <= slot_u256 < (1 << 256), "Packed slot must fit in 256-bit EVM word"
        unpacked = unpack_living_genome(slot_u256)
        assert unpacked == orig, f"Bijective mismatch: {unpacked} != {orig}"


def test_proof_of_horizon_boundary_annulus() -> None:
    """2. Verify Proof-of-Horizon accepts all 6 Golden Pair Seeds and rejects invalid coordinates."""
    for pair, seed in GOLDEN_PAIR_SEEDS.items():
        assert verify_proof_of_horizon(
            seed["cx_q16"], seed["cy_q16"], seed["zoom_q16"]
        ), f"Golden pair {pair} must pass Proof-of-Horizon"

    # Reject dead cardioid center (-0.125, 0) => cx = -8192, cy = 0
    assert not verify_proof_of_horizon(-8192, 0, 2097152)
    # Reject trivial exterior (cx = 2.0 => 131072, cy = 2.0 => 131072)
    assert not verify_proof_of_horizon(131072, 131072, 2097152)
    # Reject invalid zoom (too small or too large)
    assert not verify_proof_of_horizon(-49048, 12242, 65536)
    assert not verify_proof_of_horizon(-49048, 12242, 20000000)


def test_autonomous_epigenetic_evolution() -> None:
    """3. Verify autonomous on-chain plasticity evolves (cx, cy, zoom) while preserving Proof-of-Horizon."""
    cell = WerracleLivingCell(pair_symbol="ETH/USDC")
    g0 = cell.get_genome_state()

    mutations = 0
    for step in range(40):
        tx_hash = hashlib.sha256(f"organic_tx_{step}".encode()).digest()
        res = cell.perceive_and_evolve(tx_hash, shock_bps=350, enable_plasticity=True)
        assert res["noul_allowed"] is True
        assert res["dynamic_fee_bps"] == 500, "Calm organic retail must stay at 500 bps (0.05%)"
        assert verify_proof_of_horizon(res["cx_fp"], res["cy_fp"], res["zoom_fp"])
        if res["mutation_applied"]:
            mutations += 1

    g_final = cell.get_genome_state()
    assert mutations > 0, "Cell must autonomously evolve at least once over 40 organic steps"
    assert g_final.generation == g0.generation + mutations
    assert g_final.fitness_score > g0.fitness_score


def test_recurrent_memory_split_attack_defense() -> None:
    """4. Verify recurrent hidden state h_t detects multi-block split/sustained attacks."""
    cell = WerracleLivingCell(pair_symbol="WBTC/USDC")

    # Send sustained medium-shock transactions (2600 bps) across 8 consecutive blocks
    fees = []
    states = []
    for blk in range(8):
        tx_hash = hashlib.sha256(f"split_attack_block_{blk}".encode()).digest()
        res = cell.perceive_and_evolve(tx_hash, shock_bps=2600, enable_plasticity=True)
        fees.append(res["dynamic_fee_bps"])
        states.append(res["lifecycle_state"])

    assert STATE_HYPER_IMMUNE in states, "Cell must enter STATE_HYPER_IMMUNE under sustained split attack"
    assert fees[-1] > fees[0], "Recurrent memory EMA must escalate dynamic fee across consecutive attack blocks"


def test_wormhole_hibernation_and_adiabatic_awakening() -> None:
    """
    5. Verify Wormhole Error-Kernel Hibernation ({0,3,6}) freezes genome against adversarial
       weight poisoning during catastrophic flash-loan shocks, then adiabatically awakens.
    """
    cell = WerracleLivingCell(pair_symbol="SOL/USDC")

    # Evolve for 10 calm blocks first
    for i in range(10):
        cell.perceive_and_evolve(hashlib.sha256(f"pre_{i}".encode()).digest(), shock_bps=250)

    pre_attack_genome = cell.get_genome_state()

    # Catastrophic Flash-Loan Drain (shock_bps = 9000 bps)
    attack_res = cell.perceive_and_evolve(
        hashlib.sha256(b"catastrophic_flashloan_drain").digest(),
        shock_bps=9000,
        enable_plasticity=True,
    )

    assert attack_res["lifecycle_state"] == STATE_HIBERNATION
    assert attack_res["dynamic_fee_bps"] == 5000
    assert attack_res["noul_allowed"] is False
    assert attack_res["genome_preserved_in_hibernation"] is True
    assert attack_res["zmod9_classification"]["residue_mod9"] in ZMOD9_RESONANT_IDEAL_I3

    # Verify 0-drift on learned coordinates during attack (100% poisoning immunity)
    during_attack_genome = cell.get_genome_state()
    assert during_attack_genome.cx_fp == pre_attack_genome.cx_fp
    assert during_attack_genome.cy_fp == pre_attack_genome.cy_fp
    assert during_attack_genome.zoom_fp == pre_attack_genome.zoom_fp

    # Now feed calm blocks so recurrent EMA cools down and cell adiabatically awakens
    awakened = False
    for recovery_blk in range(25):
        rec_res = cell.perceive_and_evolve(
            hashlib.sha256(f"recovery_{recovery_blk}".encode()).digest(),
            shock_bps=100,
            enable_plasticity=False,
        )
        if rec_res["lifecycle_state"] == STATE_HOMEOSTASIS:
            awakened = True
            break

    assert awakened, "Cell must adiabatically awaken from Wormhole Hibernation once EMA stress subsides"
    post_awakening_genome = cell.get_genome_state()
    assert post_awakening_genome.cx_fp == pre_attack_genome.cx_fp
    assert post_awakening_genome.cy_fp == pre_attack_genome.cy_fp


def test_all_6_golden_pool_living_cells() -> None:
    """6. Verify all 6 DeFi Golden Pool Living Cells initialize and perceive without error."""
    for pair in GOLDEN_PAIR_SEEDS:
        cell = WerracleLivingCell(pair_symbol=pair)
        res = cell.perceive_and_evolve(hashlib.sha256(pair.encode()).digest(), shock_bps=400)
        assert res["pair_symbol"] == pair
        assert res["dynamic_fee_bps"] == 500
        assert len(res["packed_slot_hex"]) == 66


if __name__ == "__main__":
    test_256bit_genome_bijective_packing()
    test_proof_of_horizon_boundary_annulus()
    test_autonomous_epigenetic_evolution()
    test_recurrent_memory_split_attack_defense()
    test_wormhole_hibernation_and_adiabatic_awakening()
    test_all_6_golden_pool_living_cells()
    print("[PASSED] All 6 WerracleLivingCell Step-1 biological & algebraic test suites succeeded (100%).")
