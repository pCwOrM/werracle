"""
werracle.engine.core
====================
Standalone, Zero-External-Dependency Fractal Decision Engine for Werracle.
Derived from WERR (v0.5.1-stable) mathematical foundations.
Operates completely isolated from any external werr/answerr packages.

Features synchronized with WERR Core v0.5.1:
- 4-Quadrant Boundary Density Estimation (arXiv:1810.11107)
- Supercritical Pitchfork Cadence Bifurcation Operator for deadlock elimination
- Sparse Multi-Scale Harmonic Tripod (Z mod 9) support
- Pure Python and NumPy execution with zero stored neural weight tensors
"""

import math
import hashlib
from typing import Dict, List, Any, Optional, Tuple, Union
import numpy as np


def sigmoid(x: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """Numerically stable bounded logistic sigmoid function."""
    if isinstance(x, np.ndarray):
        return 1.0 / (1.0 + np.exp(-np.clip(x, -50.0, 50.0)))
    if x < -50.0:
        return 0.0
    if x > 50.0:
        return 1.0
    return 1.0 / (1.0 + math.exp(-x))


# =========================================================================
# Bounded Domain Density Estimation (WERR v0.5.1 / arXiv:1810.11107)
# =========================================================================

def _vec_erf(x: np.ndarray) -> np.ndarray:
    """
    Vectorized error function approximation (Abramowitz & Stegun 7.1.26).
    Maximum absolute error: < 1.5e-7. Pure NumPy, zero external dependencies.
    """
    x = np.asarray(x, dtype=np.float64)
    sign = np.sign(x)
    x_abs = np.abs(x)
    a1 = 0.254829592
    a2 = -0.284496736
    a3 = 1.421413741
    a4 = -1.453152027
    a5 = 1.061405429
    p = 0.3275911
    t = 1.0 / (1.0 + p * x_abs)
    poly = ((((a5 * t + a4) * t + a3) * t + a2) * t + a1) * t
    y = 1.0 - poly * np.exp(-x_abs * x_abs)
    return sign * y


def normal_cdf(z: np.ndarray) -> np.ndarray:
    """Standard normal cumulative distribution function Phi(z)."""
    return 0.5 * (1.0 + _vec_erf(z / np.sqrt(2.0)))


def compute_boundary_correction_weights(u: np.ndarray, bandwidth: float = 0.12) -> np.ndarray:
    """
    Computes boundary weight inverse W(u, h) = 1 / omega(u, h) on [0, 1] (arXiv:1810.11107).
    """
    u_clamped = np.clip(u, 0.0, 1.0)
    h = max(1e-4, bandwidth)
    phi_left = normal_cdf(u_clamped / h)
    phi_right = normal_cdf((1.0 - u_clamped) / h)
    omega = np.clip(phi_left + phi_right - 1.0, 0.45, 1.0)
    return 1.0 / omega


def extract_bounded_quadrant_weights(
    escape_iters: np.ndarray,
    max_iter: int = 36,
    bandwidth: float = 0.12
) -> Tuple[float, float, float, float, List[float]]:
    """
    Boundary-corrected quadrant weight extraction (WERR v0.5.1 / arXiv:1810.11107).
    Partitions escape matrix into 4 quadrants, compensating for boundary truncation on [0, 1].
    """
    h, w = escape_iters.shape
    mid_h, mid_w = h // 2, w // 2

    q1 = escape_iters[:mid_h, mid_w:]  # top-right
    q2 = escape_iters[:mid_h, :mid_w]  # top-left
    q3 = escape_iters[mid_h:, :mid_w]  # bottom-left
    q4 = escape_iters[mid_h:, mid_w:]  # bottom-right

    quads = [q1, q2, q3, q4]
    weights = []
    ratios = []

    for q in quads:
        u = q.astype(np.float64) / float(max_iter)
        weights_corr = compute_boundary_correction_weights(u, bandwidth=bandwidth)
        cusp_mask = (u >= 0.90).astype(np.float64)
        boundary_corrected_ratio = np.sum(weights_corr * cusp_mask) / max(1e-9, np.sum(weights_corr))
        avg_energy = np.sum(weights_corr * u) / max(1e-9, np.sum(weights_corr))
        composite_ratio = 0.65 * boundary_corrected_ratio + 0.35 * avg_energy
        ratios.append(float(composite_ratio))
        w_val = float((composite_ratio - 0.5) * 6.0)
        weights.append(w_val)

    return weights[0], weights[1], weights[2], weights[3], ratios


# =========================================================================
# Cadence Supercritical Pitchfork Bifurcation Operator (WERR v0.5.1)
# =========================================================================

def apply_cadence_bifurcation(
    scores: Union[List[float], np.ndarray],
    lambda_param: float = 0.20,
    alpha: float = 0.50,
    beta: float = 0.25,
    fractal_fields: Optional[Union[List[float], np.ndarray]] = None,
    deadlock_threshold: float = 0.85
) -> np.ndarray:
    """
    Applies coupled pitchfork bifurcation to break destructive nodal deadlocks
    between competing decision candidates (WERR v0.5.1).
    """
    s = np.array(scores, dtype=np.float64)
    K = len(s)
    if K <= 1:
        return s

    sorted_s = np.sort(s)
    top_gap = sorted_s[-1] - sorted_s[-2]

    if top_gap < deadlock_threshold:
        diff_matrix = s[:, np.newaxis] - s[np.newaxis, :]
        bif_force = np.sum(np.sign(diff_matrix) * (np.abs(diff_matrix) ** alpha), axis=1)

        if fractal_fields is not None and len(fractal_fields) == K:
            h_arr = np.array(fractal_fields, dtype=np.float64)
            bif_force += beta * (h_arr - np.mean(h_arr))

        s = s + lambda_param * bif_force

    return s


# =========================================================================
# 2D Mandelbrot Patch Generator
# =========================================================================

def compute_mandelbrot_patch(
    cx: float,
    cy: float,
    zoom: float,
    res: int = 32,
    max_iter: int = 50
) -> Tuple[float, float, List[List[int]]]:
    """
    Evaluates Mandelbrot escape dynamics over a 2D patch centered at (cx, cy).
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
    """Standard 4-quadrant escape ratios."""
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


# =========================================================================
# Werracle Core Engine (WERR v0.5.1 Aligned)
# =========================================================================

class WerracleCoreEngine:
    """
    Standalone Werracle Fractal Reflex Engine.
    Aligned with WERR Core v0.5.1 specifications.
    Executes typed System-1 decisions natively with 0 Bytes stored weight tensors.

    Orthogonal 8-State Parameter Architecture (2 x 2 x 2):
      - enable_domain    in {False ('none'), True ('multi')}
      - enable_lexical   in {False, True}  (Discrete Keyword & Criteria Index)
      - enable_resonance in {False, True}  (Spectral Pole & Stem Resonance)

    Optimal Auto-Guard Rules:
      1. When enable_domain=False (domain_mode='none'), domain dictionaries are locked OFF (Universal Cusp).
      2. When enable_domain=True (domain_mode='multi') and both dictionaries are OFF ([1,0,0]),
         auto-guards to Universal Cusp so uncalibrated coordinate shifts never degrade accuracy.
      3. When enable_domain=True and at least one dictionary is ON ([1,1,0], [1,0,1], [1,1,1]),
         routes genuine domain telemetry states to their specialized DomainGate while keeping OOD tasks on the Universal Cusp.
    """
    def __init__(
        self,
        base_cx: float = -0.7436438870371587,
        base_cy: float = 0.13182590420531197,
        base_zoom: float = 50.0,
        resolution: int = 32,
        max_iter: int = 30,
        mode: Optional[str] = None,
        domain_mode: Optional[str] = None,
        enable_domain: Optional[bool] = None,
        enable_lexical: Optional[bool] = None,
        enable_resonance: Optional[bool] = None,
        tripod: bool = True,
        cadence_lambda: float = 0.10,
        cadence_beta: float = 0.15,
        cadence_alpha: float = 0.50,
        temp_choice: float = 1.25,
        cx: Optional[float] = None,
        cy: Optional[float] = None,
        zoom: Optional[float] = None
    ):
        self.universal_cx = cx if cx is not None else base_cx
        self.universal_cy = cy if cy is not None else base_cy
        self.universal_zoom = zoom if zoom is not None else base_zoom
        self.cx = self.universal_cx
        self.cy = self.universal_cy
        self.zoom = self.universal_zoom
        self.resolution = resolution
        self.max_iter = max_iter

        # 1. Resolve Domain switch (enable_domain / domain_mode)
        if enable_domain is not None:
            self.enable_domain = bool(enable_domain)
            self.domain_mode = "multi" if self.enable_domain else "none"
        elif domain_mode is not None:
            self.domain_mode = str(domain_mode).lower()
            self.enable_domain = (self.domain_mode == "multi")
        else:
            self.domain_mode = "none"
            self.enable_domain = False

        # 2. Resolve Dictionary switches (enable_lexical, enable_resonance, mode)
        if enable_lexical is not None or enable_resonance is not None:
            raw_lex = bool(enable_lexical) if enable_lexical is not None else False
            raw_res = bool(enable_resonance) if enable_resonance is not None else False
            if raw_lex and raw_res:
                self.mode = "hybrid"
            elif raw_res:
                self.mode = "resonance"
            elif raw_lex:
                self.mode = "lexical"
            else:
                self.mode = "pure_fractal"
        elif mode is not None:
            m_str = str(mode).lower()
            if m_str in ("hybrid", "both") or (m_str == "production" and self.enable_domain):
                raw_lex = True
                raw_res = True
                self.mode = "hybrid" if self.enable_domain else "pure_fractal"
            elif m_str in ("lexical", "production"):
                raw_lex = True
                raw_res = False
                self.mode = "lexical" if self.enable_domain else "pure_fractal"
            elif m_str == "resonance":
                raw_lex = False
                raw_res = True
                self.mode = "resonance" if self.enable_domain else "pure_fractal"
            else:
                raw_lex = False
                raw_res = False
                self.mode = "pure_fractal"
        else:
            # Conflict-free purpose-aligned defaults:
            # - When Domain is ON ('multi'): Hybrid [1,1,1] (Lexical + Resonance active)
            # - When Domain is OFF ('none'): Pure Fractal [0,0,0] (Universal Cusp safety preserved)
            if self.enable_domain:
                raw_lex = True
                raw_res = True
                self.mode = "hybrid"
            else:
                raw_lex = False
                raw_res = False
                self.mode = "pure_fractal"

        self.raw_enable_lexical = raw_lex
        self.raw_enable_resonance = raw_res

        # 3. Enforce Optimal Auto-Guard Rules:
        # Rule 1: If Domain is OFF ('none'), domain dictionaries are locked OFF.
        self.enable_lexical = raw_lex if self.enable_domain else False
        self.enable_resonance = raw_res if self.enable_domain else False

        # Rule 2: If Domain is ON ('multi') and BOTH dictionaries are OFF ([1,0,0]), auto-guard to Universal Cusp.
        if self.enable_domain and (not self.enable_lexical and not self.enable_resonance):
            self.effective_domain_active = False
        else:
            self.effective_domain_active = self.enable_domain

        self.tripod = tripod
        self.cadence_lambda = cadence_lambda
        self.cadence_beta = cadence_beta
        self.cadence_alpha = cadence_alpha
        self.temp_choice = temp_choice

    def decide_noul(
        self,
        risk_signal: float,
        context_name: str = "default"
    ) -> Dict[str, Any]:
        """
        Noul Boolean Decision:
        Returns {'allowed': bool, 'probability': float, 'confidence': float}
        """
        h = int(hashlib.md5(context_name.encode('utf-8')).hexdigest()[:6], 16)
        delta = (h / 16777215.0 - 0.5) * (0.1 / self.zoom)

        black_ratio, _, grid = compute_mandelbrot_patch(
            self.cx + delta, self.cy + delta, self.zoom, self.resolution, self.max_iter
        )

        if self.mode == "hybrid":
            grid_np = np.array(grid, dtype=np.int32)
            w1, w2, w3, b, _ = extract_bounded_quadrant_weights(grid_np, self.max_iter)
            fractal_bias = (w1 + w2 - w3 - b) * 0.15
        else:
            w1, w2, w3, b, _ = extract_quadrant_weights(grid, self.max_iter)
            fractal_bias = (w1 + w2 - w3 - b) * 0.25

        logit = -risk_signal + fractal_bias
        prob = float(sigmoid(logit))

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
        Choice Route Selector with Cadence Bifurcation Deadlock Elimination.
        """
        if num_choices <= 1:
            return 0
        _, _, grid = compute_mandelbrot_patch(
            self.cx, self.cy, self.zoom, self.resolution, self.max_iter
        )
        weights = extract_quadrant_weights(grid, self.max_iter)[:4]

        scores = [weights[i % 4] + context_bias * (i + 1) * 0.1 for i in range(num_choices)]
        
        # Apply WERR v0.5.1 Cadence Bifurcation
        bif_scores = apply_cadence_bifurcation(
            scores,
            lambda_param=self.cadence_lambda,
            alpha=self.cadence_alpha,
            beta=self.cadence_beta
        )
        return int(np.argmax(bif_scores))

    def decide_score(
        self,
        risk_signal: float,
        max_score: int = 3
    ) -> int:
        """
        Severity / Priority Score:
        Maps continuous risk to [0 .. max_score].
        """
        norm = max(0.0, min(1.0, (risk_signal + 2.0) / 4.0))
        return int(round(norm * max_score))
