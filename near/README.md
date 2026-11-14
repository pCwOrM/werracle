<p align="center">
  <img src="../assets/werracle_logo_oracle.svg" alt="Werracle Logo Emblem" width="140" height="140" />
</p>

# ⚡ Werracle for NEAR Protocol: Intra-Block AI Shield for NEAR Intents & Chain Signatures

[![NEAR Protocol](https://img.shields.io/badge/NEAR%20Protocol-Intents%20%26%20Chain%20Signatures-00EC97.svg?logo=near&logoColor=black)](https://near.org)
[![Aurora EVM](https://img.shields.io/badge/Aurora%20EVM-Ethereum%20on%20NEAR-78D64B.svg)](https://aurora.dev)
[![Track: Unstoppable DeFi](https://img.shields.io/badge/Track%2001-Unstoppable%20DeFi-002f6c.svg)](https://nearhackathon.com)
[![Track: AI Security & Defense](https://img.shields.io/badge/Track%2002-AI%20Security%20%26%20Defense-0ea5e9.svg)](https://nearhackathon.com)
[![Track: Agent Economy](https://img.shields.io/badge/Track%2003-Agent%20Economy-10b981.svg)](https://nearhackathon.com)
[![License: BSL 1.1](https://img.shields.io/badge/License-BSL%201.1-blue.svg)](../LICENSE)
[![Formal Proof: Lean 4](https://img.shields.io/badge/Formal%20Verification-Lean%204%20(0%20Sorry)-9333ea.svg)](../formal_proofs/WerracleProof.lean)

---

## 🌟 Executive Overview for NEAR Hackathon Judges

NEAR Protocol pioneers **Chain Abstraction**, **NEAR Intents**, and **Chain Signatures**—enabling users and AI agents to transact seamlessly across Bitcoin, Ethereum, Solana, Base, and Arbitrum from a single NEAR account.

However, cross-chain execution creates a catastrophic vulnerability: **Intra-Block MEV, Flash-Loan Arbitrage, and Toxic Flow Leaks.**
* When a cross-chain swap or liquidation intent is submitted, off-chain solvers race to execute it.
* Traditional machine learning cannot defend contracts on-chain due to the **Von Neumann memory wall** (multi-gigabyte weights cost millions of gas).
* Zero-Knowledge Machine Learning (ZK-ML) introduces **10 to 300 seconds proving latency**, making intra-block reflex defense impossible.

### 🛡️ The Werracle Solution on NEAR & Aurora
**Werracle** is the world’s first production-grade, zero-storage on-chain AI decision oracle fitting inside a **single 32-byte storage slot (`bytes32`)**.

1. **Sub-Millisecond Intra-Block Execution:** Evaluates continuous non-linear fractal decision boundaries via procedural polynomial escape dynamics ($z_{n+1} = z_n^2 + c$) in **~20,700–21,400 execution gas (< $0.0001 on Aurora)**.
2. **Native Aurora Deployment:** Runs with zero code changes on **Aurora (EVM on NEAR)**, taking advantage of NEAR's 1-second finality.
3. **NEAR Intent & Chain Signature Guard:** Acts as a pre-signing reflex circuit breaker: before a Chain Signature is broadcasted to external chains, Werracle verifies orderbook volatility, pool turbulence, and toxic rebalancing signals. If an attack is detected, the intent is atomically vetoed within milliseconds.

---

## 🏗️ Architecture: How Werracle Integrates with NEAR

```
                                      [User / Autonomous AI Agent]
                                                    │
                                                    ▼
                                      [NEAR Intent Declaration]
                                      "Swap 10,000 USDC for ETH"
                                                    │
                                                    ▼
                 ┌──────────────────────────────────────────────────────────────────┐
                 │                  NEAR Protocol (Chain Signatures)                │
                 │                                                                  │
                 │   1. Solver Proposes Execution Route                             │
                 │   2. Werracle Intent Guard Call (Aurora EVM / RPC)               │
                 │      • Reads 24-byte Coordinate Seed Θ = (cx, cy, zoom)          │
                 │      • Computes Q16.16 Fixed-Point Pareto Micro-Grid (~21k gas)  │
                 │      • Evaluates Boundary: [NOUL: PASS / VETO]                   │
                 │                                                                  │
                 │   [VETO: Toxic MEV Detected]        [PASS: Clean Flow Verified]  │
                 │          │                                      │                │
                 │          ▼                                      ▼                │
                 │   Atomic Revert (<1ms)             Chain Signature Broadcast     │
                 │   0 Gas Wasted on Target           (Base, Arbitrum, Ethereum)    │
                 └──────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Live Aurora Testnet Deployment

* **Network:** Aurora Testnet (Chain ID `1313161555`)
* **RPC Endpoint:** `https://testnet.aurora.dev`
* **Explorer:** [https://explorer.testnet.aurora.dev](https://explorer.testnet.aurora.dev)
* **Lead Builder & Sovereign NEAR Account:** `pcworm.near`
* **Deployer EVM Address:** [`0x89D689A469210ef708420294B332b586d00371aF`](https://explorer.testnet.aurora.dev/address/0x89D689A469210ef708420294B332b586d00371aF)

### 📜 Verified On-Chain Deployments:
| Contract | Description | Aurora Testnet Contract Address | Deployment Tx Hash |
| :--- | :--- | :--- | :--- |
| **`Werracle.sol`** | Canonical v1.0 Pareto Oracle (16-point) | [`0x4085673F1e45bf26682CA704b2d09C03d1212cd4`](https://explorer.testnet.aurora.dev/address/0x4085673F1e45bf26682CA704b2d09C03d1212cd4) | [`0xe5e6c64...`](https://explorer.testnet.aurora.dev/tx/0xe5e6c64208f874d7a71271dec17ff9ed33dc79cce5f6c856584ed6ef15f895c9) |
| **`WerracleTripodZMod9.sol`** | Multi-Scale Sparse Tripod with $\mathbb{Z}/9\mathbb{Z}$ Lean 4 Dynamics | [`0x1d7Ae9E1dDDA805539d9e225425804Ef8B9caBaF`](https://explorer.testnet.aurora.dev/address/0x1d7Ae9E1dDDA805539d9e225425804Ef8B9caBaF) | [`0x67ccad9...`](https://explorer.testnet.aurora.dev/tx/0x67ccad988e467cd5257d0c83d9e9606cd112f86c83a6d4d710fd05a415eaea13) |

---

## 🧪 Verification, Live Cross-Chain Parity & Simulation

Run the zero-dependency NEAR Intent Guard, Chain Signatures (`v1.signer`) policy gate, and live Aurora EVM parity verifier:

```bash
# 1. Full live audit: 4 canonical intents + Aurora Testnet bit-exact EVM parity (8/8 vectors)
#    + NEAR RPC (pcworm.near, v1.signer, intents.near) + live NEAR Intents 1Click dry quote
python3 near/werracle_near_intent_guard.py

# 2. Air-gapped / deterministic modes & machine-readable agent JSON output
python3 near/werracle_near_intent_guard.py --offline
python3 near/werracle_near_intent_guard.py --json --eval-risk 2.5

# 3. Direct Aurora Testnet Foundry queries (expected: true, 5266)
cast call 0x1d7Ae9E1dDDA805539d9e225425804Ef8B9caBaF "previewDecision(bytes32,int64)(bool,uint16)" \
  0x0000000000000000000000000000000000000000000000000000000000000000 0 \
  --rpc-url https://testnet.aurora.dev

# 4. Unit tests, 1,000-test sealed battery & Foundry smart contract suite
python3 -m pytest -q
python3 tests/run_1000_sealed_battery.py
forge test
```

### Key Metrics
* **Storage Footprint:** Single 32-byte slot (`bytes32`)
* **Inference Gas Cost:** ~20,700–21,438 execution gas (`86,813` measured Aurora Testnet tx gas estimate for `decideNoul`; < $0.0001 on Aurora)
* **Execution Latency:** < 1 millisecond (~40–55 us in Python Q16.16)
* **Formal Verification:** 40 core Werracle Lean 4 theorems (`formal_proofs/`, 0 `sorry`; 170+ across the broader WERR research corpus)
* **Audit & Test Suites:** 1,000/1,000 sealed test battery + 22/22 `pytest` tests + 7/7 `forge test` Foundry tests

---

## 📋 Hackathon Baseline & Diff Disclosure (Rules Q-002 / Q-003 / Q-005)

* **Pre-Hackathon Baseline ([`pre-hackathon`](https://github.com/pCwOrM/werracle/tree/pre-hackathon) tag, Oct 18 2026):** Core Q16.16 fixed-point research kernel (`engine/`), early Solidity v1 prototype, initial 1,000-test battery, and baseline Lean 4 formalizations.
* **Built During NEAR Hackathon 2026 ([Compare `pre-hackathon...hackathon-submission`](https://github.com/pCwOrM/werracle/compare/pre-hackathon...hackathon-submission)):**
  * [`near/werracle_near_intent_guard.py`](werracle_near_intent_guard.py) & [`tests/test_near_intent_guard.py`](../tests/test_near_intent_guard.py): Bit-exact Q16.16 `WerracleTripodZMod9` Python port, Chain Signatures (`v1.signer`) pre-signing policy gate, live NEAR Intents 1Click API (`1click.chaindefuser.com/v0`) quote slippage audit, NEAR RPC account checks, and live Aurora Testnet parity verification.
  * Live **Aurora Testnet** deployments (`0x1d7Ae9E1dDDA805539d9e225425804Ef8B9caBaF` & `0x4085673F1e45bf26682CA704b2d09C03d1212cd4`), [`deploy_aurora_testnet.sh`](deploy_aurora_testnet.sh), and [`NEAR_INTENTS_AND_AURORA_INTEGRATION_SPEC.md`](../docs/NEAR_INTENTS_AND_AURORA_INTEGRATION_SPEC.md).
  * Interactive Q16.16 Aurora simulator portal ([`werracle.io`](https://werracle.io)) & OEV/liquidation telemetry observatory ([`radar.werracle.com`](https://radar.werracle.com)), extended 40-theorem Lean 4 core proof files, and Starknet/Foundry verification harnesses.
* **Reused Tooling / Libraries:** Python 3.11+ standard library (zero external pip dependencies for NEAR Guard & 1,000-test battery), Solidity `^0.8.20` + Foundry, Lean 4 + Mathlib4 (`formal_proofs/`), self-hosted Three.js.
