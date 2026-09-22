# 📄 WERRACLE — One-Pager Technical Executive Summary
### Zero-Storage On-Chain AI Decision Oracle in a Single 32-Byte EVM Storage Slot

---

## ⚡ The Breakthrough
**Werracle** is the first production-grade **On-Chain AI Decision Oracle** capable of running native, typed intelligence (`noul`, `choice`, `score`) entirely inside the Ethereum Virtual Machine (EVM) for **~18,000 – 25,000 gas** ($< $0.001 on L2s) with **0 Bytes of stored neural tensor matrices**.

| Metric | Traditional LLM / Web2 Oracle | ZK-ML (EZKL, Modulus) | **WERRACLE (EVM Native)** |
| :--- | :--- | :--- | :--- |
| **Model Weight Storage** | Gigabytes (Cloud/Server) | Off-chain Prover Cluster | **0 Bytes (Procedural Geometry)** |
| **On-Chain Footprint** | N/A (Signed Off-chain Data) | Verification Keys & Proofs | **Single 32-Byte Slot (`bytes32`)** |
| **Execution Latency** | 12 – 36 seconds (Network) | 10 – 300 seconds (SNARK generation) | **< 1 ms (Intra-Block / Atomic)** |
| **Gas Cost** | ~40,000 – 80,000 gas | ~250,000 – 500.000 gas | **~18,000 – 24,000 gas** |
| **Flash-Loan Defense** | ❌ Impossible (Too slow) | ❌ Impossible (Cross-block) | **✅ Native (Atomic Revert)** |
| **External Dependencies** | Multi-Sig / Web2 API Bridges | Heavy Prover Hardware | **ZERO (100% Autonomous EVM)** |

---

## 🧩 How It Works: The 24-Byte Slot Advantage

1. **Storage Packing (Single `bytes32` Slot):**
   * The complete decision model seed $\Theta = (c_x, c_y, \text{zoom})$ requires only **24 bytes**.
   * It is packed into Ethereum's atomic 32-byte storage slot alongside update nonces, decision thresholds, and operational flags.
   * Reading the entire brain via `SLOAD` costs just **100 gas** (warm slot).

2. **Fixed-Point Q16.16 Micro-Grid Arithmetic:**
   * Eliminates floating-point needs. Computes $z_{n+1} = z_n^2 + c$ using pure integer bit-shifts (`>> 16`).
   * Evaluates a **16-point ($4 \times 4$) Pareto micro-grid** across 4 quadrants to extract procedural synaptic weights ($w_1, w_2, w_3, \text{bias}$) on the fly.

3. **Three Strongly-Typed Primitives:**
   * **`noul`**: Probabilistic Boolean gate for access control, flash-loan circuit breakers, and transaction approval.
   * **`choice`**: 4-quadrant discrete routing for DEX order flow and dynamic pool paths.
   * **`score`**: Continuous [0..3] severity index for lending health factors and dynamic AMM fees.

---

## 💰 Monetization & Value Accrual
* **Micro Protocol Fee:** Built-in configurable `protocolFee` (e.g. 0.00005 ETH ~ $0.15) paid per decision query, routing sustainable revenue directly to the protocol treasury/deployer.
* **Uniswap v4 Dynamic Fee Hook:** `WerracleFeeHook.sol` dynamically adjusts swap fees (0.05% to 0.50%) based on real-time pool volatility, sharing hook fee yields.
* **License Model:** Business Source License 1.1 (BSL 1.1) protects commercial mainnet exclusivity for 2 years while remaining fully open-source and free for developers and researchers.

---

## 🎯 Target Ecosystems
* **Ethereum Mainnet, Base, Arbitrum One / Stylus, Optimism, Polygon, Avalanche.**
* **GitHub Repository:** `https://github.com/pCwOrM/werracle`
* **Contact & Research Lead:** Volkan Dağlı (`@pCwOrM`), ITouch Systems & Anadolu University.
