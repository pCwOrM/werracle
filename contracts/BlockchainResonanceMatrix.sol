// SPDX-License-Identifier: BSL-1.1
pragma solidity ^0.8.20;

library BlockchainResonanceMatrix {
    struct TokenResonance {
        int64 deltaCx;       // Q16.16
        int64 deltaCy;       // Q16.16
        uint16 severityBps;  // [0 .. 10000]
        uint8 harmonic;      // 3, 6, or 9
        uint8 pillarId;      // 0..4
    }

    function getResonance(uint8 id) internal pure returns (TokenResonance memory r) {
        if (id == 0) return TokenResonance(1901, 0, 4500, 3, 0); // LIQUIDITY_IMBALANCE
        if (id == 1) return TokenResonance(2071, 328, 6000, 6, 0); // TICK_VELOCITY_SPIKE
        if (id == 2) return TokenResonance(2119, 689, 7000, 6, 0); // SLIPPAGE_BREACH
        if (id == 3) return TokenResonance(2161, 1101, 8500, 9, 0); // RESERVE_EXHAUSTION
        if (id == 4) return TokenResonance(1644, 1194, 5500, 6, 0); // LVR_LEAKAGE
        if (id == 5) return TokenResonance(1390, 1390, 5000, 3, 0); // STALE_POOL_PRICE
        if (id == 6) return TokenResonance(1348, 1856, 7500, 9, 0); // DEPTH_SHOCK
        if (id == 7) return TokenResonance(744, 1460, 2500, 3, 0); // RANGE_ORDER_CROSS
        if (id == 8) return TokenResonance(770, 2368, 9000, 9, 1); // FLASHLOAN_BURST
        if (id == 9) return TokenResonance(369, 2330, 8000, 9, 1); // SANDWICH_FRONTRUN
        if (id == 10) return TokenResonance(0, 2163, 6500, 6, 1); // MEMPOOL_SNIPE
        if (id == 11) return TokenResonance(-287, 1812, 4000, 3, 1); // BACKRUN_ARBITRAGE
        if (id == 12) return TokenResonance(-790, 2431, 9500, 9, 1); // REENTRANCY_PROBE
        if (id == 13) return TokenResonance(-952, 1869, 6000, 6, 1); // JIT_LIQUIDITY_DRAIN
        if (id == 14) return TokenResonance(-1448, 1994, 8800, 9, 1); // UNCOLLATERALIZED_SPEC
        if (id == 15) return TokenResonance(-1779, 1779, 9200, 9, 1); // ORACLE_MANIPULATION
        if (id == 16) return TokenResonance(-1962, 1425, 8500, 9, 2); // UNDERCOLLATERALIZED_LOAN
        if (id == 17) return TokenResonance(-2102, 1071, 8000, 9, 2); // HEALTH_FACTOR_BREACH
        if (id == 18) return TokenResonance(-2368, 770, 9000, 9, 2); // LIQUIDATION_CASCADE
        if (id == 19) return TokenResonance(-2266, 359, 7500, 6, 2); // ORACLE_DIVERGENCE
        if (id == 20) return TokenResonance(-2425, 0, 8500, 9, 2); // BAD_DEBT_ACCUMULATION
        if (id == 21) return TokenResonance(-1942, -308, 5000, 3, 2); // TWAP_SPOT_DRIFT
        if (id == 22) return TokenResonance(-1745, -567, 4000, 3, 2); // COLLATERAL_HAIRCUT
        if (id == 23) return TokenResonance(-1226, -625, 500, 3, 2); // SOLVENCY_HEALTHY
        if (id == 24) return TokenResonance(-2100, -1525, 9800, 9, 3); // SANCTIONED_MIXER
        if (id == 25) return TokenResonance(-1854, -1854, 10000, 9, 3); // OFAC_SDN_CLUSTER
        if (id == 26) return TokenResonance(-1233, -1697, 6000, 6, 3); // SYBIL_SWARM
        if (id == 27) return TokenResonance(-922, -1810, 5500, 6, 3); // RAPID_MICRO_CHURN
        if (id == 28) return TokenResonance(-737, -2269, 8200, 9, 3); // ILLICIT_HOP
        if (id == 29) return TokenResonance(-365, -2304, 7800, 6, 3); // MIXER_TAINT_FLOW
        if (id == 30) return TokenResonance(0, -1901, 4500, 3, 3); // FRESH_STEALTH_WALLET
        if (id == 31) return TokenResonance(209, -1320, 200, 3, 3); // VERIFIED_CLEAN_RETAIL
        if (id == 32) return TokenResonance(790, -2431, 9500, 9, 4); // CIRCUIT_BREAKER_TRIP
        if (id == 33) return TokenResonance(1178, -2312, 9800, 9, 4); // EMERGENCY_PAUSE
        if (id == 34) return TokenResonance(1533, -2110, 9900, 9, 4); // TIMELOCK_BYPASS
        if (id == 35) return TokenResonance(1779, -1779, 9200, 9, 4); // UNAUTHORIZED_HOOK
        if (id == 36) return TokenResonance(1591, -1156, 5000, 3, 4); // REBALANCING_VETO
        if (id == 37) return TokenResonance(1927, -982, 6500, 6, 4); // FEE_GOVERNOR_OVERRIDE
        if (id == 38) return TokenResonance(1371, -446, 1000, 3, 4); // PARAMETER_UPDATE_SAFE
        if (id == 39) return TokenResonance(1359, -215, 500, 3, 4); // NORMAL_TRANSACTION_FLOW
        return TokenResonance(0, 0, 500, 3, 4); // Default: NORMAL_TRANSACTION_FLOW
    }
}
