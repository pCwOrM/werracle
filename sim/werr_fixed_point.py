"""
werracle.sim.werr_fixed_point
=============================
Pure Python integer simulation of the Q16.16 fixed-point Mandelbrot escape
kernel designed for EVM execution (Werracle.sol).

Fixed-Point Representation:
- Q16.16: 1.0 == 65536 (1 << 16)
- Coordinates and scale fit within 64-bit signed/unsigned integers.
- Zero floating-point operations. Bit-shifts and integer arithmetic only.
"""

# Scale factor: 2^16 = 65536
ONE = 1 << 16
HALF = ONE >> 1
FOUR = ONE << 2
ESCAPE_RADIUS_SQ = FOUR  # in Q16.16, 4.0 == 262144

# Default Seahorse Valley Seed in Q16.16
# cx = -0.7436438870371587 -> -0.743643887 * 65536 = -48735
# cy = +0.1318259042053119 -> +0.131825904 * 65536 = +8639
# zoom = 50.0              -> 50.0 * 65536 = 3276800
DEFAULT_CX_FP = int(-0.7436438870371587 * ONE)
DEFAULT_CY_FP = int(0.13182590420531197 * ONE)
DEFAULT_ZOOM_FP = int(50.0 * ONE)
MAX_ITER = 12


def mul_fp(a: int, b: int) -> int:
    """Fixed-point multiplication (Q16.16 * Q16.16 -> Q16.16)."""
    return (a * b) >> 16


def div_fp(a: int, b: int) -> int:
    """Fixed-point division (Q16.16 / Q16.16 -> Q16.16)."""
    if b == 0:
        return 0
    return (a << 16) // b


def sigmoid_fp(x: int) -> int:
    """
    Fast Piecewise Linear / Pade Sigmoid Approximation in Q16.16.
    Returns probability in Basis Points [0, 10000] (0.00% to 100.00%).
    """
    # Clamp extreme bounds (-4.0 to +4.0)
    four = 4 * ONE
    if x <= -four:
        return 180   # ~1.8%
    if x >= four:
        return 9820  # ~98.2%
    
    # Linear slope region: P(x) ~= 0.5 + 0.12 * x
    # 0.12 in Q16.16 ~= 7864
    p = HALF + mul_fp(x, 7864)
    # Convert from Q16.16 to basis points [0..10000]
    bps = (p * 10000) >> 16
    return max(100, min(9900, bps))


def iterate_mandelbrot_point(cx: int, cy: int, max_iter: int = MAX_ITER) -> int:
    """
    Performs quadratic escape zn+1 = zn^2 + c for a single Q16.16 coordinate.
    Returns:
        iter_count (int): Number of iterations before escape (0 to max_iter).
    """
    zx = 0
    zy = 0
    for i in range(max_iter):
        zx2 = (zx * zx) >> 16
        zy2 = (zy * zy) >> 16
        
        # Check escape: |z|^2 = zx^2 + zy^2 > 4.0
        if (zx2 + zy2) > ESCAPE_RADIUS_SQ:
            return i
        
        # zn+1 = zn^2 + c
        # new_zx = zx^2 - zy^2 + cx
        # new_zy = 2 * zx * zy + cy
        new_zx = zx2 - zy2 + cx
        new_zy = ((zx * zy) >> 15) + cy  # (2 * zx * zy) >> 16 == (zx * zy) >> 15
        zx = new_zx
        zy = new_zy
    
    return max_iter


