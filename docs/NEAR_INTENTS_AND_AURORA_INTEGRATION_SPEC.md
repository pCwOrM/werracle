# 📜 Werracle on NEAR: Intra-Block Reflex Oracles for Chain Signatures & Aurora EVM
**Technical Specification & Architecture Dossier for NEAR Hackathon 2026**  
*Tracks: Unstoppable DeFi (`01 / DFI`), AI Security & Defense (`02 / SEC`), Agent Economy (`03 / AGT`) &bull; Lead Builder: Volkan Dağlı (`pcworm.near`)*  
*Associated Research: arXiv:2609.30719, Elsevier SSRN: 7626279, CERN Zenodo: 10.5281/zenodo.22942598*

---

## 1. Abstract & Problem Formulation

NEAR Protocol's Chain Abstraction paradigm—anchored by **NEAR Intents** and **Chain Signatures**—allows single-account cross-chain transaction routing. While this radically simplifies user experience, it creates an acute cross-chain security hazard: **Asymmetric Latency Arbitrage & Toxic Intent Exploitation.**

When an intent to swap, bridge, or liquidate across chains is executed, multi-party computation (MPC) signers produce a Chain Signature for the target network (Ethereum, Base, Arbitrum, Solana). However:
1. **Solver Front-Running:** Malicious solvers or predatory MEV searchers can manipulate target pool liquidity inside the latency gap between intent broadcast and chain inclusion.
2. **Flash-Loan Infiltration:** Uncollateralized flash-loan drains occur atomically inside a single block. Traditional on-chain neural networks cannot detect them due to EVM memory limits (costing millions in gas).
3. **ZK-ML Failure:** Zero-Knowledge Machine Learning (ZK-ML) offloads compute off-chain but requires **10 to 300 seconds** of SNARK proving latency, making it impossible to stop intra-block attacks.

---

## 2. The Werracle Architectural Solution

Werracle introduces a zero-storage, procedural boundary derivation engine fitting inside a **single 32-byte storage slot (`bytes32`)**:

```
[Target Token Pair Signals] ──> [24-Byte Coordinate Seed Θ = (cx, cy, zoom)]
                                              │
                                              ▼
                             [Werracle Procedural Reflex Kernel]
                                   z_{n+1} = z_n^2 + c
                                Q16.16 Fixed-Point Arithmetic
                                              │
                                              ▼
                         [Boolean Noul Reflex: 1 = PASS | 0 = VETO]
                                 (~21,438 gas, < 1ms)
```

### Key Integration Points on NEAR:
1. **Aurora (Ethereum on NEAR, Chain ID `1313161555`):**
   * Werracle's Solidity bytecode runs natively on Aurora (`https://testnet.aurora.dev`), utilizing NEAR's 1-second consensus finality and ultra-low transaction fees (< $0.0001).
   * **Deployed Contracts on Aurora Testnet:**
     * `WerracleTripodZMod9.sol` (v2.0 Flagship): `0x1d7Ae9E1dDDA805539d9e225425804Ef8B9caBaF`
     * `Werracle.sol` (v1.0 Canonical): `0x4085673F1e45bf26682CA704b2d09C03d1212cd4`
2. **NEAR Intents (`intents.near` / 1Click API) & Chain Signatures (`v1.signer`) Pre-Sign Filter:**
   * Solvers and autonomous agents audit candidate 1Click swap quotes (`https://1click.chaindefuser.com/v0`) and execution parameters against `WerracleTripodZMod9.sol` (`previewDecision` / `decideNoul`) in `< 15 µs` before requesting an MPC signature from `v1.signer`.
   * If `noul == 0` (`VETO_MPC_SIGN`), the Chain Signature is suppressed before broadcast, preventing funds from ever leaving the user's account into a toxic pool.

---

## 3. Mathematical & Algorithmic Mechanics

### 3.1 Q16.16 Fixed-Point Parameter Derivation
All escape calculations are computed without floating-point emulation using Q16.16 signed integer arithmetic:
$$\text{Fixed}(x) = \lfloor x \times 2^{16} \rfloor$$

Multiplication with 16-bit shift:
$$a \otimes b = \frac{a \times b}{2^{16}}$$

### 3.2 Formal Lean 4 Certification
The underlying $Z/9Z$ ideal decomposition, dynamic boundary invariants, and non-constant sensitivity are formally verified in **Lean 4 (`v4.34.1`)**:
* **40 Theorems, 0 Sorry, 0 Axioms**
* Certificate: [`docs/WERRACLE_LEAN4_FORMAL_VERIFICATION_CERTIFICATE.md`](WERRACLE_LEAN4_FORMAL_VERIFICATION_CERTIFICATE.md)
* Sealed Test Suite: 1,000 deterministically sealed test cases with 100.0% pass rate.

---

## 4. Verification & Reproducibility

Judges and builders can verify the entire pipeline locally and on-chain:

```bash
# 1. Run NEAR Intent Guard + Live Aurora Bit-Exact Parity + 1Click API Quote Audit
python3 near/werracle_near_intent_guard.py
# Or air-gapped offline / JSON agent mode:
python3 near/werracle_near_intent_guard.py --offline --json

# 2. Query live Aurora Testnet contracts (Chain ID 1313161555)
cast call 0x1d7Ae9E1dDDA805539d9e225425804Ef8B9caBaF "previewDecision(bytes32,int64)(bool,uint16)" \
  0x0000000000000000000000000000000000000000000000000000000000000000 0 \
  --rpc-url https://testnet.aurora.dev
cast call 0x4085673F1e45bf26682CA704b2d09C03d1212cd4 "owner()(address)" \
  --rpc-url https://testnet.aurora.dev

# 3. Run Python & Foundry test suites + inspect Lean 4 formal proofs (0 sorry)
python3 -m pytest -q
forge test
cat formal_proofs/CERTIFICATE.md
```

---

## 5. Summary Matrix

| Metric | Traditional On-Chain AI | ZK-ML Provers | Werracle on Aurora / NEAR |
| :--- | :--- | :--- | :--- |
| **Storage Cost** | Millions of Gas ($SSTORE$) | Off-Chain Prover | **1 Slot (`bytes32`) / 2,100 Gas** |
| **Inference Cost** | > 10,000,000 Gas | 250,000 – 500,000 Gas | **~21,438 Gas (< $0.0001)** |
| **Reaction Latency** | Intractable | 10 – 300 Seconds | **< 1 Millisecond (Intra-Block)** |
| **MEV / Flash-Loan Defense** | Ineffective | Fails (Too Slow) | **Atomic Intra-Block Circuit Breaker** |
| **NEAR Chain Signatures** | Incompatible | Impractical | **Native Pre-Signing Reflex Guard** |
