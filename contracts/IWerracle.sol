// SPDX-License-Identifier: BSL-1.1
pragma solidity ^0.8.20;

/**
 * @title IWerracle
 * @notice Interface for Werracle Zero-Storage On-Chain AI Oracle.
 */
interface IWerracle {
    // Decision Event
    event DecisionEvaluated(
        address indexed caller,
        bytes32 indexed stateHash,
        uint8 mode, // 0: Noul, 1: Choice, 2: Score
        uint256 feePaid
    );

    // Fee Configuration Event
    event ProtocolFeeUpdated(uint256 oldFee, uint256 newFee, address newRecipient);

    /**
     * @notice Noul Boolean Reflex Gate.
     * @param stateHash Cryptographic hash representing client program state
     * @param riskScoreFP Contextual risk signal in Q16.16 (Negative=Low Risk, Positive=High Risk)
     * @return allowed True if approved, False if denied/blocked
     * @return confidenceBps Confidence level in basis points [0..10000]
     */
    function decideNoul(
        bytes32 stateHash,
        int64 riskScoreFP
    ) external payable returns (bool allowed, uint16 confidenceBps);

    /**
     * @notice Choice Route Selector across 4 fractal quadrants.
     * @param stateHash Cryptographic hash of current operation
     * @param numChoices Total number of available routing choices
     * @param contextBiasFP Additional contextual bias in Q16.16
     * @return chosenIndex Best route index [0 .. numChoices - 1]
     */
    function decideChoice(
        bytes32 stateHash,
        uint8 numChoices,
        int64 contextBiasFP
    ) external payable returns (uint8 chosenIndex);

    /**
     * @notice Continuous Severity / Priority Score.
     * @param stateHash Cryptographic hash of operation
     * @param riskScoreFP Risk level in Q16.16
     * @param maxScore Maximum integer scale (e.g. 3)
     * @return evaluatedScore Evaluated level [0 .. maxScore]
     */
    function decideScore(
        bytes32 stateHash,
        int64 riskScoreFP,
        uint256 maxScore
    ) external payable returns (uint256 evaluatedScore);

    /**
     * @notice Returns the current protocol fee required per decision call.
     */
    function protocolFee() external view returns (uint256);

    /**
     * @notice Returns the fee recipient address.
     */
    function feeRecipient() external view returns (address);
}
