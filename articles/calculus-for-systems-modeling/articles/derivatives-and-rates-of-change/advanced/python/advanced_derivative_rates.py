from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
import math


@dataclass(frozen=True)
class InvariantReview:
    value: float
    lower: float
    upper: float
    inside: bool
    issue: str


def response(x: float) -> float:
    return math.exp(0.2 * x)


def exact_derivative(x: float) -> float:
    return 0.2 * math.exp(0.2 * x)


def forward_difference(x: float, h: float) -> float:
    if h <= 0:
        raise ValueError("h must be positive")
    return (response(x + h) - response(x)) / h


def central_difference(x: float, h: float) -> float:
    if h <= 0:
        raise ValueError("h must be positive")
    return (response(x + h) - response(x - h)) / (2.0 * h)


def rate_diagnostics(x: float = 5.0) -> list[dict[str, object]]:
    h_values = [1.0, 0.5, 0.25, 0.125, 0.0625, 0.03125]
    exact = exact_derivative(x)
    rows = []
    for h in h_values:
        for method, estimate in {
            "forward_difference": forward_difference(x, h),
            "central_difference": central_difference(x, h),
        }.items():
            rows.append({
                "method": method,
                "x": x,
                "h": h,
                "estimate": estimate,
                "exact": exact,
                "absolute_error": abs(estimate - exact),
                "elasticity": (x / response(x)) * estimate,
            })
    return rows


def convergence_orders(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    out = []
    for method in sorted({row["method"] for row in rows}):
        vals = sorted([row for row in rows if row["method"] == method], key=lambda row: float(row["h"]), reverse=True)
        for a, b in zip(vals, vals[1:]):
            e1, e2 = float(a["absolute_error"]), float(b["absolute_error"])
            out.append({
                "method": method,
                "h_large": a["h"],
                "h_small": b["h"],
                "error_large": e1,
                "error_small": e2,
                "estimated_order": math.log(e1 / e2) / math.log(float(a["h"]) / float(b["h"])) if e1 > 0 and e2 > 0 else float("nan"),
            })
    return out


def roundoff_review(x: float = 5.0) -> list[dict[str, object]]:
    exact = exact_derivative(x)
    rows = []
    previous = None
    for k in range(1, 13):
        h = 10.0 ** (-k)
        estimate = forward_difference(x, h)
        error = abs(estimate - exact)
        warning = "error increased after refinement; possible roundoff/cancellation" if previous is not None and error > previous else ""
        rows.append({"h": h, "estimate": estimate, "absolute_error": error, "warning": warning})
        previous = error
    return rows


def invariant_review(values: list[float], lower: float = 0.0, upper: float = 1.0) -> list[InvariantReview]:
    return [InvariantReview(v, lower, upper, lower <= v <= upper, "" if lower <= v <= upper else "outside invariant interval") for v in values]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def to_dicts(records: list[object]) -> list[dict[str, object]]:
    return [asdict(item) for item in records]
