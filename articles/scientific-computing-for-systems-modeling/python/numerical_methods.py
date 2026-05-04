"""
Scientific Computing for Systems Modeling:
Numerical integration, root finding, and finite differences.

Educational example only.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def trapezoid_integral(x: np.ndarray, y: np.ndarray) -> float:
    """Approximate an integral using the trapezoid rule."""
    total = 0.0

    for i in range(1, len(x)):
        width = x[i] - x[i - 1]
        total += 0.5 * (y[i] + y[i - 1]) * width

    return float(total)


def finite_difference_derivative(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Approximate derivative values using finite differences."""
    return np.gradient(y, x)


def bisection_root(function, lower: float, upper: float, tolerance: float = 1e-8, max_iter: int = 100) -> float:
    """Approximate a root using the bisection method."""
    f_lower = function(lower)
    f_upper = function(upper)

    if f_lower * f_upper > 0:
        raise ValueError("Bisection requires a sign change over the interval.")

    for _ in range(max_iter):
        midpoint = 0.5 * (lower + upper)
        f_mid = function(midpoint)

        if abs(f_mid) < tolerance:
            return midpoint

        if f_lower * f_mid < 0:
            upper = midpoint
            f_upper = f_mid
        else:
            lower = midpoint
            f_lower = f_mid

    return 0.5 * (lower + upper)


def main() -> None:
    x = np.linspace(0, 10, 501)
    y = np.sin(x) + 1.5

    integral_estimate = trapezoid_integral(x, y)
    derivative = finite_difference_derivative(x, y)
    root = bisection_root(lambda z: z**2 - 2.0, lower=0.0, upper=2.0)

    outputs = pd.DataFrame({
        "x": x,
        "y": y,
        "finite_difference_derivative": derivative
    })

    summary = pd.DataFrame({
        "metric": ["trapezoid_integral_estimate", "bisection_root_sqrt_2"],
        "value": [integral_estimate, root]
    })

    print(summary)

    outputs.to_csv("../outputs/python_numerical_methods_outputs.csv", index=False)
    summary.to_csv("../outputs/python_numerical_methods_summary.csv", index=False)


if __name__ == "__main__":
    main()
