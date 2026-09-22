"""
werracle.engine.core
====================
Standalone, Zero-External-Dependency Fractal Decision Engine for Werracle.
Derived from WERR (v0.4.0-stable) mathematical foundations.
Operates completely isolated from any external werr/answerr packages.
"""

import math
import hashlib
from typing import Dict, List, Any, Optional, Tuple


def sigmoid(x: float) -> float:
    """Bounded logistic sigmoid function."""
    if x < -40.0:
        return 0.0
    if x > 40.0:
        return 1.0
    return 1.0 / (1.0 + math.exp(-x))


def compute_mandelbrot_patch(
    cx: float,
    cy: float,
    zoom: float,
    res: int = 32,
    max_iter: int = 50
) -> Tuple[float, float, List[List[int]]]:
    """
    Evaluates Mandelbrot escape dynamics over a 2D patch centered at (cx, cy).
    Returns:
        black_ratio (float): Fraction of non-escaping (stable) points [0.0, 1.0].
        avg_escape (float): Normalized mean escape iteration.
        grid (List[List[int]]): 2D iteration escape matrix.
    """
    scale = 1.0 / zoom if zoom > 0 else 1.0
    half_res = res / 2.0
    total_points = res * res
    black_count = 0
    total_iters = 0
    grid = []

    for r in range(res):
        row = []
        py = cy + (r - half_res) * (scale / half_res)
        for c in range(res):
            px = cx + (c - half_res) * (scale / half_res)
            
            # zn+1 = zn^2 + c
            zx, zy = 0.0, 0.0
            iters = max_iter
            for i in range(max_iter):
                zx2 = zx * zx
                zy2 = zy * zy
                if zx2 + zy2 > 4.0:
                    iters = i
                    break
                zy = 2.0 * zx * zy + py
                zx = zx2 - zy2 + px

            if iters == max_iter:
                black_count += 1
            total_iters += iters
            row.append(iters)
        grid.append(row)

    black_ratio = black_count / total_points
    avg_escape = total_iters / (total_points * max_iter)
    return black_ratio, avg_escape, grid


def extract_quadrant_weights(
    grid: List[List[int]],
    max_iter: int = 50
) -> Tuple[float, float, float, float, List[float]]:
    """
    Extracts 4-quadrant escape ratios (Q1: top-right, Q2: top-left, Q3: bottom-left, Q4: bottom-right).
    Returns zero-centered synaptic weights (w1, w2, w3, b) in [-1.0, 1.0].
    """
    res = len(grid)
    mid = res // 2
    max_q_sum = (mid * mid) * max_iter

    q_sums = [0, 0, 0, 0]
    for r in range(res):
        for c in range(res):
            val = grid[r][c]
            if r < mid and c >= mid:
                q_sums[0] += val # Q1 (+x, +y)
            elif r < mid and c < mid:
                q_sums[1] += val # Q2 (-x, +y)
            elif r >= mid and c < mid:
                q_sums[2] += val # Q3 (-x, -y)
            else:
                q_sums[3] += val # Q4 (+x, -y)

    ratios = [s / max_q_sum if max_q_sum > 0 else 0.5 for s in q_sums]
    w1 = (ratios[0] - 0.5) * 2.0
    w2 = (ratios[1] - 0.5) * 2.0
    w3 = (ratios[2] - 0.5) * 2.0
    b  = (ratios[3] - 0.5) * 2.0
    return w1, w2, w3, b, ratios


class WerracleCoreEngine:
    """
    Standalone Werracle Fractal Reflex Engine.
    Executes typed System-1 decisions natively with 0 Bytes stored weight tensors.
    """
    def __init__(
        self,
        base_cx: float = -0.7436438870371587,
        base_cy: float = 0.13182590420531197,
        base_zoom: float = 50.0,
        resolution: int = 32,
        max_iter: int = 30
    ):
        self.cx = base_cx
        self.cy = base_cy
        self.zoom = base_zoom
        self.resolution = resolution
        self.max_iter = max_iter

    def decide_noul(
        self,
        risk_signal: float,
        context_name: str = "default"
    ) -> Dict[str, Any]:
        """
        Noul Boolean Decision:
        Returns {'allowed': bool, 'probability': float, 'confidence': float, 'latency_us': float}
        """
        # Perturb coordinate slightly with context hash for dynamic diversity
        h = int(hashlib.md5(context_name.encode('utf-8')).hexdigest()[:6], 16)
        delta = (h / 16777215.0 - 0.5) * (0.1 / self.zoom)

        black_ratio, _, grid = compute_mandelbrot_patch(
            self.cx + delta, self.cy + delta, self.zoom, self.resolution, self.max_iter
        )
        w1, w2, w3, b, _ = extract_quadrant_weights(grid, self.max_iter)

        fractal_bias = (w1 + w2 - w3 - b) * 0.25
        logit = -risk_signal + fractal_bias
        prob = sigmoid(logit)

        allowed = prob >= 0.5
        confidence = prob if allowed else (1.0 - prob)

        return {
            "allowed": allowed,
            "probability": round(prob, 4),
            "confidence": round(confidence, 4),
            "black_ratio": round(black_ratio, 4),
            "fractal_bias": round(fractal_bias, 4)
        }

    def decide_choice(
        self,
        num_choices: int,
        context_bias: float = 0.0
    ) -> int:
        """
        Choice Route Selector:
        Evaluates best quadrant path among N choices.
        """
        if num_choices <= 1:
            return 0
        _, _, grid = compute_mandelbrot_patch(
            self.cx, self.cy, self.zoom, self.resolution, self.max_iter
        )
        weights = extract_quadrant_weights(grid, self.max_iter)[:4]

        best_score = -1e9
        best_idx = 0
        for i in range(num_choices):
            score = weights[i % 4] + context_bias * (i + 1) * 0.1
            if score > best_score:
                best_score = score
                best_idx = i
        return best_idx

    def decide_score(
        self,
        risk_signal: float,
        max_score: int = 3
    ) -> int:
        """
        Severity / Priority Score:
        Maps continuous risk to [0 .. max_score].
        """
        # Normalized risk into [0.0, 1.0]
        norm = max(0.0, min(1.0, (risk_signal + 2.0) / 4.0))
        return int(round(norm * max_score))
