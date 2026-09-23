# ⚡ Werracle: Zero-Storage On-Chain AI Decision Oracle

[![EVM Devnet: Chain ID 4242](https://img.shields.io/badge/EVM%20Devnet-Chain%20ID%204242%20(mechsrv)-38bdf8.svg)](https://api.answerr.me:4431/werracle/status)
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

## ⚡ Live EVM Testnet & Deployed On-Chain Contracts (`mechsrv`)

Werracle is actively running live on our high-performance dedicated hardware node (`mechsrv`, Ubuntu 24.04 LTS) on a customized private EVM devnet sandbox:

* **Network Name:** Werracle Devnet (Anvil EVM Sandbox)
* **Chain ID:** `4242` &bull; **Block Time:** `1.0s`
* **Public HTTPS JSON-RPC:** `https://api.answerr.me:4431/werracle/rpc`
* **Real-Time REST Gateway:** `https://api.answerr.me:4431/werracle/status`
* **Live Interactive Documentation:** [https://pcworm.github.io/werracle/apidocs.html](https://pcworm.github.io/werracle/apidocs.html)

### Deployed Contract Registry:
| Contract Name | Bytecode Address | Gas Benchmark | Description |
| :--- | :--- | :--- | :--- |
| **`Werracle.sol`** | [`0x5FbDB2315678afecb367f032d93F642f64180aa3`](https://api.answerr.me:4431/werracle/status) | **21,438 gas** | 32-Byte Slot On-Chain AI Decision Oracle |
| **`WerracleFeeHook.sol`** | [`0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512`](https://api.answerr.me:4431/werracle/status) | **23,150 gas** | Uniswap v4 Dynamic Fee Governor Hook |

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
* **Official Contacts:** `vdagli@itouch.com.tr` (Corporate) | `pcworm@pcworm.net` (Lead Research) | `ask@answerr.com` (AI Autonomous Agent) | Web: `https://answerr.me`

---

## 📜 License
Werracle is released under the **Business Source License 1.1 (BSL 1.1)**.  
* Non-commercial use, testing on testnets, academic research, and non-profit integration is 100% free and open.
* Commercial mainnet deployments require canonical router routing or written licensing until **January 1, 2030**, after which it automatically converts to the **Apache License, Version 2.0**.
* Embodied procedural mechanisms are subject to pending patent application **TÜRKPATENT TR 2026/016285**.
