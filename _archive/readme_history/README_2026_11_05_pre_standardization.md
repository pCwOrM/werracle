<div align="center">

# WERRACLE
### Zero-Storage On-Chain AI Decision Oracle & DeFi Risk Radar

[![License: BSL 1.1](https://img.shields.io/badge/License-BSL_1.1-0ea5e9.svg)](LICENSE)
[![Solidity: ^0.8.24](https://img.shields.io/badge/Solidity-^0.8.24%20(Q16.16)-6366f1.svg)](contracts/)
[![EVM Devnet: Chain ID 4242](https://img.shields.io/badge/EVM_Devnet-Chain_4242-10b981.svg)](https://api.answerr.me/werracle/status)
[![Zenodo DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.22942598-f59e0b.svg)](https://doi.org/10.5281/zenodo.22942598)
[![arXiv Preprint](https://img.shields.io/badge/arXiv-2609.30719-b91c1c.svg)](https://arxiv.org/abs/2609.30719)
[![Live Radar](https://img.shields.io/badge/Live_Telemetry-radar.werracle.com-38bdf8.svg)](https://radar.werracle.com)

<p align="center">
  <b>A zero-storage, fixed-point procedural decision oracle that executes deterministic AI reflexes directly inside the Ethereum Virtual Machine (EVM)—enabling dynamic Uniswap v4 fee hooks, sub-block MEV defense, and real-time lending vault risk telemetry without off-chain trust assumptions.</b>
</p>

[Quickstart](#-quickstart--deployment) •
[Architecture](#️-the-paradigm) •
[Smart Contracts](#-smart-contract-suite) •
[Empirical Results](#-empirical-benchmarks--svr-telemetry) •
[Live Risk Radar](#-werracle-risk-radar) •
[Ecosystem](#-the-werr-ecosystem) •
[Research Chronology](RESEARCH_CHRONOLOGY.md) •
[Türkçe Dokümantasyon](README_TR.md) •
[NEAR Hackathon Guide](near/README.md)

</div>

> ⚡ **NEAR HACKATHON 2026 OFFICIAL SUBMISSION (Tracks: Unstoppable DeFi, AI Security & Defense, Agent Economy)**:
> For Hackathon judges, AI screening agents, and developers: Please inspect the dedicated **[NEAR & Aurora EVM Architecture Guide (`near/README.md`)](near/README.md)** and **[Technical Specification (`docs/NEAR_INTENTS_AND_AURORA_INTEGRATION_SPEC.md`)](docs/NEAR_INTENTS_AND_AURORA_INTEGRATION_SPEC.md)** with live Aurora Testnet contracts, interactive simulation battery (`python3 near/werracle_near_intent_guard.py`), and 1,000-test sealed benchmark suite (`python3 tests/run_1000_sealed_battery.py`).

---

## 🏛️ The Paradigm

Decentralized finance (DeFi) protocols face a fundamental trilemma between **oracle latency**, **gas overhead**, and **trust minimization**:
1. **Traditional Push/Pull Oracles:** Depend on off-chain multi-signatures, third-party node networks, or delayed price updates—exposing Automated Market Makers (AMMs) to Loss-Versus-Rebalancing (LVR) and toxic MEV arbitrage.
2. **Deep Neural Inference:** Generative LLMs and multi-layer neural networks cannot be computed on-chain; evaluating gigabytes of float weights in EVM bytecode exceeds block gas limits by several orders of magnitude.

**Werracle** breaks this barrier by porting the **WERR** procedural fractal reflex engine into native EVM bytecode:
* **Zero-Storage Footprint:** Requires **0 bytes** of state storage for neural weights. Decision boundaries are geometric invariants computed on the fly.
* **Deterministic Q16.16 Fixed-Point Math:** Employs fixed-point polynomial escape dynamics ($z_{n+1} = z_n^2 + c$) to derive non-linear fractal decision boundaries directly in optimized Solidity assembly.
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

### 1. Run Zero-Dependency Verification & Simulation Suites

```bash
# 1. NEAR Intent Guard & Chain Signature Reflex Simulation (4 scenarios)
python3 near/werracle_near_intent_guard.py

# 2. Q16.16 Fixed-Point EVM Cross-Validation Suite
python3 sim/test_cross_validation.py

# 3. 1,000-Test Cryptographically Sealed Audit Battery
python3 tests/run_1000_sealed_battery.py
```

### 2. Query Live Aurora Testnet Contracts (Chain ID `1313161555`)

```bash
# Query Werracle.sol (v1.0) on Aurora Testnet
cast call 0x4085673F1e45bf26682CA704b2d09C03d1212cd4 "owner()(address)" --rpc-url https://testnet.aurora.dev

# Query WerracleTripodZMod9.sol (v2.0) live decision reflex on Aurora Testnet
cast call 0x1d7Ae9E1dDDA805539d9e225425804Ef8B9caBaF "previewDecision(bytes32,int64)(bool,uint16,int64,int64)" 0x0000000000000000000000000000000000000000000000000000000000000000 0 --rpc-url https://testnet.aurora.dev
```

### 3. Contract Installation (Foundry)

```bash
forge install pCwOrM/werracle
forge build
```

### Basic Contract Integration

```solidity
// SPDX-License-Identifier: BSL-1.1
pragma solidity ^0.8.20;

import {IWerracle} from "werracle/contracts/IWerracle.sol";

contract SafeVault {
    IWerracle public immutable oracle;

    constructor(address _oracle) {
        oracle = IWerracle(_oracle);
    }

    function executeProtectedAction(bytes32 stateHash, int64 riskScoreFP) external payable {
        // Query the zero-storage reflex oracle in the same transaction (~20.7k gas)
        (bool allowed, ) = oracle.decideNoul{value: msg.value}(stateHash, riskScoreFP);
        
        require(allowed, "Werracle: Emergency volatility reflex triggered");
        
        // Execute protected state transition...
    }
}
```

---

## 📐 Smart Contract Suite

The repository contains verified Solidity implementations for EVM and Aurora execution:

| Contract | Purpose | Gas Profile | Target Networks |
|---|---|---|---|
| [`WerracleTripodZMod9.sol`](contracts/WerracleTripodZMod9.sol) | v2.0 Flagship Multi-Scale Sparse Tripod with $\mathbb{Z}/9\mathbb{Z}$ Lean 4 dynamics | ~20,700 gas | Aurora (NEAR), Ethereum, Base, Arbitrum |
| [`Werracle.sol`](contracts/Werracle.sol) | v1.0 Canonical on-chain reflex oracle with 16-point Q16.16 escape math | ~21,400 gas | Aurora (NEAR), Ethereum, Base, Arbitrum |
| [`WerracleFeeHook.sol`](contracts/hooks/WerracleFeeHook.sol) | Uniswap v4 `beforeSwap` dynamic fee hook mitigating toxic LVR | ~24,800 gas | Base L2, Uniswap v4 Deployments |
| [`PancakeWerracleHook.sol`](contracts/hooks/PancakeWerracleHook.sol) | PancakeSwap v4 CLPool dynamic fee & circuit-breaker hook | ~25,100 gas | BNB Chain, Base L2 |
| [`WerrMath.sol`](contracts/WerrMath.sol) | Pure Q16.16 fixed-point polynomial orbital escape library | Pure library | All EVM-compatible chains |
| [`BlockchainResonanceMatrix.sol`](contracts/BlockchainResonanceMatrix.sol) | Procedural coordinate seed and resonance calibration matrix | Pure / View | All EVM-compatible chains |
| [`IWerracle.sol`](contracts/IWerracle.sol) | Standard Solidity interface (`decideNoul`, `decideChoice`, `decideScore`) | Interface | All EVM-compatible chains |

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
* **`werracle`:** On-chain Solidity implementations, NEAR / Aurora Intent Guards, Uniswap v4 hooks, and decentralized risk radar ([werracle.io](https://werracle.io)).
* **[`answerr`](https://github.com/pCwOrM/answerr):** Natural language dual-cognition workspace connecting System-2 deliberation to deterministic reflex execution.
* **[`hermes-werracle-guard`](https://github.com/pCwOrM/hermes-werracle-guard):** Autonomous EVM pre-execution circuit breaker (`pre_tool_call`) and transaction simulation plugin for Nous Research Hermes Agent.

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
  * **Licensor:** `ITOUCH BİLİŞİM SİSTEMLERİ MÜHENDİSLİK DANIŞMANLIK SANAYİ VE TİCARET LİMİTED ŞİRKETİ` (`ITouch Systems` · Cukurova University Science Park, Adana, Türkiye).
  * **Scientific Co-Authors & Inventors:** Volkan Dağlı (*Anadolu University*), Dr. Zerrin Dağlı (*Mersin University — Academic Advisor, Co-Author & Co-Inventor*), Dağhan Dağlı (*Toros University — Co-Author & Co-Inventor*).
  * **Chain of Title & Assignment:** The scientific co-authors have irrevocably assigned administrative and IP management authority to Volkan Dağlı, who has transferred exclusive global commercial licensing and operational rights to ITouch Systems.
  * **Trademarks:** `WERR™`, `Werracle™`, `answerr™`, and `WerrSoma™` are trademarks owned exclusively by ITouch Systems.
  * **Patent Applications:** TÜRKPATENT **TR 2026/016285** & **TR 2026/016633**.
  * **Inquiries:** `contact@werracle.com` · `info@itouch.com.tr`

---

<div align="center">
  <sub>Developed by ITouch Systems · Cukurova University Science Park, Adana, Turkey</sub><br>
  <sub>Copyright &copy; 2026 ITouch Bilişim Sistemleri Ltd. Şti. All rights reserved.</sub>
</div>
