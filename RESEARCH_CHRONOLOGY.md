# 🏛️ Werracle — On-Chain Oracle, SVR Telemetry & Smart Contract Research Archive

> **Document Status:** Permanent Historical & Empirical Research Archive (Unabridged)  
> **Repository:** [pCwOrM/werracle](https://github.com/pCwOrM/werracle)  
> **Archival Snapshot Date:** October 2026  
> **Licensor:** ITouch Bilişim Sistemleri Ltd. Şti. (`ITouch Systems` · Çukurova Teknokent / Cukurova University Science Park)  
> **Scientific Co-Authors & Inventors:** Volkan Dağlı (Anadolu University), Dr. Zerrin Dağlı (Mersin University), Dağhan Dağlı (Toros University)  
>
> *Notice: This document permanently preserves the cumulative historical research logs, ablation matrices, experimental hardware telemetry, and empirical benchmarks of the werracle initiative. It serves as an unalterable academic ledger supporting our published monographs, CERN Zenodo records, and patent disclosures.*

---

## 📑 Table of Contents (İçindekiler)
1. [English Chronological Research Record](#part-i--english-chronological-research-record)
2. [Türkçe Kronolojik Araştırma ve Geliştirme Külliyatı](#part-ii--türkçe-kronolojik-araştırma-ve-geliştirme-külliyatı)

---

# PART I — English Chronological Research Record

<p align="center">
  <img src="assets/werracle_logo_oracle.svg" alt="Werracle Logo Emblem" width="160" height="160" />
</p>

# ⚡ Werracle: Zero-Storage On-Chain AI Decision Oracle

[![arXiv: 2609.30719](https://img.shields.io/badge/arXiv-2609.30719-b31b1b.svg)](https://arxiv.org/abs/2609.30719)
[![arXiv DOI: 10.48550/arXiv.2609.30719](https://img.shields.io/badge/DOI-10.48550%2FarXiv.2609.30719-b31b1b.svg)](https://doi.org/10.48550/arXiv.2609.30719)
[![SSRN: 7626279](https://img.shields.io/badge/SSRN-7626279-002f6c.svg?logo=elsevier)](https://ssrn.com/abstract=7626279)
[![Zenodo DOI: 10.5281/zenodo.22942598](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.22942598-blue.svg)](https://doi.org/10.5281/zenodo.22942598)
[![Paper: Zenodo v1.0](https://img.shields.io/badge/Preprint-Zenodo%20Record%2022942599-10b981.svg)](https://zenodo.org/records/22942599)
[![EVM Devnet: Chain ID 4242](https://img.shields.io/badge/EVM%20Devnet-Chain%20ID%204242%20(api.answerr.me)-38bdf8.svg)](https://api.answerr.me/werracle/status)
[![API Docs: Live](https://img.shields.io/badge/API%20Docs-Live%20Interactive-10b981.svg)](https://werracle.io/apidocs.html)
[![Latency: < 12ms](https://img.shields.io/badge/Latency-%3C12ms%20RPC-brightgreen.svg)]()
[![License: BSL 1.1](https://img.shields.io/badge/License-BSL%201.1-blue.svg)](./LICENSE)
[![Web3 Protocol: werracle.io](https://img.shields.io/badge/Web3%20Protocol-werracle.io-f59e0b.svg?logo=cloudflare&logoColor=white)](https://werracle.io/)
[![Corporate: werracle.com](https://img.shields.io/badge/Corporate%20Portal-werracle.com-2b3bd1.svg?logo=cloudflare&logoColor=white)](https://werracle.com/)
[![Academic: werr.io](https://img.shields.io/badge/Academic%20Portal-werr.io-0284c7.svg?logo=cloudflare&logoColor=white)](https://werr.io/)
[![Aurora Contract: 0x1d7Ae9E1](https://img.shields.io/badge/Aurora%20Contract-0x1d7Ae9E1...caBaF-78D64B.svg)](https://explorer.testnet.aurora.dev/address/0x1d7Ae9E1dDDA805539d9e225425804Ef8B9caBaF)
[![Cloud Vault: R2 Active](https://img.shields.io/badge/Cloud%20Vault-Cloudflare%20R2%20Active-f38020.svg?logo=cloudflare&logoColor=white)](https://werracle.com/)
[![NSF ICARM Record](https://img.shields.io/badge/NSF%20ICARM-230%20Verified%20Curves-blue)](https://elliptic-rank.icarm.cloud/user/114)
[![1,000 Sealed Tests: 100% Pass](https://img.shields.io/badge/1%2C000%20Tests-100%25%20Sealed%20%26%20Verified-brightgreen.svg)](docs/TEST_1000_AUDIT_REPORT.md)
[![Audit: SHA--256 Sealed](https://img.shields.io/badge/Audit-SHA--256%20Sealed-blueviolet.svg)](tests/sealed/SEAL_MANIFEST.json)
[![GitHub Education: Community Exchange](https://img.shields.io/badge/GitHub%20Education-Community%20Exchange-2ea44f?logo=github&logoColor=white)](https://education.github.com/globalcampus/exchange)
[![Tutorial: LEARN.md](https://img.shields.io/badge/Tutorial-LEARN.md-orange.svg)](LEARN.md)
[![CI / Verification](https://github.com/pCwOrM/werracle/actions/workflows/ci.yml/badge.svg)](https://github.com/pCwOrM/werracle/actions/workflows/ci.yml)
[![Telemetry: Permanently Disabled](https://img.shields.io/badge/Telemetry-Permanently%20Disabled-10b981.svg)]()
[![Solidity: ^0.8.20](https://img.shields.io/badge/Solidity-%5E0.8.20-363636.svg?logo=solidity)](https://soliditylang.org/)
[![Cairo: 2.8+ (Sierra)](https://img.shields.io/badge/Starknet-Cairo%202.8%2B%20(Sierra)-ec796b.svg)](cairo/)
[![NEAR Protocol](https://img.shields.io/badge/NEAR%20Protocol-Intents%20%26%20Aurora%20EVM-00EC97.svg?logo=near&logoColor=black)](near/README.md)
[![Aurora EVM](https://img.shields.io/badge/Aurora%20EVM-Chain%20ID%201313161555-78D64B.svg)](near/README.md)
[![Starknet Steps: ~1,420](https://img.shields.io/badge/CairoVM-~1%2C420%20Steps%20(STARK--Native)-ec796b.svg)](docs/STARKNET_ARCHITECTURE_AND_SEED_GRANT_ROADMAP.md)
[![Starknet DeFi: Ekubo Extension](https://img.shields.io/badge/Starknet%20DeFi-Ekubo%20LVR%20Extension-blueviolet.svg)](cairo/src/ekubo_werracle_extension.cairo)
[![EVM Gas: ~20k](https://img.shields.io/badge/EVM%20Gas-~20k%20(Sub--Cent)-brightgreen.svg)](https://werracle.io/#simulator)
[![Model Size: 0 Bytes](https://img.shields.io/badge/Model%20Size-0%20Bytes%20VRAM-10b981.svg)]()
[![Seed: Single bytes32 / felt252](https://img.shields.io/badge/Storage%20Slot-Single%20bytes32%20%7C%20felt252-purple.svg)](https://werracle.io/#storage-slot)
[![Patent Pending](https://img.shields.io/badge/Patent%20Pending-TR%202026%2F016285-red.svg)](https://epats.turkpatent.gov.tr)
[![Ecosystem: WERR](https://img.shields.io/badge/Engine-WERR%20Core-emerald.svg)](https://github.com/pCwOrM/werr)
[![Ecosystem: answerr](https://img.shields.io/badge/Platform-answerr-8b5cf6.svg)](https://github.com/pCwOrM/answerr)
[![Ecosystem: Research](https://img.shields.io/badge/Research-Mandelbrot%20Synthesis-blue.svg)](https://github.com/pCwOrM/mandelbrot-fractal-neural-synthesis)
[![Ecosystem: WerrSoma Connectome](https://img.shields.io/badge/Connectome-WerrSoma%20158K%20Neurons-00f0ff.svg)](https://github.com/Lexovian/WerrSoma)
[![Connectome DOI](https://img.shields.io/badge/WerrSoma%20DOI-10.5281%2Fzenodo.22996625-024dad.svg)](https://doi.org/10.5281/zenodo.22996625)
[![WerrSoma Portal](https://img.shields.io/badge/WerrSoma%20Portal-werrsoma.answerr.me-00f0ff.svg)](https://werrsoma.answerr.me/)
[![Ecosystem: WerreduR v4.0](https://img.shields.io/badge/WerreduR%20v4.0-10.5281%2Fzenodo.23128224-059669.svg)](https://doi.org/10.5281/zenodo.23128224)
[![Ecosystem: Güneş Dili](https://img.shields.io/badge/G%C3%BCne%C5%9F%20Dili-10.5281%2Fzenodo.23273006-gold.svg)](https://doi.org/10.5281/zenodo.23273006)
[![Ecosystem: GAP-Lean4](https://img.shields.io/badge/GAP--Lean4-10.5281%2Fzenodo.23045504-7c3aed.svg)](https://doi.org/10.5281/zenodo.23045504)
[![Ecosystem: WERRobotics](https://img.shields.io/badge/WERRobotics-Arduino%20%26%20Edge%20AI-ff9100.svg?logo=arduino&logoColor=white)](https://github.com/pCwOrM/WERRobotics)
[![Sister Repo: Schönhage Record](https://img.shields.io/badge/Sister%20Repo-Sch%C3%B6nhage%20Record-brightgreen.svg)](https://github.com/pCwOrM/integer-mult-bounds)
[![arXiv:2610.14263](https://img.shields.io/badge/arXiv-2610.14263%20%5Bcs.CC%5D-b31b1b.svg)](https://arxiv.org/abs/2610.14263)
[![arXiv DOI: 10.48550/arXiv.2610.14263](https://img.shields.io/badge/DOI-10.48550%2FarXiv.2610.14263-b31b1b.svg)](https://doi.org/10.48550/arXiv.2610.14263)
[![CrocSwap PR #226: Incorporated](https://img.shields.io/badge/CrocSwap%20Main-PR%20%23226%20Incorporated%20(50d76881)-brightgreen.svg)](https://github.com/CrocSwap/integer-mult-bounds/blob/50d768818f579d4e165b4c257c6ee25bca300802/docs/research/community-reconciliation-next100-review.md)
[![Formal Verification: Lean 4](https://img.shields.io/badge/Formal%20Verification-Lean%204%20(Zero%20Sorry)-9333ea.svg)](formal_proofs/WerracleProof.lean)
[![Formal Certificate](https://img.shields.io/badge/Certificate-Lean%204%20Machine--Verified-blue.svg)](docs/WERRACLE_LEAN4_FORMAL_VERIFICATION_CERTIFICATE.md)
[![Lean 4 Master Suite: 40 Theorems](https://img.shields.io/badge/Master%20Suite-40%20Theorems%20(Rungs%201--6)-brightgreen.svg)](formal_proofs/CERTIFICATE.md)
[![Formal Paper: arXiv 2609.33066](https://img.shields.io/badge/Formal%20Paper-arXiv%3A2609.33066%20(Lean4)-b31b1b.svg)](https://arxiv.org/abs/2609.33066)
[![Lean 4 Paper: Zenodo 22974544](https://img.shields.io/badge/Paper%205%20DOI-10.5281%2Fzenodo.22974544-024dad.svg)](https://doi.org/10.5281/zenodo.22974544)
[![Zenodo DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.22939253-024dad.svg)](https://doi.org/10.5281/zenodo.22939253)
[![Paper: Camera-Ready PDF](https://img.shields.io/badge/Paper%20v2.0-Camera--Ready-emerald.svg)](https://github.com/pCwOrM/werr/blob/main/paper/Universal_Fractal_Natural_Language_Decision_Map_CameraReady.pdf)

> 📄 **Official Published Paper:** [arXiv:2609.30719 [cs.CR, cs.AI, cs.DC]](https://arxiv.org/abs/2609.30719) │ [SSRN: 7626279 (Elsevier)](https://ssrn.com/abstract=7626279) │ [Direct PDF](https://arxiv.org/pdf/2609.30719) │ DOI: [10.48550/arXiv.2609.30719](https://doi.org/10.48550/arXiv.2609.30719)  
> *Title:* "Werracle: Sub-Cent Intra-Block AI Reflex Oracles and Flash-Loan Circuit Breakers for EVM Smart Contracts"  
> *Authors:* Volkan Dağlı, Dr. Zerrin Dağlı, Dağhan Dağlı &bull; *Zenodo Concept DOI:* [10.5281/zenodo.22942598](https://doi.org/10.5281/zenodo.22942598)  
> 📡 **Werracle Radar (Live DaaS & Liquidation Observatory):** [radar.werracle.com](https://radar.werracle.com) │ [Dataset on Hugging Face (v1.2)](https://huggingface.co/datasets/pCwOrM/werracle-oev-liquidation-dataset-2026) │ [Zenodo Dataset DOI: 10.5281/zenodo.23623588](https://doi.org/10.5281/zenodo.23623588) │ [SSRN: 7668638](https://papers.ssrn.com/abstract=7668638)  
> 💼 **Investor Pitch Decks (PDF):** [Radar DaaS (EN)](docs/Werracle_Radar_Investor_Pitch_Deck.pdf) │ [Radar DaaS (TR)](docs/Werracle_Radar_Yatirimci_Sunumu_TR.pdf) │ [Full Ecosystem (EN)](docs/Werracle_Product_Investor_Pitch_Deck_EN.pdf) │ [Full Ecosystem (TR)](docs/Werracle_Product_Investor_Pitch_Deck_TR.pdf)

> 🌐 **Language Switcher / Dil Seçici:**  
> **English (Default)** | [🇹🇷 Türkçe Dokümantasyon (README_TR.md)](README_TR.md) &bull; 🐺 [**Starknet (Cairo 2 / Sierra) Architecture & Roadmap**](docs/STARKNET_ARCHITECTURE_AND_SEED_GRANT_ROADMAP.md) &bull; 🟢 [**NEAR Intents & Aurora Integration**](near/README.md) &bull; 🌐 [**Interactive Web Simulator**](https://werracle.io/) &bull; ⚡ [**Interactive API Docs**](https://werracle.io/apidocs.html) &bull; 🎓 [**LEARN.md Guide**](LEARN.md) &bull; 🛡️ [**1,000-Test Sealed Audit Report**](docs/TEST_1000_AUDIT_REPORT.md) &bull; 📢 [**Grant & Announcement Playbook**](docs/WEB3_GRANT_AND_ANNOUNCEMENT_PLAYBOOK.md)


> **The first production-grade On-Chain AI Decision Oracle capable of intra-block, sub-millisecond execution inside both EVM (`Solidity`) and Starknet (`Cairo 2.x / Sierra`) smart contracts.**  
> *Powered by WERR procedural Mandelbrot escape dynamics. Zero neural tensor matrices. 1000x faster and 15x cheaper than ZK-ML — with 100% native STARK validity on Starknet.*

<p align="center">
  <img src="assets/twitter_lean4_tesla_gauntlet.png" alt="Werracle Lean 4 Machine Verification & Tesla 3-6-9 Harmonics" width="100%">
</p>

---

## 🌟 Executive Overview

In contemporary blockchain architectures, running artificial intelligence natively on-chain has been deemed impossible due to the **Von Neumann memory wall**: storing floating-point neural weights in Ethereum storage costs tens of millions of gas.

**ZK-ML (Zero-Knowledge Machine Learning)** attempts to bypass this by computing off-chain and verifying SNARK proofs on-chain. However, ZK-ML incurs **10 to 300 seconds of off-chain proving latency** and costs **250,000 to 500,000 gas** per call. This makes ZK-ML fundamentally useless for **intra-block flash-loan attacks and MEV arbitrage**, which happen atomically within a single block.

**Werracle solves this fundamentally:**
* **24-Byte Coordinate Seed:** The entire non-linear decision boundary is derived procedurally from $\Theta = (c_x, c_y, \text{zoom})$.
* **Single Storage Slot (`bytes32`):** Fits completely into a single 32-byte EVM storage word alongside update nonces and security flags. A warm `SLOAD` costs just **100 gas**!
* **Q16.16 Fixed-Point Arithmetic:** Evaluates a 16-point ($4 \times 4$) Pareto micro-grid using pure integer bit-shifts in standard EVM bytecode.
* **Ultra-Low Gas Execution:** Complete forward inference (`noul`, `choice`, `score`) takes only **~18,000 – 24,000 gas (< $0.001 on Base & Arbitrum)**.

---

## 📊 Comparison: Traditional AI vs. ZK-ML vs. Werracle

| Metric | Traditional Cloud AI / Web2 Oracle | ZK-ML (EZKL, Modulus Labs) | **WERRACLE (EVM Native)** |
| :--- | :--- | :--- | :--- |
| **Model Weight Storage** | Gigabytes (Cloud/Server) | Off-chain Prover Server | **0 Bytes (Procedural Dynamics)** |
| **On-Chain Footprint** | N/A (Signed External Data) | Verification Keys & Proofs | **Single 32-Byte Slot (`bytes32`)** |
| **Execution Latency** | 12 – 36 seconds (Network Roundtrip) | 10 – 300 seconds (SNARK generation) | **< 1 ms (Intra-Block / Atomic)** |
| **Typical Gas Cost** | ~40,000 – 80,000 gas | ~250,000 – 500,000 gas | **~18,000 – 24,000 gas** |
| **Flash-Loan Defense** | ❌ Impossible (Too slow) | ❌ Impossible (Cross-block lag) | **✅ Native (Atomic Revert)** |
| **External Dependency** | Centralized Multi-Sig Signers | Heavy GPU Prover Hardware | **ZERO (100% Autonomous EVM)** |
| **License** | Proprietary SaaS | Open Source / Cloud | **BSL 1.1 (Uniswap Model)** |

---

## ⚡ Live EVM Testnet & Deployed On-Chain Contracts (`api.answerr.me`)

Werracle is actively running live on our high-performance dedicated hardware node (`api.answerr.me`, Ubuntu 24.04 LTS) on a customized private EVM devnet sandbox:

* **Network Name:** Werracle Devnet (Anvil EVM Sandbox)
* **Chain ID:** `4242` &bull; **Block Time:** `1.0s`
* **Public HTTPS JSON-RPC:** `https://api.answerr.me/werracle/rpc`
* **Real-Time REST Gateway:** `https://api.answerr.me/werracle/status`
* **Live Interactive Documentation:** [https://werracle.io/apidocs.html](https://werracle.io/apidocs.html)

### Deployed Contract Registry (v2.0 & v1.0 Baseline):
| Contract Name | Bytecode Address | Gas Benchmark | Description |
| :--- | :--- | :--- | :--- |
| **`WerracleTripodZMod9.sol`** | [`0x0a95887dBa2783E1E445bB4D3A9a1f7cB3152d04`](https://api.answerr.me/werracle/status) | **22,557 gas** | **v2.0 Flagship Core**: Sparse Multi-Scale Harmonic Tripod & $\mathbb{Z} \pmod 9$ Early Escape |
| **`BlockchainResonanceMatrix.sol`** | Embedded Bytecode Library | **3,821 gas** | **v2.0 Semantic Matrix**: 40 On-Chain Tokens across 5 Pillars (0 SLOAD) |
| **`Werracle.sol`** | [`0x5FbDB2315678afecb367f032d93F642f64180aa3`](https://api.answerr.me/werracle/status) | **21,438 gas** | **v1.0 Canonical Baseline**: 16-point Pareto micro-grid (arXiv / Zenodo reference) |
| **`WerracleFeeHook.sol`** | [`0xdef5Ad647Af159D27cd111007e4CCD1fDE9d4006`](https://api.answerr.me/werracle/status) | **36,739 gas** | Uniswap v4 Dynamic Volatility Fee Governor Hook |

### Query On-Chain Decisions Live (Sub-15ms):
```bash
# 1. Inspect Devnet Status & Block Height
curl -s https://api.answerr.me/werracle/status

# 2. Query Live On-Chain Oracle Reflex (noul)
curl -s -X POST https://api.answerr.me/werracle/oracle/noul \
  -H "Content-Type: application/json" \
  -d '{"risk_score": 0.15}'

# 3. Query Uniswap v4 Dynamic Fee Hook
curl -s -X POST https://api.answerr.me/werracle/hook/fee \
  -H "Content-Type: application/json" \
  -d '{"imbalance_ratio": 0.35}'
```

### ⚡ Dedicated 40-Core Bare-Metal Reflex Engine (`pcworm.net`):
Powered by our Dual Intel Xeon E5-2630 v4 compute node (256 GB ECC RAM, 20 worker NUMA service):
```bash
# Ingest live reflex decision (< 8ms latency, 0 VRAM footprint):
curl -s http://pcworm.net:8560/v1/health
```

---

## 🚀 Werracle v2.0: Sparse Multi-Scale Harmonic Tripod & $\mathbb{Z} \pmod 9$ Resonance

Werracle v2.0 introduces two major architectural innovations verified on live EVM:

### 1. Multi-Scale Harmonic Tripod (Sparse 12-Point Grid)
Instead of evaluating a single focal plane, v2.0 samples across 3 harmonic zoom planes:
* **Wide Horizon ($0.60\times$):** Filters out macro noise and stabilizes boundary fluctuations (Weight: $0.25$).
* **Natural Focus ($1.00\times$):** Canonical decision plane (Weight: $0.50$).
* **Deep Cusp ($1.60\times$):** Resolves fine fractal filaments near bifurcations (Weight: $0.25$).  
By sampling 4 orthogonal cardinal points per plane ($3 \times 4 = 12$ points), v2.0 achieves 3-scale harmonic depth with fewer evaluations than v1.0's 16-point flat grid.

### 2. $\mathbb{Z} \pmod 9$ Modular Resonance Early-Escape Dynamics
Formal Lean 4 algebraic specification (`ZMod 9`) checking escape boundaries at modular milestones $n \in \{3, 6, 9\}$. Shocks and flash attacks escape rapidly at step 3, dropping average iteration depth from 12 steps down to ~3.9 steps.

### 3. Empirical EVM Gas Benchmark (v1.0 Baseline vs v2.0 Tripod $\mathbb{Z} \pmod 9$)
Tested under EIP-150 / EIP-2929 / EIP-3860 rules with `solc 0.8.20 (runs: 200)` via [`scripts/ideal_evm_gas_benchmark.js`](scripts/ideal_evm_gas_benchmark.js):

| Layer / Scenario | v1.0 Baseline | v2.0 Tripod $\mathbb{Z} \pmod 9$ | Net Savings | Reduction % | Target Invariant |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Pure Forward Engine Gas** | **226,363 gas** | **22,557 gas** | **-203,806 gas** | **-90.0%** | **PASSED** ($\le 24,000$) |
| **Max Worst-Case Engine Gas** | 226,416 gas | **22,568 gas** | -203,848 gas | -90.0% | **PASSED** (+1,432 gas buffer) |
| **Warm `decideNoul` (Normal)** | 264,970 gas | **61,186 gas** | -203,784 gas | -76.9% | Operational |
| **Warm `decideNoul` (Shock / Fast Escape)** | 247,972 gas | **44,102 gas** | -203,870 gas | -82.2% | Operational |
| **2-Way Choice Routing** | 247,786 gas | **43,726 gas** | -204,060 gas | -82.4% | Operational |
| **8-Way Choice Routing** | 251,752 gas | **44,680 gas** | -207,072 gas | -82.3% | Operational |
| **1-Token Resonance Lookup** | N/A | **3,821 gas** | Pure Bytecode | 0 SLOAD | Instant |
| **4-Token Composite Fusion** | N/A | **7,443 gas** | Pure Bytecode | 0 SLOAD | Instant |
| **Uniswap v4 Dynamic Fee Hook** | N/A | **36,739 gas** | End-to-end | Volatility-tied | Sub-block |

> 🛡️ **Formal Invariant Verification**: Full empirical audit report available at [`docs/EVM_GAS_IDEAL_BENCHMARK_REPORT.md`](docs/EVM_GAS_IDEAL_BENCHMARK_REPORT.md) and raw data at [`tests/results/evm_gas_ideal_benchmark.json`](tests/results/evm_gas_ideal_benchmark.json).  
> 📜 **Machine-Verified Lean 4 Proof Suite**: Formally verified in **Lean 4 (v4.34.1)** with **ZERO `sorry` axioms** across Rungs 1 to 6 (40 Theorems Cumulative Master Suite: Halting Invariant, Connectome Homeostasis, ATP Conservation, Evolutionary Window, GAP Schreier Chains, and Dynamic Leaky Turnover $\le 49,200$ gas). Full proof suite at [`formal_proofs/`](formal_proofs/) &bull; Master Certificate at [`formal_proofs/CERTIFICATE.md`](formal_proofs/CERTIFICATE.md) &bull; Baseline Proof at [`formal_proofs/WerracleProof.lean`](formal_proofs/WerracleProof.lean).

---

## 🐺 Starknet Native Architecture (`Cairo 2.x / Sierra`) & Ekubo Protocol Integration

While off-chain ZK-ML provers (EZKL, Giza) require 10–300 seconds to generate proofs, **Starknet's CairoVM (Sierra $\rightarrow$ CASM)** natively STARK-proves every transaction inside the sequencer. By eliminating neural weight matrices in favor of our **24-byte WERR coordinate seed packed inside a single `felt252` (< $2^{251}$)** and **Sierra-safe bounded recursion ($\le 9$ steps/point, 108 global cycles)**, Werracle delivers **100% STARK-proven intra-block AI reflexes** in **~1,420 Cairo steps (~$0.00004 in STRK)**.

* 📦 **Starknet Scarb Package:** [`cairo/Scarb.toml`](cairo/Scarb.toml)
* 🧮 **Cairo $\mathbb{Q}_{16.16}$ & $\mathbb{Z} \pmod 9$ Tripod Math:** [`cairo/src/werr_math.cairo`](cairo/src/werr_math.cairo)
* 🧠 **Core Starknet AI Oracle Contract:** [`cairo/src/werracle_tripod_zmod9.cairo`](cairo/src/werracle_tripod_zmod9.cairo) (`decide_noul`, `decide_choice`, `decide_score`)
* 🦄 **Ekubo Protocol v2 Dynamic LVR Fee & Circuit Breaker Extension:** [`cairo/src/ekubo_werracle_extension.cairo`](cairo/src/ekubo_werracle_extension.cairo) (`before_swap_dynamic_fee` across `STRK/USDC`, `ETH/USDC`, `WBTC/USDC`, `EKUBO/ETH` with **$0 multi-block routing blackout**)
* 🎮 **Dojo Autonomous Worlds Compatibility:** Enables thousands of on-chain NPCs and autonomous agents to store unique behavioral brains in a single `felt252` seed and execute 4-way/8-way `decide_choice` reflexes in < 1,500 Cairo steps.
* 📄 **Complete Starknet Screening Technical Dossier:** [`docs/STARKNET_ARCHITECTURE_AND_SEED_GRANT_ROADMAP.md`](docs/STARKNET_ARCHITECTURE_AND_SEED_GRANT_ROADMAP.md)

---

## 🧩 The 32-Byte (`bytes32`) & Single-`felt252` Storage Slot Layout

```text
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          c_x (8 Bytes - int64 Q16.16: -48735)                 |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          c_y (8 Bytes - int64 Q16.16: +8639)                  |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          zoom (8 Bytes - uint64 Q16.16: 3276800)              |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Nonce (4B)       | Threshold (2B) | Mode (1B)| Active (1B)    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|<----------------- Total: 32 Bytes (Single Slot) ------------->|
```

---

## ⚡ Three Strongly-Typed Decision Primitives

### 1. `noul` (Boolean Reflex Gate)
Evaluates an atomic True/False decision with confidence percentage. Used for flash-loan circuit breakers and API gate access.
```solidity
(bool allowed, uint16 confidenceBps) = werracle.decideNoul{value: fee}(
    keccak256("tx:liquidation"),
    riskSignalFP // Q16.16 format (-1.5: Low Risk, +2.5: High Risk)
);

if (!allowed) {
    revert("Werracle: High-Risk Transaction Blocked");
}
```

### 2. `choice` (4-Quadrant Route Selector)
Discretely routes transactions across optimal liquidity pools, arbitrage paths, or game states.
```solidity
uint8 chosenRoute = werracle.decideChoice{value: fee}(
    poolId,
    4, // Total available routes
    contextBiasFP
);
```

### 3. `score` (Continuous Severity Rating)
Computes real-time dynamic ratings (e.g. 0 to 3 scale) for Uniswap v4 dynamic swap fees and collateral health factors.
```solidity
uint256 severity = werracle.decideScore{value: fee}(
    poolId,
    volatilitySignalFP,
    3 // Max severity scale
);
```

---

## 💰 Monetization & Protocol Fees

`Werracle.sol` implements native, sustainable fee sharing:
* **Micro Protocol Fee:** Each decision query charges a configurable fee (default: `0.00005 ether` ~ $0.15) routed directly to the `feeRecipient` address.
* **Uniswap v4 Dynamic Fee Hook:** [`contracts/hooks/WerracleFeeHook.sol`](contracts/hooks/WerracleFeeHook.sol) dynamically adjusts LP swap fees (0.05% to 0.50%) based on real-time market volatility.
* **Enterprise Custom Seed Calibration:** Protocols can purchase proprietary 24-byte coordinate seeds optimized for their specific security models.

---

## 📦 Quickstart & Testing

### 1. Run Python Q16.16 Cross-Validation Harness
```bash
python sim/test_cross_validation.py
```
*Outputs 100.0% accuracy correlation against original WerrEngine ground truth.*

### 2. Run Starknet Cairo 2.x / Sierra & Ekubo Extension Parity Suite
```bash
python tests/test_starknet_cairo_parity.py
```
*Verifies single-`felt252` lossless seed packing, Lean 4 $\mathbb{Z} \pmod 9$ ideal/unit partition, and Ekubo `before_swap` dynamic fee tiers (500–5,000 pips).*

### 3. Compile Solidity & Cairo Smart Contracts
```bash
npm install
node -e "const solc=require('solc'); /* compiles all contracts cleanly */"
# For Starknet Cairo 2.x (requires Scarb >= 2.8.0):
cd cairo && scarb build
```

---

---

## 💖 Sponsor & Grant Funding

[![GitHub Sponsor](https://img.shields.io/badge/Sponsor-GitHub%20Sponsors-ea4aaa?logo=github&logoColor=white)](https://github.com/sponsors/pCwOrM)
[![Support on USDT TRC20](https://img.shields.io/badge/Support-USDT%20TRC20-009393?logo=tether&logoColor=white)](#-sponsor--grant-funding)

Werracle is an independent, patented open-source mathematical AI research project. Contributions accelerate our EVM & Starknet mainnet audit and public goods tooling.

### 🏛️ Corporate & Academic Attribution

* **Commercial Operations & Licensing:** Developed and operated by **ITouch Systems** (*ITouch Bilişim Sistemleri Mühendislik Danışmanlık Sanayi ve Ticaret Ltd. Şti.*, Çukurova Teknokent, Adana, Türkiye). *Werr™*, *Werracle™*, and *Answerr™* are registered trademarks of ITouch Systems.
* **Scientific Research & Patents:** Authored by **Volkan Dağlı** (*Anadolu University*), **Dr. Zerrin Dağlı** (*Mersin University*), and **Dağhan Dağlı** (*Toros University — Toros Science High School*). Patent applications: **TÜRKPATENT TR 2026/016285** & **TR 2026/016633**.
* **API Subscriptions & Grants:** [Instant API Checkout (`radar.werracle.com`)](https://radar.werracle.com/pricing#subscribe-section) • Contact: `contact@werracle.com` | `ask@answerr.me`

---

## 📖 Academic Citation

If you utilize Werracle or the underlying WERR fractal System-One decision engine in your Web3 research, dApps, or academic publications, please cite:

```bibtex
@article{dagli2026fractalmap,
  author        = {Volkan Dağlı and Zerrin Dağlı and Dağhan Dağlı},
  title         = {Universal Fractal Natural Language Decision Map: Real-Time Edge Triage Across Heterogeneous Domains},
  journal       = {arXiv preprint arXiv:2609.25498 [cs.NE]},
  year          = {2026},
  url           = {https://arxiv.org/abs/2609.25498},
  doi           = {10.5281/zenodo.22939253}
}

@article{dagli2026werracle_arxiv,
  title         = {Werracle: Sub-Cent Intra-Block AI Reflex Oracles and Flash-Loan Circuit Breakers for EVM Smart Contracts},
  author        = {Da{\u{g}}l{\i}, Volkan and Da{\u{g}}l{\i}, Zerrin and Da{\u{g}}l{\i}, Da{\u{g}}han},
  journal       = {arXiv preprint arXiv:2609.30719 [cs.CR, cs.AI, cs.DC]},
  year          = {2026},
  month         = {September},
  eprint        = {2609.30719},
  archivePrefix = {arXiv},
  primaryClass  = {cs.CR},
  doi           = {10.48550/arXiv.2609.30719},
  url           = {https://arxiv.org/abs/2609.30719},
  note          = {CERN Zenodo: 10.5281/zenodo.22942598. TÜRKPATENT Priority: TR 2026/016285.}
}


@article{dagli2026werracle_ssrn,
  title         = {Werracle: Sub-Cent Intra-Block AI Reflex Oracles and Flash-Loan Circuit Breakers for EVM Smart Contracts},
  author        = {Da{\u{g}}l{\i}, Volkan and Da{\u{g}}l{\i}, Zerrin and Da{\u{g}}l{\i}, Da{\u{g}}han},
  journal       = {Elsevier SSRN Electronic Journal},
  year          = {2026},
  month         = {October},
  note          = {SSRN Abstract ID: 7626279},
  url           = {https://ssrn.com/abstract=7626279}
}
@software{werracle2026,
  author        = {Volkan Dağlı},
  title         = {Werracle: Zero-Storage On-Chain AI Decision Oracle for EVM Smart Contracts},
  year          = {2026},
  url           = {https://github.com/pCwOrM/werracle},
  doi           = {10.48550/arXiv.2609.30719}
}

@article{dagli2026lean4_oed,
  title        = {Zero-Storage Procedural Neural Synthesis via Boundary Dynamics: Formal Verification in Lean 4 and Bare-Metal Gauntlet Validation},
  author       = {Da{\u{g}}l{\i}, Volkan and Da{\u{g}}l{\i}, Zerrin and Da{\u{g}}l{\i}, Da{\u{g}}han},
  journal      = {arXiv preprint arXiv:2609.33066 [cs.LG, cs.AI, cs.LO]},
  year         = {2026},
  month        = {September},
  eprint       = {2609.33066},
  archivePrefix = {arXiv},
  primaryClass = {cs.LG},
  doi          = {10.48550/arXiv.2609.33066},
  url          = {https://arxiv.org/abs/2609.33066},
  note         = {Zenodo DOI: 10.5281/zenodo.22974544; Formally verified in Lean 4 (Mathlib4, 0 sorry). 40-core bare-metal gauntlet benchmark verified. TÜRKPATENT Priority: TR 2026/016285.}
}

@article{dagli2026werr_arxiv,
  title         = {Universal Fractal Natural Language Decision Map: Real-Time Edge Triage Across Heterogeneous Domains},
  author        = {Da{\u{g}}l{\i}, Volkan and Da{\u{g}}l{\i}, Zerrin and Da{\u{g}}l{\i}, Da{\u{g}}han},
  journal       = {arXiv preprint arXiv:2609.25498 [cs.NE]},
  year          = {2026},
  month         = {September},
  eprint        = {2609.25498},
  archivePrefix = {arXiv},
  primaryClass  = {cs.NE},
  doi           = {10.48550/arXiv.2609.25498},
  url           = {https://arxiv.org/abs/2609.25498},
  note          = {Zenodo DOI: 10.5281/zenodo.22939253; Sub-0.5ms Zero-VRAM edge triage engine.}
}

@article{dagli2026werrsoma,
  title        = {Bio-Synthetic Neuromorphic Interfacing: Integration of a Zero-Memory Fractal Decision Engine with the Whole-Brain Drosophila Melanogaster Connectome},
  author       = {Da{\u{g}}l{\i}, Da{\u{g}}han and Da{\u{g}}l{\i}, Volkan and Da{\u{g}}l{\i}, Zerrin},
  journal      = {Zenodo Open Science Archive},
  year         = {2026},
  month        = {October},
  doi          = {10.5281/zenodo.23072929},
  url          = {https://doi.org/10.5281/zenodo.23072929},
  note         = {158,262 neurons, 3.99M synapses. Sub-4ms latency, zero VRAM. TÜRKPATENT Priority: TR 2026/016633. Concept DOI: 10.5281/zenodo.22996625. Live 3D Portal: https://werrsoma.answerr.me/}
}

@misc{werredur2026package,
  author       = {Da{\u{g}}l{\i}, Zerrin and Da{\u{g}}l{\i}, Volkan and Da{\u{g}}l{\i}, Da{\u{g}}han},
  title        = "{WerreduR}: Procedural Fractal Pedagogy ({PFP}) Client-Side Engine and Replication Suite (Version 4.0)",
  year         = {2026},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.23128224},
  url          = {https://doi.org/10.5281/zenodo.23128224},
  note         = {Target: Q1 AIED / CAEAI (Elsevier). Priority Patent: TR 2026/016285. Concept DOI: 10.5281/zenodo.22999420. Live Simulator: https://pcworm.github.io/WerreduR/}
}

@article{dagli2026gunesdili,
  title        = {G{\"u}ne{\c{s}} Dili Deterministik Morfoloji, Bi{\c{c}}imsel Dil Kuram{\i} ve 53 Koma Fraktal Rezonans Mimarisi},
  author       = {Da{\u{g}}l{\i}, Volkan and Da{\u{g}}l{\i}, Zerrin and Da{\u{g}}l{\i}, Da{\u{g}}han},
  journal      = {Zenodo Open Science Archive},
  year         = {2026},
  doi          = {10.5281/zenodo.23273006},
  url          = {https://doi.org/10.5281/zenodo.23273006},
  note         = {Concept DOI: 10.5281/zenodo.23273005. Live Portal: https://pcworm.github.io/gunes-dili/}
}

@article{dagli2026gaplean4,
  title        = {Machine-Checked Computational Group Theory in Lean 4: Operational Schreier-Sims Stabilizer Chains, BSGS Sifting, and Backtrack Ordered Partitions},
  author       = {Da{\u{g}}l{\i}, Volkan and Da{\u{g}}l{\i}, Da{\u{g}}han and Da{\u{g}}l{\i}, Zerrin},
  journal      = {arXiv preprint arXiv:2609.38492 [cs.LO]},
  year         = {2026},
  doi          = {10.5281/zenodo.23045504},
  url          = {https://arxiv.org/abs/2609.38492},
  note         = {GAP-to-Lean4 Formal Port, Gokujo CI Gate Verified.}
}
```

---

## 🏛️ Associated Formal Verification & Scientific Corpus

Werracle represents Paper 7 in the unified open-science corpus spanning fractal neural synthesis, formal verification, biophysical modeling, and decentralized reflex intelligence:

| Pillar / Paper | Contribution & Focus | Latest Version DOI | Concept / Family DOI | arXiv / Verification & Status | Primary Repository |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Paper 1: MFNS** | Mandelbrot Fractal Neural Synthesis | [`10.5281/zenodo.22867037`](https://doi.org/10.5281/zenodo.22867037) | [`10.5281/zenodo.22774934`](https://doi.org/10.5281/zenodo.22774934) | Open Science Archive (In Revision) | [`pCwOrM/mandelbrot-fractal-neural-synthesis`](https://github.com/pCwOrM/mandelbrot-fractal-neural-synthesis) |
| **Paper 2: OED** | Orbital Error Dynamics (OED v3) | [`10.5281/zenodo.22900465`](https://doi.org/10.5281/zenodo.22900465) | [`10.5281/zenodo.22896855`](https://doi.org/10.5281/zenodo.22896855) | [`arXiv:2609.30115`](https://arxiv.org/abs/2609.30115) • [HF Paper](https://huggingface.co/papers/2609.30115) (Claimed) | [`pCwOrM/mandelbrot-fractal-neural-synthesis`](https://github.com/pCwOrM/mandelbrot-fractal-neural-synthesis) |
| **Paper 3: WerreduR** | Procedural Fractal Pedagogy (v4.0) | [`10.5281/zenodo.23128224`](https://doi.org/10.5281/zenodo.23128224) | [`10.5281/zenodo.22999420`](https://doi.org/10.5281/zenodo.22999420) | Target: Q1 AIED / CAEAI • [Live Simulator](https://pcworm.github.io/WerreduR/) | [`jesmaat/WerreduR`](https://github.com/jesmaat/WerreduR) (Mirror: [`pCwOrM/WerreduR`](https://github.com/pCwOrM/WerreduR)) |
| **Paper 4: BH Page** | Black Hole Page Curve & Quantum Gravity (v5) | [`10.5281/zenodo.23072120`](https://doi.org/10.5281/zenodo.23072120) | [`10.5281/zenodo.22961999`](https://doi.org/10.5281/zenodo.22961999) | CERN Record 22978460 • Quantum Stabilizers | [`pCwOrM/mandelbrot-fractal-neural-synthesis`](https://github.com/pCwOrM/mandelbrot-fractal-neural-synthesis) |
| **Paper 5: Formal** | Lean 4 40-Core Gauntlet (v2) | [`10.5281/zenodo.22983889`](https://doi.org/10.5281/zenodo.22983889) | [`10.5281/zenodo.22974543`](https://doi.org/10.5281/zenodo.22974543) | [`arXiv:2609.33066`](https://arxiv.org/abs/2609.33066) • [HF Paper](https://huggingface.co/papers/2609.33066) (Claimed) | [`pCwOrM/werr`](https://github.com/pCwOrM/werr) & [`werracle`](https://github.com/pCwOrM/werracle) |
| **Paper 6: WerrSoma** | Drosophila Connectome (158K Neurons, v1.1) | [`10.5281/zenodo.23072929`](https://doi.org/10.5281/zenodo.23072929) | [`10.5281/zenodo.22996625`](https://doi.org/10.5281/zenodo.22996625) | `arXiv:submit/8161759` [on hold] • [Live 3D Portal](https://werrsoma.answerr.me/) | [`Lexovian/WerrSoma`](https://github.com/Lexovian/WerrSoma) (Mirror: [`pCwOrM/WerrSoma`](https://github.com/pCwOrM/WerrSoma)) |
| **Paper 7: Werracle** | Sub-Cent Intra-Block EVM AI Oracle (This Work) | [`10.5281/zenodo.22942599`](https://doi.org/10.5281/zenodo.22942599) | [`10.5281/zenodo.22942598`](https://doi.org/10.5281/zenodo.22942598) | [`arXiv:2609.30719`](https://arxiv.org/abs/2609.30719) • [HF Paper](https://huggingface.co/papers/2609.30719) (Claimed) | [`pCwOrM/werracle`](https://github.com/pCwOrM/werracle) & [`werralem`](https://github.com/pCwOrM/werralem) |
| **Paper 8: Schönhage**| Tensor Carrier Compression ($W=176M$) | [`10.5281/zenodo.23268580`](https://doi.org/10.5281/zenodo.23268580) | [`10.5281/zenodo.23268579`](https://doi.org/10.5281/zenodo.23268579) | [`arXiv:2610.14263`](https://arxiv.org/abs/2610.14263) ([PDF](https://arxiv.org/pdf/2610.14263) • [DOI: `10.48550/arXiv.2610.14263`](https://doi.org/10.48550/arXiv.2610.14263) • `submit/8207241` [published]) • [CrocSwap #226 (Incorporated)](https://github.com/CrocSwap/integer-mult-bounds/pull/226) • [Contributors](https://github.com/CrocSwap/integer-mult-bounds/blob/50d768818f579d4e165b4c257c6ee25bca300802/CONTRIBUTORS.md) • [Audit `50d76881`](https://github.com/CrocSwap/integer-mult-bounds/blob/50d768818f579d4e165b4c257c6ee25bca300802/docs/research/community-reconciliation-next100-review.md) | [`pCwOrM/integer-mult-bounds`](https://github.com/pCwOrM/integer-mult-bounds) |
| **Paper 9: Güneş Dili**| Deterministik Morfoloji & 53 Koma | [`10.5281/zenodo.23273006`](https://doi.org/10.5281/zenodo.23273006) | [`10.5281/zenodo.23273005`](https://doi.org/10.5281/zenodo.23273005) | Lean 4 Machine Verified • [Live Portal](https://pcworm.github.io/gunes-dili/) | [`pCwOrM/gunes-dili`](https://github.com/pCwOrM/gunes-dili) |
| **Paper 10: GDT** | General Divisor Theorem & Residue Conditioning | [`10.5281/zenodo.23316070`](https://doi.org/10.5281/zenodo.23316070) | [`10.5281/zenodo.23316070`](https://doi.org/10.5281/zenodo.23316070) | Lean 4 Machine Verified (2,287 Checks PASS) | [`pCwOrM/general-divisor-theorem`](https://github.com/pCwOrM/general-divisor-theorem) |
| **Paper 11: Niemeier**| 24D Niemeier $A_8^3$ & K3 Umbral Moonshine | [`10.5281/zenodo.23324066`](https://doi.org/10.5281/zenodo.23324066) | [`10.5281/zenodo.23324066`](https://doi.org/10.5281/zenodo.23324066) | Lean 4 Certified (0 sorry, 0 axioms) • Record 23324067 | [`pCwOrM/niemeier-a8-umbral-moonshine`](https://github.com/pCwOrM/niemeier-a8-umbral-moonshine) |
| **Engine: WERR** | Zero-VRAM Gauntlet & JevBench Intake | [`10.5281/zenodo.22939253`](https://doi.org/10.5281/zenodo.22939253) | [`10.5281/zenodo.22867425`](https://doi.org/10.5281/zenodo.22867425) | [`arXiv:2609.25498`](https://arxiv.org/abs/2609.25498) • [HF Paper](https://huggingface.co/papers/2609.25498) • [HF Dataset](https://huggingface.co/datasets/pCwOrM/werr_open_decisions) | [`pCwOrM/werr`](https://github.com/pCwOrM/werr) |
| **Platform: answerr**| Reflex AI & Live Workspace | Production: [`answerr.me`](https://answerr.me) | - | Dual-Cognition Reflex Platform | [`pCwOrM/answerr`](https://github.com/pCwOrM/answerr) |
| **Discrete Alg** | GAP-Lean4 Formally Verified Port (35 Theorems) | [`10.5281/zenodo.23045504`](https://doi.org/10.5281/zenodo.23045504) | [`10.5281/zenodo.23045503`](https://doi.org/10.5281/zenodo.23045503) | [`arXiv:2609.38492`](https://arxiv.org/abs/2609.38492) • [HF Paper](https://huggingface.co/papers/2609.38492) (Claimed) | [`pCwOrM/gap-lean4-port`](https://github.com/pCwOrM/gap-lean4-port) |
| **Edge Robotics: WERRobotics** | Zero-Memory Arduino & Embedded Reflex Kernel (`v0.5.1`) | [`10.5281/zenodo.22939253`](https://doi.org/10.5281/zenodo.22939253) | [`10.5281/zenodo.22867425`](https://doi.org/10.5281/zenodo.22867425) | ATmega328P / ESP32 / STM32 (`0 Bytes Heap`, `TR 2026/016633`) | [`pCwOrM/WERRobotics`](https://github.com/pCwOrM/WERRobotics) |

---

## 📜 License
Werracle is released under the **Business Source License 1.1 (BSL 1.1)**.  
* Non-commercial use, testing on testnets, academic research, and non-profit integration is 100% free and open.
* Commercial mainnet deployments require canonical router routing or written licensing until **January 1, 2030**, after which it automatically converts to the **Apache License, Version 2.0**.
* Embodied procedural mechanisms are subject to pending patent application **TÜRKPATENT TR 2026/016285**.

## 🏛️ Historical Archives & Version Heritage

All previous design iterations and protocol evolutions are permanently preserved in source for transparency:

- **Classic v1.0 Archive (`werracle.io` Initial Baseline):** [`https://werracle.io/v1_classic.html`](https://werracle.io/v1_classic.html)
- **Architecture v2.0 Sandbox Archive:** [`https://werracle.io/v2_initial_archive.html`](https://werracle.io/v2_initial_archive.html)
- **Corporate Portal v1.0 (Dark Theme Archive):** [`https://werracle.com/archive_dark_v1.html`](https://werracle.com/archive_dark_v1.html)


---

# PART II — Türkçe Kronolojik Araştırma ve Geliştirme Külliyatı

<p align="center">
  <img src="assets/werracle_logo_oracle.svg" alt="Werracle Logo Amblemi" width="160" height="160" />
</p>

# ⚡ Werracle: Sıfır-Bellekli On-Chain Yapay Zekâ ve Karar Oracle'ı

[![EVM Devnet: Chain ID 4242](https://img.shields.io/badge/EVM%20Devnet-Chain%20ID%204242%20(api.answerr.me)-38bdf8.svg)](https://api.answerr.me/werracle/status)
[![API Dokümantasyonu](https://img.shields.io/badge/API%20Belgeleri-Canl%C4%B1%20Etkile%C5%9Fimli-10b981.svg)](https://werracle.io/apidocs.html)
[![Gecikme: < 12ms](https://img.shields.io/badge/Gecikme-%3C12ms%20RPC-brightgreen.svg)]()
[![Lisans: BSL 1.1](https://img.shields.io/badge/Lisans-BSL%201.1-blue.svg)](./LICENSE)
[![Web3 Protokol: werracle.io](https://img.shields.io/badge/Web3%20Protokol-werracle.io-f59e0b.svg?logo=cloudflare&logoColor=white)](https://werracle.io/)
[![Kurumsal Portal: werracle.com](https://img.shields.io/badge/Kurumsal%20Portal-werracle.com-2b3bd1.svg?logo=cloudflare&logoColor=white)](https://werracle.com/)
[![Akademik Portal: werr.io](https://img.shields.io/badge/Akademik%20Portal-werr.io-0284c7.svg?logo=cloudflare&logoColor=white)](https://werr.io/)
[![Aurora Sözleşmesi: 0x1d7Ae9E1](https://img.shields.io/badge/Aurora%20S%C3%B6zle%C5%9Fmesi-0x1d7Ae9E1...caBaF-78D64B.svg)](https://explorer.testnet.aurora.dev/address/0x1d7Ae9E1dDDA805539d9e225425804Ef8B9caBaF)
[![Bulut Kasası: R2 Aktif](https://img.shields.io/badge/Bulut%20Kasas%C4%B1-Cloudflare%20R2%20Aktif-f38020.svg?logo=cloudflare&logoColor=white)](https://werracle.com/)
[![NSF ICARM Rekoru](https://img.shields.io/badge/NSF%20ICARM-230%20Do%C4%9Frulanm%C4%B1%C5%9F%20E%C4%9Fri-blue)](https://elliptic-rank.icarm.cloud/user/114)
[![1.000 Mühürlü Test: %100 Başarı](https://img.shields.io/badge/1.000%20Test-%25100%20M%C3%BCh%C3%BCrl%C3%BC%20ve%20Do%C4%9Frulanm%C4%B1%C5%9F-brightgreen.svg)](docs/TEST_1000_AUDIT_REPORT.md)
[![Denetim: SHA--256 Mühürlü](https://img.shields.io/badge/Denetim-SHA--256%20M%C3%BCh%C3%BCrl%C3%BC-blueviolet.svg)](tests/sealed/SEAL_MANIFEST.json)
[![GitHub Education: Community Exchange](https://img.shields.io/badge/GitHub%20Education-Community%20Exchange-2ea44f?logo=github&logoColor=white)](https://education.github.com/globalcampus/exchange)
[![Rehber: LEARN.md](https://img.shields.io/badge/Rehber-LEARN.md-orange.svg)](LEARN.md)
[![CI / Doğrulama](https://github.com/pCwOrM/werracle/actions/workflows/ci.yml/badge.svg)](https://github.com/pCwOrM/werracle/actions/workflows/ci.yml)
[![Telemetri: Kalıcı Olarak Kapalı](https://img.shields.io/badge/Telemetri-Kal%C4%B1c%C4%B1%20Olarak%20Olarak%20Devred%C4%B1%C5%9F%C4%B1-10b981.svg)]()
[![Solidity: ^0.8.20](https://img.shields.io/badge/Solidity-%5E0.8.20-363636.svg?logo=solidity)](https://soliditylang.org/)
[![Cairo: 2.8+ (Sierra)](https://img.shields.io/badge/Starknet-Cairo%202.8%2B%20(Sierra)-ec796b.svg)](cairo/)
[![Starknet Adım: ~1.420](https://img.shields.io/badge/CairoVM-~1.420%20Ad%C4%B1m%20(STARK--Native)-ec796b.svg)](docs/STARKNET_ARCHITECTURE_AND_SEED_GRANT_ROADMAP.md)
[![Starknet DeFi: Ekubo Eklentisi](https://img.shields.io/badge/Starknet%20DeFi-Ekubo%20LVR%20Extension-blueviolet.svg)](cairo/src/ekubo_werracle_extension.cairo)
[![EVM Gas: ~20k](https://img.shields.io/badge/EVM%20Gas-~20k%20(Kuru%C5%9F%20Mertebesinde)-brightgreen.svg)](https://werracle.io/#simulator)
[![Model Boyutu: 0 Bayt](https://img.shields.io/badge/Model%20Boyutu-0%20Bayt%20VRAM-10b981.svg)]()
[![Depolama: Tek bytes32 / felt252](https://img.shields.io/badge/Storage%20Slotu-Tek%20bytes32%20%7C%20felt252-purple.svg)](https://werracle.io/#storage-slot)
[![Patent Başvurusu](https://img.shields.io/badge/Patent%20Ba%C5%9Fvurusu-TR%202026%2F016285-red.svg)](https://epats.turkpatent.gov.tr)
[![Ekosistem: WERR](https://img.shields.io/badge/Motor-WERR%20%C3%87ekirdek-emerald.svg)](https://github.com/pCwOrM/werr)
[![Ekosistem: answerr](https://img.shields.io/badge/Platform-answerr-8b5cf6.svg)](https://github.com/pCwOrM/answerr)
[![Ekosistem: Araştırma](https://img.shields.io/badge/Ara%C5%9Ft%C4%B1rma-Mandelbrot%20Sentezi-blue.svg)](https://github.com/pCwOrM/mandelbrot-fractal-neural-synthesis)
[![Ekosistem: WerrSoma Konnektom](https://img.shields.io/badge/Konnektom-WerrSoma%20158K%20N%C3%B6ron-00f0ff.svg)](https://github.com/Lexovian/WerrSoma)
[![Konnektom DOI](https://img.shields.io/badge/WerrSoma%20DOI-10.5281%2Fzenodo.22996625-024dad.svg)](https://doi.org/10.5281/zenodo.22996625)
[![WerrSoma Portalı](https://img.shields.io/badge/WerrSoma%20Portal-werrsoma.answerr.me-00f0ff.svg)](https://werrsoma.answerr.me/)
[![Ekosistem: WERRobotics](https://img.shields.io/badge/WERRobotics-Arduino%20%26%20Edge%20AI-ff9100.svg?logo=arduino&logoColor=white)](https://github.com/pCwOrM/WERRobotics)
[![NEAR Protocol](https://img.shields.io/badge/NEAR%20Protocol-Intents%20%26%20Aurora%20EVM-00EC97.svg?logo=near&logoColor=black)](near/README.md)
[![Aurora EVM](https://img.shields.io/badge/Aurora%20EVM-Chain%20ID%201313161555-78D64B.svg)](near/README.md)
[![arXiv: 2609.30719 (Werracle)](https://img.shields.io/badge/arXiv-2609.30719%20%5Bcs.CR%5D-b31b1b.svg)](https://arxiv.org/abs/2609.30719)
[![SSRN: 7626279](https://img.shields.io/badge/SSRN-7626279-002f6c.svg?logo=elsevier)](https://ssrn.com/abstract=7626279)
[![arXiv DOI: 10.48550/arXiv.2609.30719](https://img.shields.io/badge/arXiv%20DOI-10.48550%2FarXiv.2609.30719-b31b1b.svg)](https://doi.org/10.48550/arXiv.2609.30719)
[![arXiv: 2609.25498 (WERR)](https://img.shields.io/badge/arXiv-2609.25498%20%5Bcs.AI%5D-b31b1b.svg)](https://arxiv.org/abs/2609.25498)
[![Lean 4 Formel İspat: Zenodo 22974544](https://img.shields.io/badge/Paper%205%20DOI-10.5281%2Fzenodo.22974544-024dad.svg)](https://doi.org/10.5281/zenodo.22974544)
[![Lean 4 Formel Makale: arXiv 2609.33066](https://img.shields.io/badge/Formel%20Makale-arXiv%3A2609.33066%20(Lean4)-b31b1b.svg)](https://arxiv.org/abs/2609.33066)
[![Formel Doğrulama: Lean 4 (0 Sorry)](https://img.shields.io/badge/Formel%20Doğrulama-Lean%204%20(0%20Sorry)-9333ea.svg)](formal_proofs/WerracleProof.lean)
[![Zenodo DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.22942598-024dad.svg)](https://doi.org/10.5281/zenodo.22942598)
[![Makale: Kamera-Hazır PDF](https://img.shields.io/badge/Makale%20v2.0-Kamera--Haz%C4%B1r-emerald.svg)](https://arxiv.org/pdf/2609.30719)

> 🌐 **Dil Seçici / Language Switcher:**  
> **Türkçe (Varsayılan)** | [🇬🇧 English Documentation (README.md)](README.md) &bull; 🐺 [**Starknet (Cairo 2 / Sierra) Mimarisi ve Yol Haritası**](docs/STARKNET_ARCHITECTURE_AND_SEED_GRANT_ROADMAP.md) &bull; 🟢 [**NEAR Intents ve Aurora Mimarisi**](near/README.md) &bull; 📄 [**Resmi arXiv Makalesi (2609.30719)**](https://arxiv.org/abs/2609.30719) &bull; 🌐 [**Etkileşimli Web Simülatörü**](https://werracle.io/) &bull; ⚡ [**Etkileşimli API Dokümanı**](https://werracle.io/apidocs.html) &bull; 🎓 [**LEARN.md Eğitim Kılavuzu**](LEARN.md) &bull; 🛡️ [**1.000 Test Mühürlü Denetim Raporu**](docs/TEST_1000_AUDIT_REPORT.md) &bull; 📢 [**Hibe ve Duyuru Rehberi**](docs/WEB3_GRANT_AND_ANNOUNCEMENT_PLAYBOOK.md)

> **Hem Ethereum Sanal Makinesi (`EVM / Solidity`) hem de Starknet (`Cairo 2.x / Sierra`) içinde blok-içi (intra-block) düzeyde ve milisaniye-altı hızda çalışabilen ilk üretime hazır On-Chain AI Karar Oracle'ı.**  
> *WERR prosedürel Mandelbrot kaçış dinamiği ile güçlendirilmiştir. Sıfır tensör matrisi. ZK-ML'den 1000 kat daha hızlı ve 15 kat daha ucuz — Starknet üzerinde %100 doğal STARK kanıt geçerliliği ile.*  
> 📄 **Resmi Yayın:** *"Werracle: Sub-Cent Intra-Block AI Reflex Oracles and Flash-Loan Circuit Breakers for EVM Smart Contracts"* — [**arXiv:2609.30719 [cs.CR, cs.AI, cs.DC]**](https://arxiv.org/abs/2609.30719) │ [**SSRN: 7626279 (Elsevier)**](https://ssrn.com/abstract=7626279) | DOI: [`10.48550/arXiv.2609.30719`](https://doi.org/10.48550/arXiv.2609.30719) | Zenodo: [`10.5281/zenodo.22942598`](https://doi.org/10.5281/zenodo.22942598)  
> 📡 **Werracle Radar (Canlı DaaS & Tasfiye Gözlemevi):** [radar.werracle.com](https://radar.werracle.com) │ [Hugging Face Veri Seti (v1.2)](https://huggingface.co/datasets/pCwOrM/werracle-oev-liquidation-dataset-2026) │ [Zenodo Veri Seti DOI: 10.5281/zenodo.23623588](https://doi.org/10.5281/zenodo.23623588) │ [SSRN: 7668638](https://papers.ssrn.com/abstract=7668638)  
> 💼 **Yatırımcı Sunumları (PDF):** [Radar DaaS (EN)](docs/Werracle_Radar_Investor_Pitch_Deck.pdf) │ [Radar DaaS (TR)](docs/Werracle_Radar_Yatirimci_Sunumu_TR.pdf) │ [Tüm Ekosistem (EN)](docs/Werracle_Product_Investor_Pitch_Deck_EN.pdf) │ [Tüm Ekosistem (TR)](docs/Werracle_Product_Investor_Pitch_Deck_TR.pdf)

<p align="center">
  <img src="assets/twitter_lean4_tesla_gauntlet.png" alt="Werracle Lean 4 Formel Doğrulama & Tesla 3-6-9 Harmonikleri" width="100%">
</p>

---

## 🌟 Genel Bakış

Blokzincir mimarilerinde geleneksel derin öğrenme modellerini çalıştırmak **bellek duvarı darboğazı** nedeniyle imkânsız kabul edilmiştir: Milyonlarca kayan noktalı parametreyi Ethereum depolamasında ($SSTORE$) saklamak milyonlarca gas tüketir.

**ZK-ML (Zero-Knowledge Machine Learning)** bu sorunu çözmek için modeli zincir dışında çalıştırıp zincir üzerinde SNARK kanıtı doğrular. Ancak ZK-ML'de kanıt üretimi **10 ila 300 saniye** sürer ve işlem başına **250.000 – 500.000 gas** harcanır. Bu durum ZK-ML'i, tek bir işlem içinde atomik olarak gerçekleşen **flash-loan ve MEV arbitraj saldırılarına karşı tamamen etkisiz** kılar.

**Werracle bu çıkmazı kökünden çözer:**
* **24-Baytlık Koordinat Tohumu:** Karar yüzeyi doğrudan $\Theta = (c_x, c_y, \text{zoom})$ Mandelbrot koordinatından prosedürel olarak türetilir.
* **Tek Bir 32-Bayt Slot (`bytes32`):** Güncelleme sayacı ve eşik değerleriyle birlikte tek bir depolama slotuna tam oturur. Okuma maliyeti warm slot için sadece **100 gas**'tır.
* **Q16.16 Sabit Noktalı Aritmetik:** Kayan nokta (float) olmadan saf tam sayı bit kaydırmaları ile 16 noktalı ($4 \times 4$) Pareto mikro-ızgarasını tarar.
* **Aşırı Düşük Gas İcrası:** Tam bir yapay zekâ kararı (`noul`, `choice`, `score`) yalnızca **~18.000 – 24.000 gas (Base ve Arbitrum'da kuruşun kesirleri)** harcar.

---

## 📊 Kıyaslama Tablosu

| Boyut / Metrik | Geleneksel Web2 Oracle (Chainlink vb.) | ZK-ML (EZKL, Modulus Labs) | **WERRACLE (EVM Native)** |
| :--- | :--- | :--- | :--- |
| **Model Ağırlık Belleği** | Gigabaytlarca Sunucu Belleği | Zincir Dışı Prover Sunucusu | **0 Bayt (Prosedürel Geometri)** |
| **On-Chain Depolama** | N/A (İmzalı Harici Veri) | Doğrulama Anahtarları ve İspatlar | **Tek Bir 32-Bayt Slot (`bytes32`)** |
| **Karar Gecikmesi** | 12 – 36 saniye (Ağ Gecikmesi) | 10 – 300 saniye (İspat Üretimi) | **< 1 ms (Blok-İçi / Atomik)** |
| **Tipik Gas Maliyeti** | ~40.000 – 80.000 gas | ~250.000 – 500.000 gas | **~18.000 – 24.000 gas** |
| **Flash-Loan Savunması** | ❌ İmkânsız (Çok yavaş) | ❌ İmkânsız (Asenkron blok gecikmesi)| **✅ Mükemmel (İşlem anında `revert`)** |
| **Harici Bağımlılık** | Çoklu-İmzalı (Multi-Sig) Sunucular | Ağır GPU Donanımı | **SIFIR (Tamamen Özerk EVM Kontratı)** |
| **Lisans** | Kapalı SaaS | Açık Kaynak / Bulut | **BSL 1.1 (Uniswap Modeli)** |

---

## ⚡ Canlı EVM Testnet ve Akıllı Kontratlar (`api.answerr.me`)

Werracle, yüksek performanslı özel donanım düğümümüz (`api.answerr.me`, Ubuntu 24.04 LTS) üzerinde özelleştirilmiş özel EVM devnet kum havuzunda canlı olarak çalışmaktadır:

* **Ağ Adı:** Werracle Devnet (Anvil EVM Sandbox)
* **Chain ID:** `4242` &bull; **Blok Süresi:** `1.0s`
* **Genel HTTPS JSON-RPC:** `https://api.answerr.me/werracle/rpc`
* **Gerçek Zamanlı REST Ağ Geçidi:** `https://api.answerr.me/werracle/status`
* **Canlı Etkileşimli Dokümantasyon:** [https://werracle.io/apidocs.html](https://werracle.io/apidocs.html)

### Dağıtılmış Kontrat Kaydı (v2.0 ve v1.0 Tabanı):
| Kontrat Adı | Bayt Kodu Adresi | Gas Kıyaslaması | Açıklama |
| :--- | :--- | :--- | :--- |
| **`WerracleTripodZMod9.sol`** | [`0x0a95887dBa2783E1E445bB4D3A9a1f7cB3152d04`](https://api.answerr.me/werracle/status) | **22.557 gas** | **v2.0 Amiral Gemisi Çekirdeği**: Seyreltilmiş Çok Ölçekli Tripod ve $\mathbb{Z} \pmod 9$ Erken Kaçış |
| **`BlockchainResonanceMatrix.sol`** | Gömülü Baytkodu Kütüphanesi | **3.821 gas** | **v2.0 Anlamsal Matris**: 5 Sütunda 40 On-Chain Belirteç (0 SLOAD) |
| **`Werracle.sol`** | [`0x5FbDB2315678afecb367f032d93F642f64180aa3`](https://api.answerr.me/werracle/status) | **21.438 gas** | **v1.0 Kanonik Tabanı**: 16-noktalı Pareto mikro-ızgarası (arXiv / Zenodo referansı) |
| **`WerracleFeeHook.sol`** | [`0xdef5Ad647Af159D27cd111007e4CCD1fDE9d4006`](https://api.answerr.me/werracle/status) | **36.739 gas** | Uniswap v4 Dinamik Volatilite Ücret Kancası (Hook) |

### Canlı On-Chain Kararları Sorgulayın (15ms Altı):
```bash
# 1. Devnet Durumunu ve Blok Yüksekliğini İnceleyin
curl -s https://api.answerr.me/werracle/status

# 2. Canlı On-Chain Oracle Refleksini (noul) Sorgulayın
curl -s -X POST https://api.answerr.me/werracle/oracle/noul \
  -H "Content-Type: application/json" \
  -d '{"risk_score": 0.15}'

# 3. Uniswap v4 Dinamik Ücret Kancasını (Hook) Sorgulayın
curl -s -X POST https://api.answerr.me/werracle/hook/fee \
  -H "Content-Type: application/json" \
  -d '{"imbalance_ratio": 0.35}'
```

---

## 🚀 Werracle v2.0: Çok Ölçekli Seyreltilmiş Tripod ve $\mathbb{Z} \pmod 9$ Rezonansı

Werracle v2.0, canlı EVM üzerinde test edilmiş ve kanıtlanmış iki büyük algoritmik yenilik sunar:

### 1. Çok Ölçekli Harmonik Tripod (Seyreltilmiş 12-Noktalı Izgara)
Tek bir odak düzlemi yerine, v2.0 üç harmonik yakınlaştırma düzlemi üzerinden örnekleme yapar:
* **Geniş Ufuk ($0.60\times$):** Makro gürültüyü filtreler ve sınır dalgalanmalarını stabilize eder (Ağırlık: $0.25$).
* **Doğal Odak ($1.00\times$):** Kanonik karar düzlemi (Ağırlık: $0.50$).
* **Derin Kırılma ($1.60\times$):** Çatallanma sınırındaki ince fraktal iplikçikleri ayrıştırır (Ağırlık: $0.25$).  
Her düzlemde 4 ortogonal kardinal nokta ($3 \times 4 = 12$ nokta) taranarak, v1.0'ın 16 noktalı düz ızgarasından daha az işlemle 3 ölçekli harmonik derinlik elde edilir.

### 2. $\mathbb{Z} \pmod 9$ Modüler Rezonans Erken Kaçış Dinamiği
Lean 4 formel cebirsel halka yapısına (`ZMod 9`) dayalı modüler kilometre taşlarında ($n \in \{3, 6, 9\}$) kaçış kontrolü yapılır. Flaş saldırılar ve ani şoklar 3. adımda hızla kaçarak ortalama döngü derinliğini 12 adımdan ~3.9 adıma düşürür.

### 3. Ampirik EVM Gaz Kıyaslaması (v1.0 Taban vs v2.0 Tripod $\mathbb{Z} \pmod 9$)
EIP-150 / EIP-2929 / EIP-3860 kuralları altında `solc 0.8.20 (runs: 200)` derlemesiyle [`scripts/ideal_evm_gas_benchmark.js`](scripts/ideal_evm_gas_benchmark.js) aracıyla canlı ölçülmüştür:

| Katman / Senaryo | v1.0 Taban | v2.0 Tripod $\mathbb{Z} \pmod 9$ | Net Tasarruf | Düşüş Oranı | Tavan Kriteri |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Saf Çıkarım Motoru Gazı** | **226.363 gaz** | **22.557 gaz** | **-203.806 gaz** | **-%90,0** | **BAŞARILI** ($\le 24.000$) |
| **En Kötü Durum Motor Tavanı** | 226.416 gaz | **22.568 gaz** | -203.848 gaz | -%90,0 | **BAŞARILI** (+1.432 gaz payı) |
| **Warm `decideNoul` (Normal)** | 264.970 gaz | **61.186 gaz** | -203.784 gaz | -%76,9 | Operasyonel |
| **Warm `decideNoul` (Şok / Hızlı Kaçış)** | 247.972 gaz | **44.102 gaz** | -203.870 gaz | -%82,2 | Operasyonel |
| **2 Seçenekli Rota Seçimi** | 247.786 gaz | **43.726 gaz** | -204.060 gaz | -%82,4 | Operasyonel |
| **8 Seçenekli Rota Seçimi** | 251.752 gaz | **44.680 gaz** | -207.072 gaz | -%82,3 | Operasyonel |
| **1-Belirteç Rezonans Sorgusu** | N/A | **3.821 gaz** | Salt Bytecode | 0 SLOAD | Anlık |
| **4-Belirteç Kompozit Füzyon** | N/A | **7.443 gaz** | Salt Bytecode | 0 SLOAD | Anlık |
| **Uniswap v4 Dinamik Kanca** | N/A | **36.739 gaz** | Uçtan Uca | Volatiliteye Bağlı | Sub-blok |

> 🛡️ **Formel İnvaryant Doğrulaması**: Ayrıntılı ampirik denetim raporu [`docs/EVM_GAS_IDEAL_BENCHMARK_REPORT.md`](docs/EVM_GAS_IDEAL_BENCHMARK_REPORT.md) ve ham JSON verileri [`tests/results/evm_gas_ideal_benchmark.json`](tests/results/evm_gas_ideal_benchmark.json) dosyasında mevcuttur.

---

## 🧩 EVM 32-Bayt Storage Slot Düzeni

```text
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          c_x (8 Bayt - int64 Q16.16: -48735)                  |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          c_y (8 Bayt - int64 Q16.16: +8639)                   |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          zoom (8 Bayt - uint64 Q16.16: 3276800)               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Nonce (4B)       | Eşik (2B)      | Mod (1B) | Aktif (1B)     |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|<----------------- Toplam: 32 Bayt (Tek Slot) ----------------->|
```

---

## ⚡ Üç Temel Karar Primitifi

### 1. `noul` (Boolean Refleks Kapısı)
İşlem güvenliği, flash-loan devre kesicisi veya geçiş izni için atomik True/False ve güven skoru üretir:
```solidity
(bool allowed, uint16 confidenceBps) = werracle.decideNoul{value: fee}(
    keccak256("tx:liquidation"),
    riskSignalFP // Q16.16 format (-1.5: Güvenli, +2.5: Yüksek Tehdit)
);

if (!allowed) {
    revert("Werracle: Supheli Islem Engellendi");
}
```

### 2. `choice` (4-Kadran Rota Seçici)
İşlemleri en uygun likidite havuzuna, arbitraj rotasına veya oyun durumuna dinamik yönlendirir:
```solidity
uint8 chosenRoute = werracle.decideChoice{value: fee}(
    poolId,
    4, // Seçenek adedi
    contextBiasFP
);
```

### 3. `score` (Sürekli Şiddet / Derecelendirme)
Uniswap v4 dinamik komisyonları ve borçlanma teminat faktörleri için anlık risk seviyesi (0 ile 3 arası) üretir:
```solidity
uint256 severity = werracle.decideScore{value: fee}(
    poolId,
    volatilitySignalFP,
    3 // Maksimum skala
);
```

---

## 💰 Gelir Modelleri ve Protokol Ücreti

`Werracle.sol` sürdürülebilir bir nakit akışı sağlamak üzere tasarlanmıştır:
* **İşlem Başına Mikro Protokol Ücreti:** Her karar çağrısında cüzi bir fee (varsayılan: `0.00005 ether` ~ $0.15) tahsil edilir ve doğrudan kontrat sahibinin cüzdanına akar.
* **Uniswap v4 Dinamik Komisyon Kancası:** [`contracts/hooks/WerracleFeeHook.sol`](contracts/hooks/WerracleFeeHook.sol), piyasa oynaklığına göre komisyonu %0.05 ile %0.50 arasında dinamik yöneterek LP gelirlerinden pay alır.
* **Kurumsal Tohum Eğitimi (B2B):** Web3 protokollerine kendi özel risk modellerine uygun 24-baytlık özel koordinat tohumu sağlama hizmeti.

---

## 📦 Kurulum ve Testler

### 1. Python Q16.16 Çapraz Doğrulama Testi
```bash
python sim/test_cross_validation.py
```
*Orijinal WerrEngine referansı ile %100 birebir karar korelasyonu üretir.*

### 2. Solidity Kontratlarını Derleme
```bash
npm install
node -e "const solc=require('solc'); /* tüm kontratları derler */"
```

---

---

## 💳 Bağış ve Hibe Kabul Cüzdanı
* **Resmi Cüzdan (Binance - USDT TRC20 / TRON Ağı):** `TLMhaDJTVYBHBSGJ9nCQGLvqnYFPsBgLJu`
* **Resmi İletişim:** `vdagli@itouch.com.tr` (Kurumsal) | `pcworm@pcworm.net` (Baş Araştırmacı) | `ask@answerr.me` (AI Otonom Ajan) | Web: `https://answerr.me`

---

## 📖 Akademik Alıntı (Citation)

Werracle'ı veya temelindeki WERR fraktal Sistem-1 karar motorunu Web3 araştırmalarınızda, dApp'lerinizde veya akademik yayınlarınızda kullanıyorsanız lütfen şu şekilde atıfta bulununuz:

```bibtex
@article{dagli2026werracle_arxiv,
  author        = {Volkan Da{\u{g}}l{\i} and Zerrin Da{\u{g}}l{\i} and Da{\u{g}}han Da{\u{g}}l{\i}},
  title         = {Werracle: Sub-Cent Intra-Block AI Reflex Oracles and Flash-Loan Circuit Breakers for EVM Smart Contracts},
  journal       = {arXiv preprint arXiv:2609.30719 [cs.CR, cs.AI, cs.DC]},
  year          = {2026},
  eprint        = {2609.30719},
  archivePrefix = {arXiv},
  primaryClass  = {cs.CR},
  url           = {https://arxiv.org/abs/2609.30719},
  doi           = {10.48550/arXiv.2609.30719},
  note          = {Zenodo Archive: 10.5281/zenodo.22942598. TÜRKPATENT Priority: TR 2026/016285}
}


@article{dagli2026werracle_ssrn,
  title         = {Werracle: Sub-Cent Intra-Block AI Reflex Oracles and Flash-Loan Circuit Breakers for EVM Smart Contracts},
  author        = {Da{\u{g}}l{\i}, Volkan and Da{\u{g}}l{\i}, Zerrin and Da{\u{g}}l{\i}, Da{\u{g}}han},
  journal       = {Elsevier SSRN Electronic Journal},
  year          = {2026},
  month         = {October},
  note          = {SSRN Abstract ID: 7626279},
  url           = {https://ssrn.com/abstract=7626279}
}
@article{dagli2026fractalmap,
  author        = {Volkan Dağlı and Zerrin Dağlı and Dağhan Dağlı},
  title         = {Universal Fractal Natural Language Decision Map: Real-Time Edge Triage Across Heterogeneous Domains},
  journal       = {arXiv preprint arXiv:2609.25498 [cs.NE]},
  year          = {2026},
  url           = {https://arxiv.org/abs/2609.25498},
  doi           = {10.5281/zenodo.22939253}
}

@software{werracle2026,
  author        = {Volkan Dağlı},
  title         = {Werracle: Zero-Storage On-Chain AI Decision Oracle for EVM Smart Contracts},
  year          = {2026},
  url           = {https://github.com/pCwOrM/werracle},
  doi           = {10.5281/zenodo.22939253}
}

@article{dagli2026lean4_oed,
  title        = {Zero-Storage Procedural Neural Synthesis via Boundary Dynamics: Formal Verification in Lean 4 and Bare-Metal Gauntlet Validation},
  author       = {Da{\u{g}}l{\i}, Volkan and Da{\u{g}}l{\i}, Zerrin and Da{\u{g}}l{\i}, Da{\u{g}}han},
  journal      = {Zenodo Open Science Archive},
  year         = {2026},
  month        = {September},
  doi          = {10.5281/zenodo.22974544},
  url          = {https://doi.org/10.5281/zenodo.22974544},
  note         = {Formally verified in Lean 4 (Mathlib4, 0 sorry). 40-core bare-metal gauntlet benchmark verified. TÜRKPATENT Priority: TR 2026/016285.}
}

@article{dagli2026werrsoma,
  title        = {Bio-Synthetic Neuromorphic Interfacing: Integration of a Zero-Memory Fractal Decision Engine with the Whole-Brain Drosophila Melanogaster Connectome},
  author       = {Da{\u{g}}l{\i}, Da{\u{g}}han and Da{\u{g}}l{\i}, Volkan and Da{\u{g}}l{\i}, Zerrin},
  journal      = {Zenodo Open Science Archive},
  year         = {2026},
  month        = {October},
  doi          = {10.5281/zenodo.23072929},
  url          = {https://doi.org/10.5281/zenodo.23072929},
  note         = {158.262 nöron, 3.99M sinaps. Sub-4ms refleks gecikmesi, 0 VRAM. TÜRKPATENT Başvuru: TR 2026/016633. Çatı DOI: 10.5281/zenodo.22996625. Canlı 3D Portal: https://werrsoma.answerr.me/}
}
```

---

### 🏛️ Kurumsal ve Akademik Künye

* **Ticari İşletim ve Lisanslama:** **ITouch Systems** (*ITouch Bilişim Sistemleri Mühendislik Danışmanlık Sanayi ve Ticaret Ltd. Şti.*, Çukurova Teknokent, Adana) tarafından geliştirilmekte ve işletilmektedir. *Werr®*, *Werracle®* ve *Answerr®* markaları ITouch Systems bünyesindedir.
* **Bilimsel Araştırma ve Patentler:** **Volkan Dağlı** (*Anadolu Üniversitesi*), **Dr. Zerrin Dağlı** (*Mersin Üniversitesi*) ve **Dağhan Dağlı** (*Toros Üniversitesi — Toros Fen Lisesi*). Patent başvuruları: **TÜRKPATENT TR 2026/016285** ve **TR 2026/016633**.
* **API Aboneliği ve İletişim:** [Anında API Aboneliği (`radar.werracle.com`)](https://radar.werracle.com/v1/radar/dashboard#subscribe-section) • İletişim: `contact@werracle.com` | `ask@answerr.me`

---

## 📜 Lisans
Werracle, **Business Source License 1.1 (BSL 1.1)** ile korunmaktadır (Uniswap v3/v4 modeli):
* Testnet'lerde test etmek, akademik araştırmalar ve kar amacı gütmeyen protokoller için **%100 ücretsiz ve açık kaynaklıdır**.
* Ticari ana ağ (mainnet) dağıtımları **1 Ocak 2030** tarihine kadar resmi yönlendirici kullanımına veya ticari lisansa tabidir; bu tarihten sonra otomatik olarak **Apache License, Version 2.0**'a dönüşür.
* Somutlaştırılan prosedürel mekanizmalar **TÜRKPATENT TR 2026/016285** patent başvurusu koruması altındadır.

## 🏛️ Tarihsel Arşivler ve Sürüm Mirası

Tüm önceki tasarım ve protokol sürümleri şeffaflık ve denetlenebilirlik amacıyla kaynakta arşiv olarak korunmaktadır:

- **Klasik v1.0 Arşivi (`werracle.io` İlk Temel Sürüm):** [`https://werracle.io/v1_classic.html`](https://werracle.io/v1_classic.html)
- **Mimari v2.0 Deneme Alanı Arşivi:** [`https://werracle.io/v2_initial_archive.html`](https://werracle.io/v2_initial_archive.html)
- **Kurumsal Portal v1.0 (Koyu Tema Arşivi):** [`https://werracle.com/archive_dark_v1.html`](https://werracle.com/archive_dark_v1.html)

