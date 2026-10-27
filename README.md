<div align="center">

# WERRACLE
### Zero-Storage On-Chain AI Decision Oracle & DeFi Risk Radar

[![License: BSL 1.1](https://img.shields.io/badge/License-BSL_1.1-0ea5e9.svg)](LICENSE)
[![Solidity: ^0.8.24](https://img.shields.io/badge/Solidity-^0.8.24%20(Q16.16)-6366f1.svg)](contracts/)
[![EVM Devnet: Chain ID 4242](https://img.shields.io/badge/EVM_Devnet-Chain_4242-10b981.svg)](https://api.answerr.me/rpc)
[![Zenodo DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.22942598-f59e0b.svg)](https://doi.org/10.5281/zenodo.22942598)
[![arXiv Preprint](https://img.shields.io/badge/arXiv-2609.30719-b91c1c.svg)](https://arxiv.org/abs/2609.30719)
[![Live Radar](https://img.shields.io/badge/Live_Telemetry-radar.werracle.com-38bdf8.svg)](https://radar.werracle.com)

<p align="center">
  <b>A zero-storage, fixed-point procedural decision oracle that executes deterministic AI reflexes directly inside the Ethereum Virtual Machine (EVM)—enabling dynamic Uniswap v4 fee hooks, sub-block MEV defense, and real-time lending vault risk telemetry without off-chain trust assumptions.</b>
</p>

[Quickstart](#-quickstart--deployment) •
[Architecture](#-on-chain-fractal-architecture) •
[Smart Contracts](#-smart-contract-suite) •
[Empirical Results](#-empirical-benchmarks--svr-telemetry) •
[Live Risk Radar](#-werracle-risk-radar) •
[Ecosystem](#-the-werr-ecosystem) •
[Research Chronology](RESEARCH_CHRONOLOGY.md) •
[Türkçe Dokümantasyon](README_TR.md)

</div>

---

## 🏛️ The Paradigm

Decentralized finance (DeFi) protocols face a fundamental trilemma between **oracle latency**, **gas overhead**, and **trust minimization**:
1. **Traditional Push/Pull Oracles:** Depend on off-chain multi-signatures, third-party node networks, or delayed price updates—exposing Automated Market Makers (AMMs) to Loss-Versus-Rebalancing (LVR) and toxic MEV arbitrage.
2. **Deep Neural Inference:** Generative LLMs and multi-layer neural networks cannot be computed on-chain; evaluating gigabytes of float weights in EVM bytecode exceeds block gas limits by several orders of magnitude.

**Werracle** breaks this barrier by porting the **WERR** procedural fractal reflex engine into native EVM bytecode:
* **Zero-Storage Footprint:** Requires **0 bytes** of state storage for neural weights. Decision boundaries are geometric invariants computed on the fly.
* **Deterministic Q16.16 Fixed-Point Math:** Employs fixed-point polynomial boundary escape dynamics ($z_{n+1} = z_n^2 + c$) implemented in optimized Solidity assembly.
* **Sub-Block Execution Latency:** Computes full reflex verification in **$< 42,000$ gas** on Ethereum L1 and sub-cent transaction costs on Base / Arbitrum L2s.

```
       Incoming Trade / Liquidation Transaction
                          │
                          ▼
       ┌──────────────────────────────────────┐
       │     Uniswap v4 Pool / Morpho Vault   │
       └──────────────────┬───────────────────┘
                          │ Call beforeSwap() / liquidate()
                          ▼
       ┌──────────────────────────────────────┐
       │       WerracleCore (On-Chain)        │
       │   Q16.16 Fixed-Point Fractal Engine  │  ◄── Zero Storage Weights
       │          Gas: ~38,500 units          │
       └──────────────────┬───────────────────┘
                          │
             ┌────────────┴────────────┐
             ▼                         ▼
   [Dynamic Swap Fee]        [Reflex Protection]
  Recaptures LVR/MEV        Halts bad-debt cascades
```

---

## ⚡ Quickstart & Deployment

### Contract Installation (Foundry)

```bash
forge install pCwOrM/werracle
```

*Or install via npm/yarn:*

```bash
npm install @werracle/contracts
```

### Basic Contract Integration

```solidity
// SPDX-License-Identifier: BUSL-1.1
pragma solidity ^0.8.24;

import {IWerracleOracle} from "@werracle/contracts/interfaces/IWerracleOracle.sol";

contract SafeVault {
    IWerracleOracle public immutable oracle;

    constructor(address _oracle) {
        oracle = IWerracleOracle(_oracle);
    }

    function executeProtectedAction(bytes32 poolId, uint256 volatility) external {
        // Query the zero-storage reflex oracle
        // Returns: 0 = Allow / Normal, 1 = Caution / Elevated Fee, 2 = Emergency Gate
        uint8 decision = oracle.evaluateRisk(poolId, volatility);
        
        require(decision != 2, "Werracle: Emergency volatility reflex triggered");
        
        // Execute state transition...
    }
}
```

---

## 📐 Smart Contract Suite

The repository contains audited Solidity implementations for EVM execution:

| Contract | Purpose | Gas Profile | Target Networks |
|---|---|---|---|
| [`WerracleCore.sol`](contracts/WerracleCore.sol) | Canonical on-chain reflex oracle with Q16.16 escape math | ~38,500 gas | Ethereum L1, Base, Arbitrum |
| [`WerracleUniswapV4Hook.sol`](contracts/hooks/WerracleUniswapV4Hook.sol) | `beforeSwap` dynamic fee hook mitigating toxic LVR | ~41,200 gas | Base L2, Uniswap v4 Deployments |
| [`WerracleMorphoSVR.sol`](contracts/adapters/WerracleMorphoSVR.sol) | MetaMorpho vault health monitoring & SVR recapture | ~32,000 gas | Ethereum L1 / Base L2 |
| [`FixedPointFractal.sol`](contracts/libraries/FixedPointFractal.sol) | Math library computing iterative complex orbital escape | Pure library | EVM Bytecode compatible |

---

## 📊 Empirical Benchmarks & SVR Telemetry

Werracle's Smart Value Recapture (SVR) and dynamic fee hooks have undergone extensive stress simulations and live testnet benchmarks:

* **Smart Value Recapture (SVR):** Achieved **94.38%** value recapture on volatile arbitrage events compared to static 30 bps Uniswap pools.
* **FastLane Atlas Solver Benchmarks:** Demonstrated microsecond-level reflex arbitration across adversarial backrunning bundles.
* **MetaMorpho Lending Resilience:** Successfully prevented bad-debt cascade triggers across synthetic liquidation shocks.

Detailed simulation scripts, Monte Carlo runs, and contract gas profiler logs are available in [RESEARCH_CHRONOLOGY.md](RESEARCH_CHRONOLOGY.md).

---

## 📡 Werracle Risk Radar

Werracle powers an enterprise-grade live risk intelligence dashboard accessible at:

🔗 **[https://radar.werracle.com](https://radar.werracle.com)**

* **Live MetaMorpho Vault Telemetry:** Real-time collateralization monitoring, supply/borrow APY volatility, and bad debt exposure metrics.
* **Base L2 Execution Feeds:** Real-time streaming of on-chain reflex transactions, dynamic swap fee adjustments, and MEV protection events.
* **Institutional DaaS API:** Low-latency REST & WebSocket feeds for quantitative market makers and decentralized protocols.

---

## 🌐 The WERR Ecosystem

Werracle represents the decentralized execution tier of the WERR foundational architecture:

```
                          ┌─────────────────────────────┐
                          │            WERR             │
                          │   Core Mathematical Engine  │
                          │  Zero-Memory System-1 Reflex │
                          └──────────────┬──────────────┘
                                         │
                 ┌───────────────────────┴───────────────────────┐
                 ▼                                               ▼
  ┌─────────────────────────────┐                 ┌─────────────────────────────┐
  │          Werracle           │                 │           answerr           │
  │   On-Chain Decision Oracle  │                 │  Dual-Cognition Workspace   │
  │  DeFi Risk Radar & DaaS     │                 │ Natural Language Gating API │
  │   https://radar.werracle.com│                 │     https://answerr.me      │
  └─────────────────────────────┘                 └─────────────────────────────┘
```

* **[`werr`](https://github.com/pCwOrM/werr):** The core zero-memory fractal reflex engine and Lean 4 formally verified mathematical proofs.
* **`werracle`:** On-chain Solidity implementations, Uniswap v4 hooks, and decentralized risk radar.
* **[`answerr`](https://github.com/pCwOrM/answerr):** Natural language dual-cognition workspace connecting System-2 deliberation to deterministic reflex execution.

---

## 📄 Academic Citation & Archival References

If you cite or replicate this research in scientific publications, please use the following metadata:

```bibtex
@article{dagli2026werracle,
  author       = {Dağlı, Volkan and Dağlı, Zerrin and Dağlı, Dağhan},
  title        = {{Werracle: Zero-Storage On-Chain AI Decision Oracle via Procedural Fractal Dynamics}},
  journal      = {arXiv preprint arXiv:2609.30719},
  year         = {2026},
  doi          = {10.48550/arXiv.2609.30719},
  publisher    = {Zenodo},
  version      = {v1.0.0},
  note         = {Zenodo DOI: 10.5281/zenodo.22942598}
}
```

* **SSRN Research Abstract:** SSRN: 7626279 ([https://ssrn.com/abstract=7626279](https://ssrn.com/abstract=7626279))
* **Full Research Chronology:** [`RESEARCH_CHRONOLOGY.md`](RESEARCH_CHRONOLOGY.md)

---

## ⚖️ License & Intellectual Property

* **Open-Science, Educational & Evaluation Use:** The Licensed Work is free to run, inspect, benchmark, test, fork, and replicate for all non-commercial academic research, personal evaluations, and public testnet deployments under the **Business Source License 1.1 (BSL 1.1)**.
* **Commercial Operations & Production Licensing:** Any commercial mainnet deployment, integration into fee-generating DeFi protocols, or proprietary SaaS/DaaS operation requires a written Commercial License from the Licensor:
  * **Licensor:** `ITOUCH BİLİŞİM SİSTEMLERİ MÜHENDİSLİK DANIŞMANLIK SANAYİ VE TİCARET LİMİTED ŞİRKETİ` (`ITouch Systems` · Çukurova Teknokent / Cukurova University Science Park, Adana, Türkiye).
  * **Scientific Co-Authors & Inventors:** Volkan Dağlı (*Anadolu University*), Dr. Zerrin Dağlı (*Academic Advisor, Co-Author & Co-Inventor*), Dağhan Dağlı (*Co-Author & Co-Inventor — Toros University / Toros Science High School*).
  * **Patent Applications:** TÜRKPATENT **TR 2026/016285** & **TR 2026/016633**.
  * **Inquiries:** `contact@werracle.com` · `info@itouch.com.tr`

---

<div align="center">
  <sub>Developed by ITouch Systems · Cukurova University Science Park, Adana, Turkey</sub><br>
  <sub>Copyright &copy; 2026 ITouch Bilişim Sistemleri Ltd. Şti. All rights reserved.</sub>
</div>
