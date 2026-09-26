// SPDX-License-Identifier: BSL-1.1
pragma solidity ^0.8.20;

import "../IWerracle.sol";

/**
 * @title PancakeWerracleHook
 * @notice PancakeSwap v4 Dynamic Fee & Anti-LVR Hook powered by Werracle On-Chain AI Oracle.
 * @dev Specially adapted for PancakeSwap v4 (BNB Chain, Ethereum, Arbitrum, Base).
 *      Intercepts `beforeSwap` inside PancakeSwap v4's CLPoolManager / BinPoolManager pipelines,
 *      dynamically scaling liquidity provider fees between 500 pips (0.05%) and 5,000 pips (0.50%)
 *      in <1ms with zero persistent storage reads (0 SLOAD) during the forward pass.
 *
 * Designed for PancakeSwap v4 Developer & Ecosystem Grants Program.
 */
contract PancakeWerracleHook {
    IWerracle public immutable oracle;
    address public immutable hookOwner;
    address public immutable vaultManager;

    // Minimum and Maximum Dynamic Fee in pips (1 pip = 0.0001% = 1/1,000,000)
    // In PancakeSwap v4 convention: 500 pips = 0.05%, 5000 pips = 0.50%
    uint24 public constant MIN_FEE = 500;
    uint24 public constant MAX_FEE = 5000;

    // PancakeSwap v4 Hook Permission Flags
    // beforeSwap = true, afterSwap = false, beforeInitialize = false
    uint160 public constant PANCAKE_HOOK_PERMISSIONS = 0x0080; // BEFORE_SWAP_FLAG

    event PancakeDynamicFeeCalculated(
        bytes32 indexed poolId,
        uint24 dynamicFeePips,
        uint256 severityTier
    );
    event HookOwnerUpdated(address indexed oldOwner, address indexed newOwner);

    modifier onlyOwner() {
        require(msg.sender == hookOwner, "Not Hook Owner");
        _;
    }

    constructor(address oracleAddress, address _vaultManager) {
        require(oracleAddress != address(0), "Zero Oracle");
        oracle = IWerracle(oracleAddress);
        vaultManager = _vaultManager;
        hookOwner = msg.sender;
    }

    /**
     * @notice PancakeSwap v4 Hook Entrypoint for Dynamic Swap Fee calculation.
     * @param poolId Identifier of the PancakeSwap v4 liquidity pool (PoolId)
     * @param imbalanceSignalFP Imbalance/volatility ratio in Q16.16 fixed-point
     * @return dynamicFeePips Fee in pips applied dynamically to this swap
     */
    function calculatePancakeDynamicFee(
        bytes32 poolId,
        int64 imbalanceSignalFP
    ) external payable returns (uint24 dynamicFeePips) {
        // Forward protocol query fee if required
        uint256 reqFee = oracle.protocolFee();
        require(msg.value >= reqFee, "Insufficient Protocol Fee");

        // Query Oracle severity score [0 .. 3] via ZMod 9 procedural resonance
        uint256 severityScore = oracle.decideScore{value: reqFee}(
            poolId,
            imbalanceSignalFP,
            3
        );

        // Refund any excess native tokens (e.g. BNB or ETH)
        if (msg.value > reqFee) {
            payable(msg.sender).transfer(msg.value - reqFee);
        }

        // Map severity [0, 1, 2, 3] -> [MIN_FEE .. MAX_FEE]
        // 0 -> 500 pips  (0.05% - Calm retail volume, 0 perturbation)
        // 1 -> 1500 pips (0.15% - Normal intra-block variance)
        // 2 -> 3000 pips (0.30% - Elevated cross-venue latency arb)
        // 3 -> 5000 pips (0.50% - Toxic flashloan shock / MEV sandwich)
        if (severityScore == 0) {
            dynamicFeePips = 500;
        } else if (severityScore == 1) {
            dynamicFeePips = 1500;
        } else if (severityScore == 2) {
            dynamicFeePips = 3000;
        } else {
            dynamicFeePips = 5000;
        }

        emit PancakeDynamicFeeCalculated(poolId, dynamicFeePips, severityScore);
    }

    /**
     * @notice Native PancakeSwap v4 beforeSwap hook compliance interface.
     * @dev Called by PancakeSwap v4 PoolManager prior to swap execution.
     * @param sender The address initiating the swap
     * @param poolId The unique hash of the PancakeSwap v4 pool
     * @param zeroForOne Swap direction flag (token0 -> token1 or token1 -> token0)
     * @param amountSpecified Amount of tokens requested for the swap
     * @param hookData Encoded market signal data passed by the trader or router
     * @return selector Returns bytes4(keccak256("beforeSwap(...)")) selector
     * @return feeOverride The dynamic fee override in pips to protect LP yield
     */
    function beforeSwap(
        address sender,
        bytes32 poolId,
        bool zeroForOne,
        int256 amountSpecified,
        bytes calldata hookData
    ) external returns (bytes4 selector, uint24 feeOverride) {
        // Decode telemetry signal if provided in hookData, otherwise use amount magnitude
        int64 signalFP;
        if (hookData.length >= 8) {
            signalFP = abi.decode(hookData, (int64));
        } else {
            // Normalize transaction impact to Q16.16 (abs magnitude)
            int256 rawMagnitude = amountSpecified < 0 ? -amountSpecified : amountSpecified;
            signalFP = int64(int256((rawMagnitude % 1e18) * 65536 / 1e18));
        }

        // Forward protocol query fee if configured
        uint256 reqFee = oracle.protocolFee();
        uint256 severityScore;
        if (reqFee > 0 && address(this).balance >= reqFee) {
            severityScore = oracle.decideChoice{value: reqFee}(poolId, 4, signalFP);
        } else {
            severityScore = oracle.decideChoice(poolId, 4, signalFP);
        }

        if (severityScore == 0) {
            feeOverride = MIN_FEE;
        } else if (severityScore == 1) {
            feeOverride = 1500;
        } else if (severityScore == 2) {
            feeOverride = 3000;
        } else {
            feeOverride = MAX_FEE;
        }

        // Standard PancakeSwap v4 selector: bytes4(keccak256("beforeSwap(address,bytes32,bool,int256,bytes)"))
        selector = this.beforeSwap.selector;
    }

    /**
     * @notice Emergency withdrawal for any accumulated fee revenue.
     */
    function withdrawFees(address to) external onlyOwner {
        require(to != address(0), "Invalid recipient");
        payable(to).transfer(address(this).balance);
    }

    receive() external payable {}
}
