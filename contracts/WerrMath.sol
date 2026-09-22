// SPDX-License-Identifier: BSL-1.1
pragma solidity ^0.8.20;

/**
 * @title WerrMath
 * @notice Fixed-Point Q16.16 Math Library for Werracle On-Chain AI Oracle.
 * @dev 1.0 is represented as 2^16 = 65536.
 *      Provides deterministic quadratic escape iterations and bounded sigmoid approximations.
 */
library WerrMath {
    int64 internal constant ONE = 1 << 16;        // 65536
    int64 internal constant HALF = ONE >> 1;      // 32768
    int64 internal constant FOUR = ONE << 2;      // 262144
    int64 internal constant ESCAPE_RADIUS_SQ = FOUR; // 4.0 in Q16.16

    /**
     * @notice Multiplies two Q16.16 fixed-point numbers.
     */
    function mulFP(int64 a, int64 b) internal pure returns (int64) {
        return int64((int128(a) * int128(b)) >> 16);
    }

    /**
     * @notice Divides two Q16.16 fixed-point numbers.
     */
    function divFP(int64 a, int64 b) internal pure returns (int64) {
        require(b != 0, "WerrMath: Zero Division");
        return int64((int128(a) << 16) / int128(b));
    }

    /**
     * @notice Computes quadratic escape iteration for a single point (cx, cy).
     *         Formula: zn+1 = zn^2 + c
     * @param cx Real coordinate in Q16.16
     * @param cy Imaginary coordinate in Q16.16
     * @param maxIter Maximum iteration threshold (e.g. 12)
     * @return iters Escape step count (0 to maxIter)
     */
    function iterateEscape(int64 cx, int64 cy, uint8 maxIter) internal pure returns (uint8 iters) {
        int64 zx = 0;
        int64 zy = 0;

        for (uint8 i = 0; i < maxIter; i++) {
            int64 zx2 = int64((int128(zx) * int128(zx)) >> 16);
            int64 zy2 = int64((int128(zy) * int128(zy)) >> 16);

            // Escape condition: |z|^2 = zx^2 + zy^2 > 4.0
            if (zx2 + zy2 > ESCAPE_RADIUS_SQ) {
                return i;
            }

            // new_zx = zx^2 - zy^2 + cx
            // new_zy = 2 * zx * zy + cy
            int64 newZx = zx2 - zy2 + cx;
            int64 newZy = int64((int128(zx) * int128(zy)) >> 15) + cy; // (2*zx*zy)>>16 == (zx*zy)>>15
            zx = newZx;
            zy = newZy;
        }

        return maxIter;
    }

    /**
     * @notice Fast Piecewise Linear Sigmoid approximation in Q16.16.
     *         Maps logit in [-4.0, +4.0] to probability in basis points [0, 10000].
     * @param x Logit signal in Q16.16
     * @return bps Probability in Basis Points [100, 9900] (1.00% to 99.00%)
     */
    function sigmoidBps(int64 x) internal pure returns (uint16 bps) {
        int64 four = FOUR;
        if (x <= -four) return 180;   // ~1.8%
        if (x >= four) return 9820;   // ~98.2%

        // Linear slope approximation: P(x) ~= 0.5 + 0.12 * x
        // 0.12 in Q16.16 ~= 7864
        int64 p = HALF + mulFP(x, 7864);
        int64 res = (p * 10000) >> 16;

        if (res < 100) return 100;
        if (res > 9900) return 9900;
        return uint16(uint64(res));
    }
}
