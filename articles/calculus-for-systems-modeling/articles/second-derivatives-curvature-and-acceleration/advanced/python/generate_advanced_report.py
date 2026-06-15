from pathlib import Path
import sys

CURRENT = Path(__file__).resolve()
ADVANCED_DIR = CURRENT.parents[1]
sys.path.insert(0, str(CURRENT.parent))

from advanced_second_derivatives import sample_checks, to_dicts, write_csv, write_json


def main() -> None:
    out = ADVANCED_DIR / "outputs"
    table_dir = out / "tables"
    report_dir = out / "reports"
    json_dir = out / "json"

    checks = to_dicts(sample_checks())
    failures = [row for row in checks if not row["passed"]]

    write_csv(table_dir / "advanced_second_derivative_condition_checks.csv", checks)

    audit = {
        "article": "Second Derivatives, Curvature, and Acceleration",
        "advanced_standard": True,
        "topics": [
            "twice_differentiability",
            "acceleration",
            "concavity",
            "curvature",
            "inflection_review",
            "second_order_approximation",
            "critical_point_classification",
            "finite_difference_stability",
            "noise_sensitivity"
        ],
        "condition_failures": failures,
        "warnings": [
            "Second derivative claims require stronger smoothness assumptions than first derivative claims.",
            "Inflection requires concavity sign change, not only f''=0.",
            "Numerical second derivatives amplify noise.",
            "Finite-difference step size and smoothing assumptions must be documented.",
            "Curvature should not be overread as tipping-point evidence without structural support."
        ]
    }

    write_json(json_dir / "advanced_second_derivative_audit.json", audit)

    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "advanced_second_derivative_audit.md").write_text(
        "# Advanced Mathematical Audit: Second Derivatives, Curvature, and Acceleration\n\n"
        "## Formal topics included\n\n"
        "- Twice differentiability\n"
        "- Acceleration and change in rate\n"
        "- Concavity and curvature\n"
        "- Inflection candidate review\n"
        "- Second-order approximation\n"
        "- Critical-point interpretation\n"
        "- Finite-difference stability\n"
        "- Noise and smoothing warnings\n\n"
        "## Modeling implication\n\n"
        "A second-derivative result should state the function or trajectory, operating point, first derivative, second derivative, curvature interpretation, finite-difference method, smoothing assumptions, and noise warnings.\n",
        encoding="utf-8"
    )

    print("Advanced second-derivative audit generated.")


if __name__ == "__main__":
    main()
