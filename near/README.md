# ⚡ Werracle for NEAR Protocol: Intra-Block AI Shield for NEAR Intents & Chain Signatures

[![NEAR Protocol](https://img.shields.io/badge/NEAR%20Protocol-Intents%20%26%20Chain%20Signatures-00EC97.svg?logo=near&logoColor=black)](https://near.org)
[![Aurora EVM](https://img.shields.io/badge/Aurora%20EVM-Ethereum%20on%20NEAR-78D64B.svg)](https://aurora.dev)
[![Track: Unstoppable DeFi](https://img.shields.io/badge/NEAR%20Hackathon%202026-01%20%2F%20Unstoppable%20DeFi-002f6c.svg)](https://nearhackathon.com)
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

1. **Sub-Millisecond Intra-Block Execution:** Evaluates continuous non-linear decision boundaries via procedural Mandelbrot escape dynamics (\(z_{n+1} = z_n^2 + c\)) in **~21,400 gas (< $0.0001)**.
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

## 🧪 Verification & Simulation

You can run the standalone NEAR Intent Guard verification simulation directly:

```bash
# Run the NEAR Intent Guard & Chain Signature Verification Battery
python3 near/werracle_near_intent_guard.py
```

### Key Metrics:
* **Storage Footprint:** Single 32-byte slot (`bytes32`)
* **Inference Gas Cost:** ~21,438 gas (~$0.00005 on Aurora)
* **Execution Latency:** < 1 millisecond
* **Formal Verification:** 40 Machine-Certified Lean 4 Theorems (0 sorry, 0 axioms)
* **Audit Suite:** 1,000 Cryptographically Sealed Test Cases (100.0% Pass Rate)
