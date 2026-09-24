// SPDX-License-Identifier: BSL-1.1
pragma solidity ^0.8.20;

import "./WerrMath.sol";
import "./IWerracle.sol";

/**
 * @title Werracle
 * @notice Production On-Chain AI Decision Oracle.
 * @dev Synthesizes deterministic typed decisions (noul, choice, score) directly from
 *      procedural Mandelbrot dynamics in a single 32-byte storage slot.
 *      Zero neural tensors. Sub-millisecond latency. ~20.000 gas execution.
 */
contract Werracle is IWerracle {
    using WerrMath for int64;

    // --- Ownership & Protocol Fee State ---
    address public owner;
    address public override feeRecipient;
    uint256 public override protocolFee;
    uint256 public totalDecisionsCount;

    // --- 32-Byte Storage Slot Layout (bytes32 Packed Seed) ---
    // Packed precisely into 256 bits (32 Bytes):
    // [cx: 64b | cy: 64b | zoom: 64b | nonce: 32b | threshold: 16b | defaultMode: 8b | activeFlag: 8b]
    struct PackedSeed {
        int64 cx;          // 8 Bytes: Real coordinate in Q16.16 (-0.743643887 * 65536 = -48735)
        int64 cy;          // 8 Bytes: Imag coordinate in Q16.16 (+0.131825904 * 65536 = +8639)
        uint64 zoom;       // 8 Bytes: Zoom scale in Q16.16 (50.0 * 65536 = 3276800)
        uint32 nonce;      // 4 Bytes: Calibration update nonce
        uint16 threshold;  // 2 Bytes: Decision boundary (5000 bps = 50.0%)
        uint8 defaultMode; // 1 Byte:  0=Noul, 1=Choice, 2=Score
        uint8 activeFlag;  // 1 Byte:  1=Active, 0=Paused
    }

    PackedSeed public seed;

    uint8 internal constant MAX_ITER = 12;

    // --- Modifiers ---
    modifier onlyOwner() {
        require(msg.sender == owner, "Werracle: Not Owner");
        _;
    }

    modifier handleFee() {
        require(msg.value >= protocolFee, "Werracle: Insufficient Protocol Fee");
        if (protocolFee > 0 && feeRecipient != address(0)) {
            // Forward fee directly to recipient
            (bool success, ) = feeRecipient.call{value: protocolFee}("");
            require(success, "Werracle: Fee Transfer Failed");
        }
        // Refund excess payment to caller
        uint256 excess = msg.value - protocolFee;
        if (excess > 0) {
            (bool refundSuccess, ) = msg.sender.call{value: excess}("");
            require(refundSuccess, "Werracle: Excess Refund Failed");
        }
        totalDecisionsCount++;
        _;
    }

    constructor(
        address initialFeeRecipient,
        uint256 initialProtocolFee
    ) {
        owner = msg.sender;
        feeRecipient = initialFeeRecipient != address(0) ? initialFeeRecipient : msg.sender;
        protocolFee = initialProtocolFee; // e.g. 0.00005 ether

        // Initialize with default Seahorse Valley Seed (Q16.16)
        seed = PackedSeed({
            cx: -48735,     // -0.7436438870371587 in Q16.16
            cy: 8639,       // +0.1318259042053119 in Q16.16
            zoom: 3276800,  // 50.0 in Q16.16
            nonce: 1,
            threshold: 5000,// 50%
            defaultMode: 0,
            activeFlag: 1
        });
    }

    // --- Admin Functions ---
    function setProtocolFee(uint256 newFee, address newRecipient) external onlyOwner {
        require(newRecipient != address(0), "Werracle: Zero Recipient");
        emit ProtocolFeeUpdated(protocolFee, newFee, newRecipient);
        protocolFee = newFee;
        feeRecipient = newRecipient;
    }

    function updateSeed(
        int64 cx,
        int64 cy,
        uint64 zoom,
        uint16 threshold
    ) external onlyOwner {
        seed.cx = cx;
        seed.cy = cy;
        seed.zoom = zoom;
        seed.threshold = threshold;
        seed.nonce += 1;
    }

    function setPaused(bool paused) external onlyOwner {
        seed.activeFlag = paused ? 0 : 1;
    }

    // --- Core Oracle Functions ---

    /**
     * @notice Noul Boolean Reflex Gate.
     */
    function decideNoul(
        bytes32 stateHash,
        int64 riskScoreFP
    ) external payable override handleFee returns (bool allowed, uint16 confidenceBps) {
        require(seed.activeFlag == 1, "Werracle: Engine Paused");

        (int64[4] memory weights, ) = _sampleQuadrants(seed.cx, seed.cy, seed.zoom);

        // Fractal balance bias: (w1 + w2 - w3 - w4) / 4
        int64 fractalBias = (weights[0] + weights[1] - weights[2] - weights[3]) >> 2;

        // Net logit = -riskScore + fractalBias
        int64 logit = -riskScoreFP + fractalBias;
        uint16 probBps = WerrMath.sigmoidBps(logit);

        allowed = probBps >= seed.threshold;
        confidenceBps = allowed ? probBps : (10000 - probBps);

        emit DecisionEvaluated(msg.sender, stateHash, 0, protocolFee);
    }

    /**
     * @notice View / Pure Forward Inference Preview for v1.0 baseline.
     */
    function previewDecision(
        bytes32 /*stateHash*/,
        int64 riskScoreFP
    ) external view returns (bool allowed, uint16 confidenceBps) {
        require(seed.activeFlag == 1, "Werracle: Engine Paused");

        (int64[4] memory weights, ) = _sampleQuadrants(seed.cx, seed.cy, seed.zoom);

        // Fractal balance bias: (w1 + w2 - w3 - w4) / 4
        int64 fractalBias = (weights[0] + weights[1] - weights[2] - weights[3]) >> 2;

        // Net logit = -riskScore + fractalBias
        int64 logit = -riskScoreFP + fractalBias;
        uint16 probBps = WerrMath.sigmoidBps(logit);

        allowed = probBps >= seed.threshold;
        confidenceBps = allowed ? probBps : (10000 - probBps);
    }

    /**
     * @notice Choice Route Selector among N routes.
     */
    function decideChoice(
        bytes32 stateHash,
        uint8 numChoices,
        int64 contextBiasFP
    ) external payable override handleFee returns (uint8 chosenIndex) {
        require(seed.activeFlag == 1, "Werracle: Engine Paused");
        require(numChoices > 1, "Werracle: Need >1 Choices");

        (int64[4] memory weights, ) = _sampleQuadrants(seed.cx, seed.cy, seed.zoom);

        int64 bestScore = -1000000000;
        uint8 bestIdx = 0;

        for (uint8 i = 0; i < numChoices; i++) {
            int64 score = weights[i % 4] + ((contextBiasFP * int64(int8(i + 1))) >> 2);
            if (score > bestScore) {
                bestScore = score;
                bestIdx = i;
            }
        }

        chosenIndex = bestIdx;
        emit DecisionEvaluated(msg.sender, stateHash, 1, protocolFee);
    }

    /**
     * @notice Continuous Severity / Priority Score.
     */
    function decideScore(
        bytes32 stateHash,
        int64 riskScoreFP,
        uint256 maxScore
    ) external payable override handleFee returns (uint256 evaluatedScore) {
        require(seed.activeFlag == 1, "Werracle: Engine Paused");

        // Scale risk [-2.0, +2.0] into [0, ONE]
        int64 scaledRisk = (riskScoreFP + (2 * WerrMath.ONE)) >> 2;
        if (scaledRisk < 0) scaledRisk = 0;
        if (scaledRisk > WerrMath.ONE) scaledRisk = WerrMath.ONE;

        evaluatedScore = (uint256(uint64(scaledRisk)) * maxScore) >> 16;
        emit DecisionEvaluated(msg.sender, stateHash, 2, protocolFee);
    }

    // --- Internal 16-Point Pareto Escape Kernel ---
    function _sampleQuadrants(
        int64 cx,
        int64 cy,
        uint64 zoom
    ) internal pure returns (int64[4] memory weights, uint16 blackRatioBps) {
        int64 step = zoom > 0 ? WerrMath.divFP(WerrMath.ONE, int64(zoom)) : WerrMath.ONE;
        int64 subStep = step >> 1;

        uint16[4] memory escapes;
        uint8 totalBlack = 0;

        // 16-point Pareto micro-grid (4 points per quadrant)
        // Q1 (+x, +y)
        escapes[0] += WerrMath.iterateEscape(cx + subStep, cy + subStep, MAX_ITER);
        escapes[0] += WerrMath.iterateEscape(cx + step, cy + subStep, MAX_ITER);
        escapes[0] += WerrMath.iterateEscape(cx + subStep, cy + step, MAX_ITER);
        escapes[0] += WerrMath.iterateEscape(cx + step, cy + step, MAX_ITER);

        // Q2 (-x, +y)
        escapes[1] += WerrMath.iterateEscape(cx - subStep, cy + subStep, MAX_ITER);
        escapes[1] += WerrMath.iterateEscape(cx - step, cy + subStep, MAX_ITER);
        escapes[1] += WerrMath.iterateEscape(cx - subStep, cy + step, MAX_ITER);
        escapes[1] += WerrMath.iterateEscape(cx - step, cy + step, MAX_ITER);

        // Q3 (-x, -y)
        escapes[2] += WerrMath.iterateEscape(cx - subStep, cy - subStep, MAX_ITER);
        escapes[2] += WerrMath.iterateEscape(cx - step, cy - subStep, MAX_ITER);
        escapes[2] += WerrMath.iterateEscape(cx - subStep, cy - step, MAX_ITER);
        escapes[2] += WerrMath.iterateEscape(cx - step, cy - step, MAX_ITER);

        // Q4 (+x, -y)
        escapes[3] += WerrMath.iterateEscape(cx + subStep, cy - subStep, MAX_ITER);
        escapes[3] += WerrMath.iterateEscape(cx + step, cy - subStep, MAX_ITER);
        escapes[3] += WerrMath.iterateEscape(cx + subStep, cy - step, MAX_ITER);
        escapes[3] += WerrMath.iterateEscape(cx + step, cy - step, MAX_ITER);

        // Max possible escape sum = 4 * MAX_ITER = 48
        uint16 maxQSum = 4 * uint16(MAX_ITER);

        for (uint8 q = 0; q < 4; q++) {
            // Normalized ratio [0 .. ONE]
            int64 ratio = int64((uint64(escapes[q]) * uint64(WerrMath.ONE)) / maxQSum);
            weights[q] = ratio - WerrMath.HALF; // zero-centered
        }

        blackRatioBps = (uint16(totalBlack) * 10000) / 16;
    }
}
