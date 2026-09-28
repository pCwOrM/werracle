// SPDX-License-Identifier: BUSL-1.1
pragma solidity ^0.8.20;

import "./WerrMath.sol";

/**
 * @title WerracleLivingCell
 * @author Volkan Dagli (@pCwOrM) — ITouch Systems Research
 * @notice Step 1 of the Sovereign On-Chain Living AI Architecture:
 *         A self-evolving, stateful, single-slot (256-bit / 32-byte) on-chain neural cell.
 * @dev Packs the entire DNA (cx, cy, zoom) + Recurrent Hidden State h_t (rollingStressEMA)
 *      + Epigenetic Fitness + Generation + Z/9Z Phase Residue + Lifecycle State into ONE
 *      single 256-bit EVM storage word (`uint256 livingGenomeSlot`).
 *
 *      Bit Layout of `livingGenomeSlot` (256 bits / 32 bytes):
 *      - Bits   0..63  : int64  cx               (Q16.16 real boundary gene)
 *      - Bits  64..127 : int64  cy               (Q16.16 imag boundary gene)
 *      - Bits 128..191 : uint64 zoom             (Q16.16 horizon scale gene)
 *      - Bits 192..207 : uint16 rollingStressEMA (Recurrent memory h_t in [0..10000] bps)
 *      - Bits 208..223 : uint16 fitnessScore     (Epigenetic survival fitness [0..65535])
 *      - Bits 224..239 : uint16 generation       (Autonomous mutation epoch [0..65535])
 *      - Bits 240..243 : uint4  lastResidueMod9  (Z/9Z GAP-0331 ring residue [0..8])
 *      - Bits 244..247 : uint4  lifecycleState   (0=Hibernation, 1=Homeostasis, 2=HyperImmune, 3=Plasticity)
 *      - Bit  248      : uint1  activeFlag       (1=Alive, 0=Paused)
 *      - Bits 249..251 : uint3  orthoConfigBits  (Bit2=autoGuard4d, Bit1=phaseLock, Bit0=observerHorizon)
 *      - Bits 252..255 : uint4  cd4ToleranceTier (1..15 => catastrophic shock threshold = tier * 800 bps)
 */
