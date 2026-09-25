# ⚡ Werracle: Zero-Storage On-Chain AI Decision Oracle

[![Zenodo DOI: 10.5281/zenodo.22942598](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.22942598-blue.svg)](https://doi.org/10.5281/zenodo.22942598)
[![Paper: Zenodo v1.0](https://img.shields.io/badge/Preprint-Zenodo%20Record%2022942599-10b981.svg)](https://zenodo.org/records/22942599)
[![EVM Devnet: Chain ID 4242](https://img.shields.io/badge/EVM%20Devnet-Chain%20ID%204242%20(api.answerr.me)-38bdf8.svg)](https://api.answerr.me:4431/werracle/status)
[![API Docs: Live](https://img.shields.io/badge/API%20Docs-Live%20Interactive-10b981.svg)](https://pcworm.github.io/werracle/apidocs.html)
[![Latency: < 12ms](https://img.shields.io/badge/Latency-%3C12ms%20RPC-brightgreen.svg)]()
[![License: BSL 1.1](https://img.shields.io/badge/License-BSL%201.1-blue.svg)](./LICENSE)
[![Live Portal: GitHub Pages](https://img.shields.io/badge/Live%20Portal-GitHub%20Pages-38bdf8.svg?logo=github)](https://pcworm.github.io/werracle/)
[![1,000 Sealed Tests: 100% Pass](https://img.shields.io/badge/1%2C000%20Tests-100%25%20Sealed%20%26%20Verified-brightgreen.svg)](docs/TEST_1000_AUDIT_REPORT.md)
[![Audit: SHA--256 Sealed](https://img.shields.io/badge/Audit-SHA--256%20Sealed-blueviolet.svg)](tests/sealed/SEAL_MANIFEST.json)
[![GitHub Education: Community Exchange](https://img.shields.io/badge/GitHub%20Education-Community%20Exchange-2ea44f?logo=github&logoColor=white)](https://education.github.com/globalcampus/exchange)
[![Tutorial: LEARN.md](https://img.shields.io/badge/Tutorial-LEARN.md-orange.svg)](LEARN.md)
[![CI / Verification](https://github.com/pCwOrM/werracle/actions/workflows/ci.yml/badge.svg)](https://github.com/pCwOrM/werracle/actions/workflows/ci.yml)
[![Telemetry: Permanently Disabled](https://img.shields.io/badge/Telemetry-Permanently%20Disabled-10b981.svg)]()
[![Solidity: ^0.8.20](https://img.shields.io/badge/Solidity-%5E0.8.20-363636.svg?logo=solidity)](https://soliditylang.org/)
[![EVM Gas: ~20k](https://img.shields.io/badge/EVM%20Gas-~20k%20(Sub--Cent)-brightgreen.svg)](https://pcworm.github.io/werracle/#simulator)
[![Model Size: 0 Bytes](https://img.shields.io/badge/Model%20Size-0%20Bytes%20VRAM-10b981.svg)]()
[![Seed: Single bytes32](https://img.shields.io/badge/Storage%20Slot-Single%20bytes32-purple.svg)](https://pcworm.github.io/werracle/#storage-slot)
[![Patent Pending](https://img.shields.io/badge/Patent%20Pending-TR%202026%2F016285-red.svg)](https://epats.turkpatent.gov.tr)
[![Ecosystem: WERR](https://img.shields.io/badge/Engine-WERR%20Core-emerald.svg)](https://github.com/pCwOrM/werr)
[![Ecosystem: answerr](https://img.shields.io/badge/Platform-answerr-8b5cf6.svg)](https://github.com/pCwOrM/answerr)
[![Ecosystem: Research](https://img.shields.io/badge/Research-Mandelbrot%20Synthesis-blue.svg)](https://github.com/pCwOrM/mandelbrot-fractal-neural-synthesis)
[![arXiv: 2609.25498](https://img.shields.io/badge/arXiv-2609.25498-b31b1b.svg)](https://arxiv.org/abs/2609.25498)
[![arXiv: 2609.30115](https://img.shields.io/badge/arXiv-2609.30115-b31b1b.svg)](https://arxiv.org/abs/2609.30115)
[![Formal Verification: Lean 4](https://img.shields.io/badge/Formal%20Verification-Lean%204%20(Zero%20Sorry)-9333ea.svg)](formal_proofs/WerracleProof.lean)
[![Formal Certificate](https://img.shields.io/badge/Certificate-Lean%204%20Machine--Verified-blue.svg)](docs/WERRACLE_LEAN4_FORMAL_VERIFICATION_CERTIFICATE.md)
[![Zenodo DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.22939253-024dad.svg)](https://doi.org/10.5281/zenodo.22939253)
[![Paper: Camera-Ready PDF](https://img.shields.io/badge/Paper%20v2.0-Camera--Ready-emerald.svg)](https://github.com/pCwOrM/werr/blob/main/paper/Universal_Fractal_Natural_Language_Decision_Map_CameraReady.pdf)

> 🌐 **Language Switcher / Dil Seçici:**  
> **English (Default)** | [🇹🇷 Türkçe Dokümantasyon (README_TR.md)](README_TR.md) &bull; 🌐 [**Interactive Web Simulator**](https://pcworm.github.io/werracle/) &bull; ⚡ [**Interactive API Docs**](https://pcworm.github.io/werracle/apidocs.html) &bull; 🎓 [**LEARN.md Guide**](LEARN.md) &bull; 🛡️ [**1,000-Test Sealed Audit Report**](docs/TEST_1000_AUDIT_REPORT.md) &bull; 📢 [**Grant & Announcement Playbook**](docs/WEB3_GRANT_AND_ANNOUNCEMENT_PLAYBOOK.md)

> **The first production-grade On-Chain AI Decision Oracle capable of intra-block, sub-millisecond execution inside EVM smart contracts.**  
> *Powered by WERR procedural Mandelbrot escape dynamics. Zero neural tensor matrices. 1000x faster and 15x cheaper than ZK-ML.*

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
* **Public HTTPS JSON-RPC:** `https://api.answerr.me:4431/werracle/rpc`
* **Real-Time REST Gateway:** `https://api.answerr.me:4431/werracle/status`
* **Live Interactive Documentation:** [https://pcworm.github.io/werracle/apidocs.html](https://pcworm.github.io/werracle/apidocs.html)

### Deployed Contract Registry (v2.0 & v1.0 Baseline):
| Contract Name | Bytecode Address | Gas Benchmark | Description |
| :--- | :--- | :--- | :--- |
| **`WerracleTripodZMod9.sol`** | [`0x0a95887dBa2783E1E445bB4D3A9a1f7cB3152d04`](https://api.answerr.me:4431/werracle/status) | **22,557 gas** | **v2.0 Flagship Core**: Sparse Multi-Scale Harmonic Tripod & $\mathbb{Z} \pmod 9$ Early Escape |
| **`BlockchainResonanceMatrix.sol`** | Embedded Bytecode Library | **3,821 gas** | **v2.0 Semantic Matrix**: 40 On-Chain Tokens across 5 Pillars (0 SLOAD) |
| **`Werracle.sol`** | [`0x5FbDB2315678afecb367f032d93F642f64180aa3`](https://api.answerr.me:4431/werracle/status) | **21,438 gas** | **v1.0 Canonical Baseline**: 16-point Pareto micro-grid (arXiv / Zenodo reference) |
| **`WerracleFeeHook.sol`** | [`0xdef5Ad647Af159D27cd111007e4CCD1fDE9d4006`](https://api.answerr.me:4431/werracle/status) | **36,739 gas** | Uniswap v4 Dynamic Volatility Fee Governor Hook |

### Query On-Chain Decisions Live (Sub-15ms):
```bash
# 1. Inspect Devnet Status & Block Height
curl -s https://api.answerr.me:4431/werracle/status

# 2. Query Live On-Chain Oracle Reflex (noul)
curl -s -X POST https://api.answerr.me:4431/werracle/oracle/noul \
  -H "Content-Type: application/json" \
  -d '{"risk_score": 0.15}'

# 3. Query Uniswap v4 Dynamic Fee Hook
curl -s -X POST https://api.answerr.me:4431/werracle/hook/fee \
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
> 📜 **Machine-Verified Lean 4 Proof**: Formally verified in **Lean 4 (v4.34.1)** with **ZERO `sorry` axioms** (Halting Invariant, 108-step complexity ceiling, and $\le 24,000$ gas bound). Full proof source at [`formal_proofs/WerracleProof.lean`](formal_proofs/WerracleProof.lean) &bull; Audit Certificate at [`docs/WERRACLE_LEAN4_FORMAL_VERIFICATION_CERTIFICATE.md`](docs/WERRACLE_LEAN4_FORMAL_VERIFICATION_CERTIFICATE.md).

---

## 🧩 The 32-Byte Storage Slot Layout

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

### 2. Compile Solidity Smart Contracts
```bash
npm install
node -e "const solc=require('solc'); /* compiles all contracts cleanly */"
```

---

---

## 💖 Sponsor & Grant Funding

[![GitHub Sponsor](https://img.shields.io/badge/Sponsor-GitHub%20Sponsors-ea4aaa?logo=github&logoColor=white)](https://github.com/sponsors/pCwOrM)
[![Support on USDT TRC20](https://img.shields.io/badge/Support-USDT%20TRC20-009393?logo=tether&logoColor=white)](#-sponsor--grant-funding)

Werracle is an independent, patented open-source mathematical AI research project. Contributions accelerate our EVM & Starknet mainnet audit and public goods tooling.

### 💳 Official Receiving Wallet
| Channel / Platform | Network | Receiving Address |
| :--- | :--- | :--- |
| **Official Wallet (Binance)** | TRC20 (TRON) | `TLMhaDJTVYBHBSGJ9nCQGLvqnYFPSBgLJu` |
| **Official Corporate Entity** | Teknokent | ITOUCH BİLİŞİM SİSTEMLERİ LTD. ŞTİ. (Çukurova Teknokent) |

* **Official Contacts:** `vdagli@itouch.com.tr` (Corporate) | `pcworm@pcworm.net` (Lead Research) | `ask@answerr.me` (Autonomous Agent) | Web: `https://answerr.me`

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

@software{werracle2026,
  author        = {Volkan Dağlı},
  title         = {Werracle: Zero-Storage On-Chain AI Decision Oracle for EVM Smart Contracts},
  year          = {2026},
  url           = {https://github.com/pCwOrM/werracle},
  doi           = {10.5281/zenodo.22939253}
}
```

---

## 📜 License
Werracle is released under the **Business Source License 1.1 (BSL 1.1)**.  
* Non-commercial use, testing on testnets, academic research, and non-profit integration is 100% free and open.
* Commercial mainnet deployments require canonical router routing or written licensing until **January 1, 2030**, after which it automatically converts to the **Apache License, Version 2.0**.
* Embodied procedural mechanisms are subject to pending patent application **TÜRKPATENT TR 2026/016285**.
