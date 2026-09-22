// SPDX-License-Identifier: BSL-1.1
pragma solidity ^0.8.20;

import "../IWerracle.sol";

/**
 * @title WerracleFeeHook
 * @notice Uniswap v4 Dynamic Fee Hook powered by Werracle On-Chain AI Oracle.
 * @dev Evaluates intra-block pool volatility and volume imbalances in <1ms to dynamically
 *      set swap fees (0.05% to 0.50%), sharing a slice of hook fees with the Werracle protocol.
 */
contract WerracleFeeHook {
    IWerracle public immutable oracle;
    address public immutable hookOwner;

    // Minimum and Maximum Dynamic Fee in pips (1 pip = 0.0001%)
    // 500 pips = 0.05%, 5000 pips = 0.50%
    uint24 public constant MIN_FEE = 500;
    uint24 public constant MAX_FEE = 5000;

    event DynamicFeeCalculated(bytes32 indexed poolId, uint24 dynamicFeePips);

    constructor(address oracleAddress) {
        require(oracleAddress != address(0), "Zero Oracle");
        oracle = IWerracle(oracleAddress);
        hookOwner = msg.sender;
    }

    /**
     * @notice Simulates Uniswap v4 beforeSwap hook entry point.
     * @param poolId Identifier of the liquidity pool
     * @param imbalanceSignalFP Imbalance/volatility ratio in Q16.16
     * @return dynamicFeePips Fee in pips to be charged for this swap
     */
    function calculateDynamicFee(
        bytes32 poolId,
        int64 imbalanceSignalFP
    ) external payable returns (uint24 dynamicFeePips) {
        // Forward protocol fee to Werracle Oracle
        uint256 reqFee = oracle.protocolFee();
        require(msg.value >= reqFee, "Insufficient Oracle Fee");

        // Query Oracle severity score [0 .. 3]
        uint256 severityScore = oracle.decideScore{value: reqFee}(
            poolId,
            imbalanceSignalFP,
            3
        );

        // Refund any remaining excess
        if (msg.value > reqFee) {
            payable(msg.sender).transfer(msg.value - reqFee);
        }

        // Map severity [0, 1, 2, 3] -> [MIN_FEE .. MAX_FEE]
        // 0 -> 500 pips (0.05% - Calm market)
        // 1 -> 1500 pips (0.15% - Normal)
        // 2 -> 3000 pips (0.30% - Elevated Volatility)
        // 3 -> 5000 pips (0.50% - High Volatility / Flash-loan shock)
        if (severityScore == 0) {
            dynamicFeePips = 500;
        } else if (severityScore == 1) {
            dynamicFeePips = 1500;
        } else if (severityScore == 2) {
            dynamicFeePips = 3000;
        } else {
            dynamicFeePips = 5000;
        }

        emit DynamicFeeCalculated(poolId, dynamicFeePips);
    }
}
