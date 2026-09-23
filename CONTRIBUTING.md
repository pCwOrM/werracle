# Contributing to Werracle

Thank you for your interest in contributing to **Werracle** — the first zero-storage, machine-native On-Chain AI Decision Oracle and dynamic fee governor for EVM smart contracts!

We welcome contributions ranging from Solidity gas optimizations, L2 deployments (Arbitrum, Base, Optimism, Polygon, Avalanche), novel Uniswap v4 pool hooks, to simulation battery extensions and documentation.

---

## 🏛️ Foundational Architectural Guarantees

Werracle operates under strict engineering and security contracts. Any proposed pull request must adhere to these non-negotiables:

1. **Single 32-Byte Storage Slot Footprint:**  
   All parameter updates, coordinates $(c_x, c_y, \text{zoom})$, nonces, and thresholds must pack cleanly into a single `bytes32` EVM storage word. Core contracts must NEVER allocate multi-slot floating point weight tables.
2. **Ultra-Low Gas Execution (< 25,000 gas):**  
   Forward decisions (`noul`, `choice`, `score`) must execute within ~18,000 to 24,000 gas on standard EVM environments.
3. **Deterministic Mathematical Parity:**  
   Q16.16 fixed-point arithmetic in Solidity bytecode (`WerrMath.sol`) must maintain 100.0% bitwise parity with the reference Python simulation.
4. **Air-Gapped Privacy & Zero Telemetry:**  
   Telemetry is permanently disabled. Werracle must NEVER make external HTTP calls or leak transaction parameters off-chain.

---

## 🛠️ Development & Testing Setup

### 1. Clone the Repository
```bash
git clone https://github.com/pCwOrM/werracle.git
cd werracle
git checkout -b feature/your-feature-name
```

### 2. Run the 1,000-Test Sealed Battery
Ensure that all 1,000 test cases pass cleanly with zero regression:
```bash
python tests/run_1000_sealed_battery.py
```

### 3. Smart Contract Verification (Foundry / Hardhat)
If you have Foundry installed:
```bash
forge test
```
Or using solc directly:
```bash
npx hardhat compile
```

---

## 🤝 GitHub Education & Community Exchange

Werracle actively participates in **GitHub Global Campus Community Exchange** ("Collaborate and Learn"). Students, researchers, and early-career developers are encouraged to:
* Propose novel DeFi defense gates (e.g., cross-chain bridge validation, MEV bundle detection).
* Port Werracle to non-EVM environments (Solana, Move/Sui, NEAR, Cairo).
* Benchmark gas costs across different Ethereum Layer-2 rollups.

Please review our [Code of Conduct](CODE_OF_CONDUCT.md) before participating.
Questions, mentorship requests, or technical clarifications can be sent to **`ask@answerr.me`** (Autonomous AI Co-developer) or **`pcworm@pcworm.net`** / **`vdagli@itouch.com.tr`**.
