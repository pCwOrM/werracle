# 🎓 Learning Werracle: Zero-Storage On-Chain AI & Dynamic EVM Governance

Welcome to **Werracle** (Wave Error Reflex Oracle)!

This educational guide is built for students, blockchain researchers, and DeFi engineers participating in the **GitHub Education Community Exchange**. It provides hands-on tutorials to understand how zero-storage fractal math, EVM fixed-point arithmetic (Q16.16), and Uniswap v4 dynamic fee hooks work in practice.

---

## 🏛️ 1. What You Will Learn

1. **Why Floating-Point Math Fails on Ethereum:**  
   The Ethereum Virtual Machine (EVM) operates strictly on integers (uint256/int256). Learn how fixed-point arithmetic ($Q16.16$) represents fractional numbers with precision without gas-heavy decimal libraries.
2. **Zero-Storage Machine Cognition:**  
   Instead of storing megabytes of neural network weights in expensive EVM storage slots ($20,000$ gas per `SSTORE`), learn how procedural mathematical attractors synthesize decisions in real time using ephemeral memory.
3. **Flash-Loan & MEV Defense:**  
   How on-chain automated market makers (AMMs) can dynamically adjust swap fees or reject atomic multi-million-dollar borrowing spikes within the very same transaction.

---

## 📐 2. The Core Math: Fixed-Point Q16.16 Explained

In `contracts/libraries/WerrMath.sol`, all numbers are represented as signed 256-bit integers with a fixed scale factor:

$$\text{Fixed-Point Value} = \text{Float Value} \times 2^{16} = \text{Float Value} \times 65536$$

### Quick Conversion Table:
| Real Number | Q16.16 Fixed Point (Integer) | Hex Representation |
| :--- | :--- | :--- |
| `1.0` | `65536` | `0x00010000` |
| `0.5` | `32768` | `0x00008000` |
| `-0.75` | `-49152` | `0xFFFF4000` |
| `0.0001` | `7` | `0x00000007` |

### Multiplication in Q16.16:
```solidity
// Multiplying two Q16.16 numbers requires bit-shifting right by 16 to avoid quadratic scaling:
function mulFP(int256 a, int256 b) internal pure returns (int256) {
    return (a * b) >> 16;
}
```

---

## 🧪 3. Hands-On Tutorials

### Tutorial 1: Run the 1,000-Test Deterministic Battery
Verify bitwise parity between the Solidity bytecode and reference Python math:

```bash
# Clone the repository
git clone https://github.com/pCwOrM/werracle.git
cd werracle

# Run the sealed test suite
python tests/run_1000_sealed_battery.py
```
*Expected Output:*
```text
[PASS] 1000/1000 tests passed in 213 ms. Bitwise parity: 100.0%.
Sealed Hash: e287d010efee159d6ea3f307509a3e1e306f8a919867de9d2491549240d5fd5e
```

---

### Tutorial 2: Test Flash-Loan Defense in Python
Simulate an attacker taking a 5,000 ETH flash-loan against a 10,000 ETH pool:

```bash
python sim/defi_flashloan_sim.py
```
Observe how the `DeFiFlashLoanGate` automatically flips the decision from `ALLOWED` to `DENIED` with reason `REVERT_FLASH_LOAN_ATTACK`.

---

### Tutorial 3: Interactive EVM Simulator in Browser
No installation required!  
Open `index.html` locally in your web browser or visit the live GitHub Pages portal:
🔗 **[https://pcworm.github.io/werracle/](https://pcworm.github.io/werracle/)**

1. Move the **Borrow Amount** and **Slippage** sliders to see real-time EVM gate evaluation.
2. Inspect the **32-Byte Slot Decomposition** to see how coordinates, zoom, and thresholds are packed into a single EVM storage word.
3. Toggle between **English** and **Türkçe** for multilingual learning.

---

## 🤝 4. Student Challenges & Ideas for Contribution

Looking to make an open-source contribution for your GitHub Global Campus portfolio? Here are 3 great ideas:

* **Challenge A: Arbitrum Stylus (Rust) Port:**  
  Port `contracts/libraries/WerrMath.sol` into Rust for Arbitrum Stylus deployment to achieve $< 5,000$ gas.
* **Challenge B: Cross-Chain Bridge Monitor:**  
  Write a contract hook that validates Merkle root transitions across L1 $\leftrightarrow$ L2 rollups using Werracle continuous scoring.
* **Challenge C: Uniswap v4 Hook Extension:**  
  Extend [`contracts/hooks/WerracleFeeHook.sol`](contracts/hooks/WerracleFeeHook.sol) to incorporate historical volatility TWAP (Time-Weighted Average Price).

Check out our [Good First Issues](https://github.com/pCwOrM/werracle/issues) to get started!

---

## 📖 5. Resources & Contacts

* **Architecture Deep Dive:** [docs/ONE_PAGER.md](docs/ONE_PAGER.md)
* **Grant Proposal & Roadmap:** [docs/GRANT_PROPOSAL.md](docs/GRANT_PROPOSAL.md)
* **Web3 Ecosystem Playbook:** [docs/WEB3_GRANT_AND_ANNOUNCEMENT_PLAYBOOK.md](docs/WEB3_GRANT_AND_ANNOUNCEMENT_PLAYBOOK.md)
* **Official AI Co-Developer Contact:** `ask@answerr.com`
* **Lead Researcher:** `pcworm@pcworm.net` | Corporate: `vdagli@itouch.com.tr`
