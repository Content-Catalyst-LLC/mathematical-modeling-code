from pathlib import Path
import sys

CURRENT = Path(__file__).resolve()
ADVANCED_DIR = CURRENT.parents[1]
sys.path.insert(0, str(CURRENT.parent))

from advanced_elasticity_sensitivity import sample_checks, to_dicts, write_csv, write_json


def main() -> None:
    out = ADVANCED_DIR / "outputs"
    table_dir = out / "tables"
    report_dir = out / "reports"
    json_dir = out / "json"

    checks = to_dicts(sample_checks())
    failures = [row for row in checks if not row["passed"]]

    write_csv(table_dir / "advanced_elasticity_sensitivity_condition_checks.csv", checks)

    audit = {
        "article": "Elasticity, Sensitivity, and Marginal Response",
        "advanced_standard": True,
        "topics": [
            "marginal_response",
            "point_elasticity",
            "normalized_sensitivity",
            "log_derivative_identity",
            "local_global_distinction",
            "near_zero_domain_warning",
            "finite_difference_stability",
            "parameter_range_review"
        ],
        "condition_failures": failures,
        "warnings": [
            "Elasticity is undefined or fragile near zero input or output.",
            "Log-derivative interpretation requires positive quantities.",
            "Local sensitivity should not be generalized globally without evidence.",
            "Numerical sensitivity depends on perturbation size.",
            "Sensitivity is not causal proof without a causal design or mechanism."
        ]
    }

    write_json(json_dir / "advanced_elasticity_sensitivity_audit.json", audit)

    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "advanced_elasticity_sensitivity_audit.md").write_text(
        "# Advanced Mathematical Audit: Elasticity, Sensitivity, and Marginal Response\n\n"
        "## Formal topics included\n\n"
        "- Marginal response\n"
        "- Point elasticity\n"
        "- Normalized parameter sensitivity\n"
        "- Log-derivative identity\n"
        "- Local versus global sensitivity\n"
        "- Near-zero and sign-change warnings\n"
        "- Finite-difference stability\n"
        "- Parameter range review\n\n"
        "## Modeling implication\n\n"
        "A sensitivity result should state the baseline, operating point, units, perturbation size, parameter range, local/global scope, and domain restrictions.\n",
        encoding="utf-8"
    )

    print("Advanced elasticity/sensitivity audit generated.")


if __name__ == "__main__":
    main()
