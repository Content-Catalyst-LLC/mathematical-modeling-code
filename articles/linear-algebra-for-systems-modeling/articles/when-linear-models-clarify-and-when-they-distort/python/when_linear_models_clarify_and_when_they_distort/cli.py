from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class LinearityDistortionAudit:
    workflow_name: str
    model_purpose: str
    fitted_intercept: float
    fitted_slope: float
    residual_sum_squares: float
    max_absolute_residual: float
    residual_sign_pattern: str
    curvature_warning: str
    extrapolation_warning: str
    interpretation_warning: str


def mean(values: list[float]) -> float:
    return sum(values) / len(values)


def fit_simple_linear_model(x: list[float], y: list[float]) -> tuple[float, float]:
    x_mean = mean(x)
    y_mean = mean(y)
    numerator = sum((xi - x_mean) * (yi - y_mean) for xi, yi in zip(x, y))
    denominator = sum((xi - x_mean) ** 2 for xi in x)
    if abs(denominator) < 1e-15:
        raise ValueError("Cannot fit slope when all x values are identical.")
    slope = numerator / denominator
    intercept = y_mean - slope * x_mean
    return intercept, slope


def sign_pattern(values: list[float]) -> str:
    signs: list[str] = []
    for value in values:
        if value > 1e-9:
            signs.append("+")
        elif value < -1e-9:
            signs.append("-")
        else:
            signs.append("0")
    return "".join(signs)


def build_audit() -> LinearityDistortionAudit:
    x = [0.0, 1.0, 2.0, 3.0, 4.0]
    y = [1.0 + 0.7 * xi + 0.35 * xi * xi for xi in x]

    intercept, slope = fit_simple_linear_model(x, y)
    fitted = [intercept + slope * xi for xi in x]
    residuals = [yi - fi for yi, fi in zip(y, fitted)]

    rss = sum(r * r for r in residuals)
    max_abs = max(abs(r) for r in residuals)
    pattern = sign_pattern(residuals)

    curvature_warning = (
        "Residuals show a structured sign pattern consistent with curvature. "
        "The linear fit is useful as a baseline but risks distortion if interpreted as the system mechanism."
    )

    return LinearityDistortionAudit(
        workflow_name="linearity_distortion_audit",
        model_purpose="baseline_linear_approximation_for_system_behavior",
        fitted_intercept=round(intercept, 12),
        fitted_slope=round(slope, 12),
        residual_sum_squares=round(rss, 12),
        max_absolute_residual=round(max_abs, 12),
        residual_sign_pattern=pattern,
        curvature_warning=curvature_warning,
        extrapolation_warning="Do not extrapolate the fitted line beyond the observed operating range without additional validation.",
        interpretation_warning="Linear models clarify first-order structure, but residuals, thresholds, interactions, feedback, aggregation, and causal assumptions must be reviewed before using results for decisions.",
    )


def write_outputs(output_dir: Path) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)

    audit = build_audit()
    row = asdict(audit)

    with (output_dir / "tables" / "linearity_distortion_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)

    (output_dir / "json" / "linearity_distortion_audit.json").write_text(
        json.dumps(row, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    report = [
        "# Linearity Distortion Audit",
        "",
        f"- Workflow: {audit.workflow_name}",
        f"- Model purpose: {audit.model_purpose}",
        f"- Fitted intercept: {audit.fitted_intercept}",
        f"- Fitted slope: {audit.fitted_slope}",
        f"- Residual sum of squares: {audit.residual_sum_squares}",
        f"- Max absolute residual: {audit.max_absolute_residual}",
        f"- Residual sign pattern: {audit.residual_sign_pattern}",
        "",
        audit.curvature_warning,
        "",
        audit.extrapolation_warning,
        "",
        audit.interpretation_warning,
    ]
    (output_dir / "reports" / "linearity_distortion_audit.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Linearity distortion audit complete.")


if __name__ == "__main__":
    main()
