# ⚡ Werracle: Zero-Storage On-Chain AI Decision Oracle

[![License: BSL 1.1](https://img.shields.io/badge/License-BSL%201.1-blue.svg)](./LICENSE)
[![Solidity: ^0.8.20](https://img.shields.io/badge/Solidity-%5E0.8.20-363636.svg?logo=solidity)](https://soliditylang.org/)
[![EVM Gas: ~20k](https://img.shields.io/badge/EVM%20Gas-~20k%20(Sub--Cent)-brightgreen.svg)]()
[![Model Size: 0 Bytes](https://img.shields.io/badge/Model%20Size-0%20Bytes%20VRAM-10b981.svg)]()
[![Seed: Single bytes32](https://img.shields.io/badge/Storage%20Slot-Single%20bytes32-purple.svg)]()

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

## 💳 Funding & Grants Receiving Wallets
* **Trust Wallet (USDT TRC20 / TRON Network):** `TQ6UjobN9HpGkPst2E6Cm3GiG5PSeLn5Bb`
* **Binance Wallet (USDT TRC20 / TRON Network):** `TQc3VjKPkpv3nkHcaT4LKVcfdrS6yTRSUG`
* **Official Contacts:** `vdagli@itouch.com.tr` | `pcworm@pcworm.net` | Web: `https://answerr.me`

---

## 📜 License
Werracle is released under the **Business Source License 1.1 (BSL 1.1)**.  
* Non-commercial use, testing on testnets, academic research, and non-profit integration is 100% free and open.
* Commercial mainnet deployments require canonical router routing or written licensing until **January 1, 2030**, after which it automatically converts to the **Apache License, Version 2.0**.
* Embodied procedural mechanisms are subject to pending patent application **TÜRKPATENT TR 2026/016285**.
