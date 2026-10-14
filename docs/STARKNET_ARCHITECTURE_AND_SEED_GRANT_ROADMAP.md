# 🐺 Werracle on Starknet: STARK-Native Zero-Storage AI Reflex Oracle (Cairo 2.x / Sierra)
## Official Technical Architecture & Starknet Foundation Seed Grant Screening Dossier

* **Project:** Werracle (`werracle_starknet` v2.1.0)
* **Grant Track:** Starknet Foundation Seed Grant (Status: **🔬 In Screening** — Advanced Oct 14, 2026)
* **Lead Researcher:** Volkan Dağlı (`@pCwOrM`, ORCID: `0009-0000-1587-8703`)
* **Co-Researchers:** Zerrin Dağlı, Dağhan Dağlı (ITouch Systems Research Group — Çukurova Teknokent)
* **Cairo Package Path:** [`cairo/`](../cairo/) ([`Scarb.toml`](../cairo/Scarb.toml), [`werr_math.cairo`](../cairo/src/werr_math.cairo), [`werracle_tripod_zmod9.cairo`](../cairo/src/werracle_tripod_zmod9.cairo), [`ekubo_werracle_extension.cairo`](../cairo/src/ekubo_werracle_extension.cairo))
* **Machine-Checked Formal Verification:** Lean 4 (`v4.34.1`, Mathlib4, **40 Theorems, 0 `sorry` axioms**) — [`formal_proofs/`](../formal_proofs/)
* **Published Preprints:** [arXiv:2609.30719](https://arxiv.org/abs/2609.30719) &bull; [arXiv:2609.33066](https://arxiv.org/abs/2609.33066) &bull; [Zenodo 10.5281/zenodo.22942598](https://doi.org/10.5281/zenodo.22942598)

---

## 1. Why Starknet (CairoVM / Sierra) is the Natural Mathematical Home for Werracle

On Ethereum L1 and optimistic rollups, executing machine learning models requires external **ZK-ML provers** (e.g., EZKL, Modulus) that generate SNARK proofs off-chain over **10 to 300 seconds**, making them unusable for atomic, intra-block DeFi defense or real-time on-chain gaming.

**Starknet fundamentally changes the paradigm** because **every Starknet transaction is natively STARK-proven by the sequencer via CairoVM (Sierra $\rightarrow$ CASM)**. However, running conventional neural networks inside Cairo still hits two severe bottlenecks:
1. **State & L1 Blob Data Availability Costs:** Storing thousands of neural weight felts in Starknet contract storage incurs prohibitive `StorageAccess` and L1 state-diff costs.
2. **Cairo Trace Cell Blowup:** Matrix multiplications over large weight tensors consume millions of Cairo trace steps and range-check builtins, exceeding per-transaction step limits.

### The WERR Procedural Synthesis Solution on CairoVM
Instead of storing neural weight tensors, **Werracle** derives complex, non-linear decision hyperplanes procedurally from **Orbital Error Dynamics (OED)** along the Mandelbrot boundary $\partial\mathcal{M}$ ($z_{n+1} = z_n^2 + c$):
* **Single-`felt252` Coordinate Seed:** The entire model is parameterized by a 24-byte coordinate seed $\Theta = (c_x, c_y, \text{zoom})$ + 6 bytes of governance metadata (`nonce`, `threshold`, `mode`, `active`), totaling **240 bits**—fitting effortlessly inside a **single 251-bit Starknet `felt252`**!
* **Sierra-Safe Fuel-Bounded Recursion:** In Cairo 2.x (`werr_math.cairo`), our $\mathbb{Z}/9\mathbb{Z}$ harmonic tripod evaluates 12 orthogonal points across 3 concentric zoom planes ($0.60\times, 1.00\times, 1.60\times$) with a strict recursion bound of $n \le 9$ steps per point (**$\le 108$ global arithmetic cycles**).
* **Zero Dynamic Memory / Zero External Prover Latency:** Executes natively inside the Starknet sequencer's transaction lifecycle in **~1,420 Cairo steps (~$0.00004 in STRK)** with **100% native STARK validity**.

---

## 2. Three High-Impact Use Cases in the Starknet Ecosystem

```
                   ┌──────────────────────────────────────────────┐
                   │   WerracleTripodZMod9 (Cairo 2.x / Sierra)   │
                   │   24-Byte Seed Θ = (cx, cy, zoom) in felt252 │
                   │   12-Point Harmonic Tripod (Z mod 9, <=108)  │
                   └──────┬────────────────┬───────────────┬──────┘
                          │                │               │
        ┌─────────────────┘                │               └─────────────────┐
        ▼                                  ▼                                 ▼
┌───────────────────────────┐  ┌───────────────────────────┐  ┌───────────────────────────┐
│ 1. Ekubo Protocol v2      │  │ 2. Starknet Lending Guard │  │ 3. Dojo Autonomous Worlds │
│ (EkuboWerracleExtension)  │  │ (zkLend / Nostra / Vesu)  │  │ (On-Chain NPC Reflex AI)  │
├───────────────────────────┤  ├───────────────────────────┤  ├───────────────────────────┤
│ • Intra-block LVR &       │  │ • Atomic flash-loan &     │  │ • Sub-millisecond N-way   │
│   sandwich fee adaptation │  │   oracle manipulation     │  │   `decide_choice` &       │
│   (500 to 5000 pips)      │  │   circuit breaker (`noul`)│  │   `decide_noul` reflexes  │
│ • Zero multi-block        │  │ • Shock-accelerated early │  │ • Zero weight storage per │
│   routing blackout ($0)   │  │   escape at step n in {1,3}│  │   autonomous agent entity │
└───────────────────────────┘  └───────────────────────────┘  └───────────────────────────┘
```

### 2.1 Ekubo Protocol Singleton Extensions (`ekubo_werracle_extension.cairo`)
* **Problem:** Passive liquidity providers on `STRK/USDC`, `ETH/USDC`, and `WBTC/USDC` lose yield to CEX-DEX latency arbitrage (LVR). Stateful cooldown extensions that lock elevated fees across multiple blocks suffer from cheap "dust-trade griefing" (causing aggregators like AVNU and Fibrous to route organic volume away).
* **Werracle Solution:** `EkuboWerracleExtension` evaluates pool imbalance inside `before_swap_dynamic_fee` purely intra-block with **0 persistent state lockouts**, scaling swap fees between **0.05% (500 pips)** and **0.50% (5,000 pips)** while preserving 100% AVNU/Fibrous router liveness.

### 2.2 Atomic Flash-Loan Circuit Breakers for Starknet Lending (Vesu, Nostra, zkLend)
* By invoking `decide_noul(state_hash, risk_score_fp)`, lending pools obtain an atomic, STARK-proven boolean reflex gate (`allowed`, `confidence_bps`). Under extreme flash-loan anomalies, the $\mathbb{Z}/9\mathbb{Z}$ recurrence diverges at step $n \in \{1, 3\}$, **reducing Cairo step consumption by 28% during an active attack**.

### 2.3 Dojo Engine & On-Chain Autonomous Worlds (Zero-Storage Agent Brains)
* Starknet leads Web3 in fully on-chain games and autonomous worlds via **Dojo**. Giving 10,000 on-chain NPCs individual neural networks is impossible with tensor weights. With Werracle, **every Dojo entity stores its unique behavioral personality in a single `felt252` seed** and executes `decide_choice` (4-way or 8-way tactical action selection) in ~1,420 Cairo steps!

---

## 3. CairoVM vs. EVM vs. Off-Chain ZK-ML Benchmarks

| Metric | Off-Chain ZK-ML (EZKL / Giza) | Werracle on EVM (`WerracleTripodZMod9.sol`) | **Werracle on Starknet (`werracle_starknet` Cairo 2)** |
| :--- | :---: | :---: | :---: |
| **Cryptographic Proof** | External SNARK/STARK (Async) | None (Optimistic / L1 Consensus) | **100% Native STARK Proof (Sequencer)** |
| **Proving / Execution Latency** | 10 – 300 seconds | < 1 ms (Intra-block) | **< 1 ms (Intra-block Sierra Execution)** |
| **Model Weight Storage** | Megabytes (Off-chain) | 1 `bytes32` slot (24-byte seed) | **1 `felt252` word (240-bit packed seed)** |
| **Compute Cost per Inference** | 250,000 – 500,000 gas | 21,438 – 22,557 gas | **~1,420 Cairo Steps (~180 Range Checks)** |
| **Estimated L2 Tx Cost** | $0.05 – $0.50+ | ~$0.0005 | **~$0.00004 (< 0.001 STRK)** |
| **Formal Halting Guarantee** | Unverified Heuristics | Lean 4 Proven ($\le 108$ cycles) | **Lean 4 + Sierra Fuel-Bounded ($\le 108$ cycles)** |

---

## 4. 1-to-1 Formal Verification Parity (Lean 4 $\leftrightarrow$ Cairo Sierra)

Every Cairo function in [`cairo/src/werr_math.cairo`](../cairo/src/werr_math.cairo) is backed by our machine-checked **Lean 4 Master Proof Suite** ([`formal_proofs/`](../formal_proofs/), 40 Theorems, `0 sorry` axioms) and verified for bit-exact parity via [`tests/test_starknet_cairo_parity.py`](../tests/test_starknet_cairo_parity.py):

1. **`escape_halts_bounded` (Lean 4 Theorem 1 $\leftrightarrow$ `WerrMath::escape_zmod9`):** Proves `escape_zmod9(pt_cx, pt_cy) <= 9` for all $(c_x, c_y) \in \mathbb{Z}^2$, guaranteeing Sierra compilation without unbounded loop gas exhaustion.
2. **`tripod_point_count_invariant` & `global_execution_bound` (Lean 4 Theorems 2–3 $\leftrightarrow$ `WerrMath::evaluate_sparse_tripod`):** Proves that the 3-plane harmonic tripod executes at most $12 \times 9 = 108$ quadratic iterations per call.
3. **`ZModnZObj.isUnit_iff` (Lean 4 GAP-0331 Bridge $\leftrightarrow$ `is_zmod9_resonant_ideal` / `is_zmod9_coprime_unit`):** Formal algebraic partition of $\mathbb{Z}/9\mathbb{Z}$ into the resonant sub-ideal $I_3 = \{0, 3, 6\}$ and coprime error unit group $K_{\text{error}} = (\mathbb{Z}/9\mathbb{Z})^\times = \{1, 2, 4, 5, 7, 8\}$.

---

## 5. Starknet Seed Grant Execution Roadmap & Deliverables

| Milestone | Deliverable | Status |
| :--- | :--- | :---: |
| **Milestone 1: Core Cairo 2.x / Sierra Engine & Lean 4 Parity** | Complete `werracle_starknet` Scarb package (`werr_math.cairo`, `werracle_tripod_zmod9.cairo`), 100% bit-exact Python/Cairo/EVM parity harness (`tests/test_starknet_cairo_parity.py`), and 40-theorem Lean 4 formal verification suite. | ✅ **Completed & In Repo** |
| **Milestone 2: Ekubo Protocol Extension & Starknet Sepolia Deployment** | `EkuboWerracleExtension` (`ekubo_werracle_extension.cairo`) with pre-calibrated golden seeds for `STRK/USDC`, `ETH/USDC`, `WBTC/USDC`, and `EKUBO/ETH`; live contract deployment on Starknet Sepolia + AVNU routing compatibility verification. | 🔄 **Ready for Testnet Rollout** |
| **Milestone 3: Dojo Autonomous Agent SDK & Starknet Mainnet Launch** | Open-source TypeScript (`starknet.js`) & Dojo component adapter allowing Starknet dApps and on-chain games to invoke `decide_noul`, `decide_choice`, and `decide_score` with a single contract call. | 📅 **Scheduled (Weeks 5–8)** |
