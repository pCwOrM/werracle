// SPDX-License-Identifier: BSL-1.1
pragma solidity ^0.8.20;

import "../contracts/Werracle.sol";
import "../contracts/WerrMath.sol";
import "../contracts/hooks/WerracleFeeHook.sol";

/**
 * @title WerracleTest
 * @notice Complete on-chain unit test suite and gas measurement for Werracle.
 */
contract WerracleTest {
    Werracle public oracle;
    WerracleFeeHook public hook;
    address public owner;
    address public feeRecipient;

    uint256 public constant PROTOCOL_FEE = 0.00005 ether;

    event Log(string message, uint256 val);

    constructor() {
        owner = address(this);
        feeRecipient = address(0x1111111111111111111111111111111111111111);
        oracle = new Werracle(feeRecipient, PROTOCOL_FEE);
        hook = new WerracleFeeHook(address(oracle));
    }

    // Allow this contract to receive excess refunds and fees
    receive() external payable {}

    function setUp() public {
        // Already initialized in constructor
    }

    function testInitialSeed() public view {
        (
            int64 cx,
            int64 cy,
            uint64 zoom,
            uint32 nonce,
            uint16 threshold,
            uint8 defaultMode,
            uint8 activeFlag
        ) = oracle.seed();

        require(cx == -48735, "Wrong initial cx");
        require(cy == 8639, "Wrong initial cy");
        require(zoom == 3276800, "Wrong initial zoom");
        require(threshold == 5000, "Wrong initial threshold");
        require(activeFlag == 1, "Should be active");
    }

    function testDecideNoulAdminAllowed() public {
        bytes32 stateHash = keccak256("state:admin");
        int64 riskAdminFP = int64(-15 * WerrMath.ONE / 10); // -1.5 in Q16.16

        (bool allowed, uint16 confidenceBps) = oracle.decideNoul{value: PROTOCOL_FEE}(
            stateHash,
            riskAdminFP
        );

        require(allowed == true, "Admin should be ALLOWED");
        require(confidenceBps > 5000, "Confidence should exceed 50%");
    }

    function testDecideNoulAttackerDenied() public {
        bytes32 stateHash = keccak256("state:attacker");
        int64 riskAttackerFP = int64(25 * WerrMath.ONE / 10); // +2.5 in Q16.16

        (bool allowed, uint16 confidenceBps) = oracle.decideNoul{value: PROTOCOL_FEE}(
            stateHash,
            riskAttackerFP
        );

        require(allowed == false, "Attacker should be DENIED");
        require(confidenceBps > 5000, "Confidence should exceed 50%");
    }

    function testDecideChoiceRouting() public {
        bytes32 stateHash = keccak256("state:routing");
        uint8 chosenIndex = oracle.decideChoice{value: PROTOCOL_FEE}(
            stateHash,
            4,
            0 // zero contextual bias
        );

        require(chosenIndex < 4, "Choice index out of range");
    }

    function testDecideScoreSeverity() public {
        bytes32 stateHash = keccak256("state:severity");
        int64 riskAttackerFP = int64(25 * WerrMath.ONE / 10); // +2.5 in Q16.16

        uint256 score = oracle.decideScore{value: PROTOCOL_FEE}(
            stateHash,
            riskAttackerFP,
            3 // max score
        );

        require(score >= 2, "Attacker should trigger high severity score");
    }

    function testProtocolFeeDistribution() public {
        uint256 recipientBalBefore = feeRecipient.balance;
        bytes32 stateHash = keccak256("state:fee_test");

        // Call with exact fee
        oracle.decideNoul{value: PROTOCOL_FEE}(
            stateHash,
            0
        );

        uint256 recipientBalAfter = feeRecipient.balance;
        require(
            recipientBalAfter - recipientBalBefore == PROTOCOL_FEE,
            "Fee not credited to recipient"
        );
    }

    function testDynamicFeeHook() public {
        bytes32 poolId = keccak256("pool:ETH-USDC");
        // High volatility shock (+2.5 in Q16.16)
        int64 shockFP = int64(25 * WerrMath.ONE / 10);

        uint24 dynamicFee = hook.calculateDynamicFee{value: PROTOCOL_FEE}(
            poolId,
            shockFP
        );

        require(dynamicFee >= 3000, "Shock should trigger elevated dynamic fee");
    }
}