contract WerracleLivingCell {
    using WerrMath for int64;

    uint8 public constant STATE_HIBERNATION  = 0; // Wormhole Error-Kernel Sanctuary ({0,3,6})
    uint8 public constant STATE_HOMEOSTASIS  = 1; // Calm awake reflex + recurrent memory
    uint8 public constant STATE_HYPER_IMMUNE = 2; // CD4+ heightened immune alert
    uint8 public constant STATE_PLASTICITY   = 3; // Active epigenetic evolution on dM

    int64 internal constant HORIZON_MIN_R2_FP   = 2621;    // ~0.04 in Q16.16
    int64 internal constant HORIZON_MAX_R2_FP   = 147456;  //  2.25 in Q16.16
    uint64 internal constant HORIZON_MIN_ZOOM   = 262144;  //  4.00 in Q16.16
    uint64 internal constant HORIZON_MAX_ZOOM   = 7864320; // 120.0 in Q16.16

    /// @notice The single 32-byte (256-bit) EVM storage slot holding the cell's DNA and memory
    uint256 public livingGenomeSlot;

    address public immutable guardian;

    struct UnpackedGenome {
        int64 cx;
        int64 cy;
        uint64 zoom;
        uint16 rollingStressEMA;
        uint16 fitnessScore;
        uint16 generation;
        uint8 lastResidueMod9;
        uint8 lifecycleState;
        uint8 activeFlag;
        uint8 orthoConfigBits;
        uint8 cd4ToleranceTier;
    }

    event CellPerceived(
        bytes32 indexed stateHash,
        uint8 lifecycleState,
        uint16 dynamicFeeBps,
        uint16 rollingStressEMA,
        uint16 generation
    );

    event CellEvolvedOnChain(
        uint16 indexed generation,
        int64 newCx,
        int64 newCy,
        uint64 newZoom,
        uint16 fitnessScore,
        bool zincSparkTriggered
    );

    event CellEnteredWormholeHibernation(
        uint16 rollingStressEMA,
        uint8 projectedResidueMod9,
        int64 preservedCx,
        int64 preservedCy
    );

    error CellInactive();
    error InvalidHorizonCoordinate();
    error UnauthorizedGuardian();

    constructor(int64 initCx, int64 initCy, uint64 initZoom) {
        if (!verifyProofOfHorizon(initCx, initCy, initZoom)) {
            revert InvalidHorizonCoordinate();
        }
        guardian = msg.sender;

        UnpackedGenome memory g = UnpackedGenome({
            cx: initCx,
            cy: initCy,
            zoom: initZoom,
            rollingStressEMA: 500, // 5.00% calm genesis stress
            fitnessScore: 1000,    // Genesis fitness
            generation: 1,
            lastResidueMod9: 1,    // Coprime unit genesis
            lifecycleState: STATE_HOMEOSTASIS,
            activeFlag: 1,
            orthoConfigBits: 7,    // (1,1,1) = auto_guard_4d + phase_lock + observer_horizon
            cd4ToleranceTier: 8    // 6400 bps catastrophic hibernation trigger
        });

        livingGenomeSlot = _packGenome(g);
    }

    /**
     * @notice Patent TR 2026/016285 On-Chain `Proof-of-Horizon` (< 450 gas).
     * @dev Verifies that (cx, cy, zoom) lies within the viable Mandelbrot boundary annulus
     *      and does not collapse into the dead cardioid center or trivial exterior.
     */
    function verifyProofOfHorizon(int64 cx, int64 cy, uint64 zoom) public pure returns (bool) {
        if (zoom < HORIZON_MIN_ZOOM || zoom > HORIZON_MAX_ZOOM) {
            return false;
        }
        int64 r2 = WerrMath.mulFP(cx, cx) + WerrMath.mulFP(cy, cy);
        if (r2 < HORIZON_MIN_R2_FP || r2 > HORIZON_MAX_R2_FP) {
            return false;
        }
        int64 dxCenter = cx + 8192; // cx - (-0.125)
        int64 distCenterSq = WerrMath.mulFP(dxCenter, dxCenter) + WerrMath.mulFP(cy, cy);
        if (distCenterSq < 1310) {
            return false;
        }
        return true;
    }

    /**
     * @notice Unpacks the 256-bit `livingGenomeSlot` into a structured `UnpackedGenome`.
     */
    function getGenomeState() external view returns (UnpackedGenome memory) {
        return _unpackGenome(livingGenomeSlot);
    }

    /**
     * @notice Executes a full biological perception, recurrent memory update, Wormhole
     *         Hibernation check, and autonomous epigenetic evolution within 1 storage slot.
     */
    function perceiveAndEvolve(bytes32 stateHash, int64 shockBps)
        external
        returns (
            bool noulAllowed,
            uint16 dynamicFeeBps,
            uint8 lifecycleState,
            uint16 generation,
            uint16 rollingStressEMA
        )
    {
        UnpackedGenome memory g = _unpackGenome(livingGenomeSlot);
        if (g.activeFlag == 0) revert CellInactive();

        uint16 clampedShock = shockBps <= 0 ? 0 : (shockBps >= 10000 ? 10000 : uint16(uint64(shockBps)));
        uint16 cd4CatastrophicBps = uint16(g.cd4ToleranceTier) * 800;

        // Recurrent Memory Modulation: protect against multi-block split/dust attacks
        uint16 effectiveShock = clampedShock;
        if (g.rollingStressEMA > 1800) {
            uint16 boost = (g.rollingStressEMA - 1800) >> 1;
            effectiveShock = clampedShock + boost > 10000 ? 10000 : clampedShock + boost;
        }

        // Evaluate 12-point Sparse Harmonic Tripod over Z/9Z
        (
            uint8 q1,
            uint8 q2,
            uint8 q3,
            uint8 q4,
            uint8 blackCount
        ) = _perceiveTripod(g, stateHash, effectiveShock);

        uint8 totalEscape = q1 + q2 + q3 + q4;
        uint8 zmod9Residue = totalEscape % 9;
        bool isUnit = (zmod9Residue % 3) != 0;

        // Update Recurrent Hidden State h_{t+1} = (3 * h_t + instantStress) >> 2
        uint16 escapeDivBps = uint16(((uint32(108 - totalEscape) * 10000) / 108));
        uint16 instantStress = uint16((uint32(effectiveShock) * 3 + (escapeDivBps >> 2)) >> 2);
        if (instantStress > 10000) instantStress = 10000;

        uint16 newEMA = uint16(((uint32(g.rollingStressEMA) * 3) + instantStress) >> 2);

        // Biological Lifecycle & Wormhole Error-Kernel State Machine
        if (clampedShock >= cd4CatastrophicBps || newEMA >= cd4CatastrophicBps) {
            // 1. Catastrophic Attack -> Enter Wormhole Hibernation ({0,3,6})
            // Freeze (cx, cy, zoom) to prevent adversarial weight poisoning!
            g.lifecycleState = STATE_HIBERNATION;
            g.lastResidueMod9 = (3 * zmod9Residue) % 9;
            if (g.fitnessScore < 65533) g.fitnessScore += 2;
            emit CellEnteredWormholeHibernation(newEMA, g.lastResidueMod9, g.cx, g.cy);
        } else if (g.lifecycleState == STATE_HIBERNATION) {
            // 2. Check for Adiabatic Awakening into Coprime Unit Group {1,2,4,5,7,8}
            if (newEMA < 2200 && clampedShock < 1500 && isUnit) {
                g.lifecycleState = STATE_HOMEOSTASIS;
                g.lastResidueMod9 = zmod9Residue;
                if (g.fitnessScore < 65532) g.fitnessScore += 3;
            } else {
                g.lifecycleState = STATE_HIBERNATION;
                g.lastResidueMod9 = (3 * zmod9Residue) % 9;
            }
        } else if (effectiveShock > 1800 || newEMA > 2400) {
            // 3. Elevated Stress -> CD4+ Hyper-Immune Guard (freeze genome, boost fee)
            g.lifecycleState = STATE_HYPER_IMMUNE;
            g.lastResidueMod9 = zmod9Residue;
            if (g.fitnessScore < 65534) g.fitnessScore += 1;
        } else {
            // 4. Calm / Organic Flow -> Homeostasis & Autonomous Epigenetic Plasticity
            g.lifecycleState = STATE_HOMEOSTASIS;
            g.lastResidueMod9 = zmod9Residue;
            _attemptEpigeneticEvolution(g, q1, q2, q3, q4, blackCount, newEMA, stateHash);
        }

        g.rollingStressEMA = newEMA;

        // Synthesize Dynamic Fee & Decision Output
        if (g.lifecycleState == STATE_HIBERNATION) {
            dynamicFeeBps = 5000;
            noulAllowed = false;
        } else if (g.lifecycleState == STATE_HYPER_IMMUNE) {
            uint16 quadShear = _absDiff(uint16(q1) + uint16(q3), uint16(q2) + uint16(q4));
            uint16 penalty = 1200 + uint16((uint32(effectiveShock) * 3200) / 10000) + (quadShear * 45);
            if (!isUnit) penalty += 350;
            dynamicFeeBps = penalty > 5000 ? 5000 : penalty;
            noulAllowed = dynamicFeeBps < 4200;
        } else {
            bool autoGuard4d = (g.orthoConfigBits & 0x04) != 0;
            if (autoGuard4d && effectiveShock <= 1500) {
                dynamicFeeBps = 500;
            } else {
                uint16 fee = 500 + (effectiveShock >> 2);
                dynamicFeeBps = fee > 5000 ? 5000 : fee;
            }
            noulAllowed = true;
        }

        // Single warm SSTORE back to the 256-bit slot
        livingGenomeSlot = _packGenome(g);

        emit CellPerceived(stateHash, g.lifecycleState, dynamicFeeBps, g.rollingStressEMA, g.generation);
        return (noulAllowed, dynamicFeeBps, g.lifecycleState, g.generation, g.rollingStressEMA);
    }

    function _attemptEpigeneticEvolution(
        UnpackedGenome memory g,
        uint8 q1,
        uint8 q2,
        uint8 q3,
        uint8 q4,
        uint8 blackCount,
        uint16 newEMA,
        bytes32 stateHash
    ) internal {
        int64 gradX = (int64(uint64(q1)) + int64(uint64(q4))) - (int64(uint64(q2)) + int64(uint64(q3)));
        int64 gradY = (int64(uint64(q1)) + int64(uint64(q2))) - (int64(uint64(q3)) + int64(uint64(q4)));

        bool needsShift = (blackCount < 3) || (blackCount > 9);
        bool periodic = (uint8(stateHash[0]) & 0x07) == 0;

        if (needsShift || periodic) {
            int64 candCx = g.cx;
            int64 candCy = g.cy;
            bool spark = false;

            if ((blackCount == 0 || blackCount == 12) && (g.lastResidueMod9 % 3 != 0)) {
                // Cauchy Zinc-Spark Jump over (Z/9Z)^x
                candCx += (g.lastResidueMod9 & 1 == 1) ? int64(21) : int64(-21);
                candCy += (g.lastResidueMod9 & 1 == 1) ? int64(-13) : int64(13);
                spark = true;
            } else {
                int64 stepX = gradX >> 1;
                int64 stepY = gradY >> 1;
                if (stepX > 8) stepX = 8;
                if (stepX < -8) stepX = -8;
                if (stepY > 8) stepY = 8;
                if (stepY < -8) stepY = -8;
                if (stepX == 0 && stepY == 0) {
                    stepX = (uint8(stateHash[0]) & 1) == 1 ? int64(1) : int64(-1);
                }
                candCx += stepX;
                candCy += stepY;
            }

            uint64 candZoom = g.zoom;
            if (newEMA < 800 && g.zoom < 3600000) {
                candZoom += 1024;
            } else if (newEMA > 1400 && g.zoom > 2000000) {
                candZoom -= 1024;
            }

            if (verifyProofOfHorizon(candCx, candCy, candZoom)) {
                g.cx = candCx;
                g.cy = candCy;
                g.zoom = candZoom;
                unchecked { g.generation += 1; }
                if (g.fitnessScore < 65535) g.fitnessScore += 1;
                g.lifecycleState = STATE_PLASTICITY;
                emit CellEvolvedOnChain(g.generation, candCx, candCy, candZoom, g.fitnessScore, spark);
            }
        }
    }

    function _perceiveTripod(
        UnpackedGenome memory g,
        bytes32 stateHash,
        uint16 effectiveShock
    )
        internal
        pure
        returns (
            uint8 q1,
            uint8 q2,
            uint8 q3,
            uint8 q4,
            uint8 blackCount
        )
    {
        uint64 safeZoom = g.zoom < uint64(WerrMath.ONE) ? uint64(WerrMath.ONE) : g.zoom;
        int64 zInt = int64(safeZoom);

        bool autoGuard4d = (g.orthoConfigBits & 0x04) != 0;
        bool phaseLock = (g.orthoConfigBits & 0x02) != 0;

        int64 jitterScale = phaseLock ? int64(256) : int64(512);
        int64 h0 = int64(uint64(uint16(uint256(stateHash) >> 240))) - 32768;
        int64 h1 = int64(uint64(uint16(uint256(stateHash) >> 176))) - 32768;

        int64 dx = (h0 * jitterScale) / zInt;
        int64 dy = (h1 * jitterScale) / zInt;
        int64 shockShift;

        if (autoGuard4d && effectiveShock <= 1500) {
            dx = dx >> 2;
            dy = dy >> 2;
            shockShift = (int64(uint64(effectiveShock)) * 64) / zInt;
        } else {
            shockShift = (int64(uint64(effectiveShock)) * 512) / zInt;
        }

        int64 evalCx = g.cx + dx + shockShift;
        int64 evalCy = g.cy + dy - (shockShift >> 1);

        int64 baseStep = int64(uint64(WerrMath.ONE) << 16) / zInt;
        int64[3] memory steps = [
            WerrMath.mulFP(baseStep, 109226),
            baseStep,
            WerrMath.mulFP(baseStep, 40960)
        ];

        for (uint256 s = 0; s < 3; ) {
            int64 half = steps[s] >> 1;
            uint8 e1 = _escapeZMod9(evalCx - half, evalCy + half);
            uint8 e2 = _escapeZMod9(evalCx + half, evalCy + half);
            uint8 e3 = _escapeZMod9(evalCx - half, evalCy - half);
            uint8 e4 = _escapeZMod9(evalCx + half, evalCy - half);

            q1 += e1;
            q2 += e2;
            q3 += e3;
            q4 += e4;
            if (e1 == 9) blackCount++;
            if (e2 == 9) blackCount++;
            if (e3 == 9) blackCount++;
            if (e4 == 9) blackCount++;
            unchecked { ++s; }
        }
    }

    function _escapeZMod9(int64 cx, int64 cy) internal pure returns (uint8) {
        int64 zx = 0;
        int64 zy = 0;
        for (uint8 i = 0; i < 9; ) {
            int64 zx2 = (zx * zx) >> 16;
            int64 zy2 = (zy * zy) >> 16;
            if (zx2 + zy2 > WerrMath.ESCAPE_LIMIT) {
                return i;
            }
            int64 nextZx = zx2 - zy2 + cx;
            int64 nextZy = ((zx * zy) >> 15) + cy;
            zx = nextZx;
            zy = nextZy;
            unchecked { ++i; }
        }
        return 9;
    }

    function _packGenome(UnpackedGenome memory g) internal pure returns (uint256) {
        uint256 cxU64 = uint256(uint64(g.cx));
        uint256 cyU64 = uint256(uint64(g.cy));
        uint256 zoomU64 = uint256(g.zoom);
        uint256 emaU16 = uint256(g.rollingStressEMA);
        uint256 fitU16 = uint256(g.fitnessScore);
        uint256 genU16 = uint256(g.generation);
        uint256 byte30 = uint256(((g.lifecycleState & 0x03) << 4) | (g.lastResidueMod9 & 0x0F));
        uint256 byte31 = uint256(((g.cd4ToleranceTier & 0x0F) << 4) | ((g.orthoConfigBits & 0x07) << 1) | (g.activeFlag & 0x01));

        return cxU64
            | (cyU64 << 64)
            | (zoomU64 << 128)
            | (emaU16 << 192)
            | (fitU16 << 208)
            | (genU16 << 224)
            | (byte30 << 240)
            | (byte31 << 248);
    }

    function _unpackGenome(uint256 slot) internal pure returns (UnpackedGenome memory g) {
        g.cx = int64(uint64(slot));
        g.cy = int64(uint64(slot >> 64));
        g.zoom = uint64(slot >> 128);
        g.rollingStressEMA = uint16(slot >> 192);
        g.fitnessScore = uint16(slot >> 208);
        g.generation = uint16(slot >> 224);
        uint8 byte30 = uint8(slot >> 240);
        uint8 byte31 = uint8(slot >> 248);
        g.lastResidueMod9 = byte30 & 0x0F;
        g.lifecycleState = (byte30 >> 4) & 0x03;
        g.activeFlag = byte31 & 0x01;
        g.orthoConfigBits = (byte31 >> 1) & 0x07;
        uint8 cd4 = (byte31 >> 4) & 0x0F;
        g.cd4ToleranceTier = cd4 == 0 ? 8 : cd4;
    }

    function _absDiff(uint16 a, uint16 b) internal pure returns (uint16) {
        return a >= b ? a - b : b - a;
    }
}