def sample_quadrants_microgrid(cx: int, cy: int, zoom: int) -> dict:
    """
    Samples a 16-point (4x4) Pareto micro-grid across 4 quadrants.
    Returns quadrant mass ratios (r1, r2, r3, r4) and black_ratio.
    """
    # step = 1.0 / zoom
    step = div_fp(ONE, zoom) if zoom > 0 else ONE
    sub_step = step >> 1  # step / 2

    # 4 offsets per quadrant (16 points total)
    # Q1: (+x, +y), Q2: (-x, +y), Q3: (-x, -y), Q4: (+x, -y)
    quad_escapes = [0, 0, 0, 0]
    total_black = 0

    offsets = [
        # Q1 (+x, +y)
        (sub_step, sub_step, 0), (step, sub_step, 0), (sub_step, step, 0), (step, step, 0),
        # Q2 (-x, +y)
        (-sub_step, sub_step, 1), (-step, sub_step, 1), (-sub_step, step, 1), (-step, step, 1),
        # Q3 (-x, -y)
        (-sub_step, -sub_step, 2), (-step, -sub_step, 2), (-sub_step, -step, 2), (-step, -step, 2),
        # Q4 (+x, -y)
        (sub_step, -sub_step, 3), (step, -sub_step, 3), (sub_step, -step, 3), (step, -step, 3)
    ]

    for ox, oy, q_idx in offsets:
        px = cx + ox
        py = cy + oy
        iters = iterate_mandelbrot_point(px, py, MAX_ITER)
        if iters == MAX_ITER:
            total_black += 1
        quad_escapes[q_idx] += iters

    # Normalized ratios (0 to 65536)
    # Max possible escape sum per quadrant = 4 * MAX_ITER = 48
    max_q_sum = 4 * MAX_ITER
    ratios = [(q_sum * ONE) // max_q_sum for q_sum in quad_escapes]
    black_ratio_bps = (total_black * 10000) // 16

    return {
        "r1": ratios[0],
        "r2": ratios[1],
        "r3": ratios[2],
        "r4": ratios[3],
        "weights": [r - HALF for r in ratios],  # Zero-centered [-HALF, +HALF]
        "black_ratio_bps": black_ratio_bps
    }


class WerracleFixedPointEngine:
    """
    Fixed-point EVM-equivalent decision engine.
    Produces identical results to Werracle.sol contract.
    """
    def __init__(
        self,
        cx: int = DEFAULT_CX_FP,
        cy: int = DEFAULT_CY_FP,
        zoom: int = DEFAULT_ZOOM_FP
    ):
        self.cx = cx
        self.cy = cy
        self.zoom = zoom

    def decide_noul(self, risk_signal_fp: int) -> tuple[bool, int]:
        """
        Noul Boolean Gate:
        - risk_signal_fp > 0 : High risk (tends to DENY)
        - risk_signal_fp < 0 : Low risk (tends to ALLOW)
        Returns:
            (allowed: bool, confidence_bps: int)
        """
        grid = sample_quadrants_microgrid(self.cx, self.cy, self.zoom)
        # Fractal bias from quadrant balance
        # bias = (w1 + w2 - w3 - w4) / 4
        w = grid["weights"]
        fractal_bias = (w[0] + w[1] - w[2] - w[3]) >> 2
        
        # Net logit = -risk_signal + fractal_bias
        logit = -risk_signal_fp + fractal_bias
        prob_bps = sigmoid_fp(logit)
        
        allowed = prob_bps >= 5000
        confidence = prob_bps if allowed else (10000 - prob_bps)
        return allowed, confidence

    def decide_choice(self, num_choices: int, context_bias_fp: int = 0) -> int:
        """
        Choice Route Selector:
        Evaluates best quadrant path among N choices.
        Returns selected choice index (0 to num_choices - 1).
        """
        if num_choices <= 1:
            return 0
        grid = sample_quadrants_microgrid(self.cx, self.cy, self.zoom)
        w = grid["weights"]
        
        best_idx = 0
        best_score = -1000000000
        for i in range(num_choices):
            score = w[i % 4] + ((context_bias_fp * (i + 1)) >> 2)
            if score > best_score:
                best_score = score
                best_idx = i
        return best_idx

    def decide_score(self, risk_signal_fp: int, max_score: int = 3) -> int:
        """
        Score Evaluator:
        Scales risk and fractal escape into [0, max_score].
        Returns integer level.
        """
        grid = sample_quadrants_microgrid(self.cx, self.cy, self.zoom)
        # Combine risk signal with escape velocity
        # Base normalized level: 0 to ONE
        raw_level = max(0, min(ONE, (risk_signal_fp + (2 * ONE)) >> 2))
        return (raw_level * max_score) >> 16
