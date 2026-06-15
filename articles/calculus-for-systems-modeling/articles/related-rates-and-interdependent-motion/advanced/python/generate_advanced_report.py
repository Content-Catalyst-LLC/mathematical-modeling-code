from pathlib import Path
import sys

CURRENT = Path(__file__).resolve()
ADVANCED_DIR = CURRENT.parents[1]
sys.path.insert(0, str(CURRENT.parent))

from advanced_related_rates import sample_checks, to_dicts, write_csv, write_json


def main() -> None:
    out = ADVANCED_DIR / "outputs"
    table_dir = out / "tables"
    report_dir = out / "reports"
    json_dir = out / "json"

    checks = to_dicts(sample_checks())
    failures = [row for row in checks if not row["passed"]]

    write_csv(table_dir / "advanced_related_rates_condition_checks.csv", checks)

    audit = {
        "article": "Related Rates and Interdependent Motion",
        "advanced_standard": True,
        "topics": [
            "time_parametrized_variables",
            "rate_propagation",
            "implicit_rate_coupling",
            "constraint_velocity",
            "tangent_space",
            "operating_point",
            "unit_review",
            "finite_difference_stability"
        ],
        "condition_failures": failures,
        "warnings": [
            "Related rates require a stated relationship.",
            "All time-dependent variables must be identified.",
            "Driving rate uncertainty propagates into inferred rates.",
            "Rate conversions are local to operating points.",
            "Noisy numerical differentiation can amplify measurement error."
        ]
    }

    write_json(json_dir / "advanced_related_rates_audit.json", audit)

    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "advanced_related_rates_audit.md").write_text(
        "# Advanced Mathematical Audit: Related Rates and Interdependent Motion\n\n"
        "## Formal topics included\n\n"
        "- Time-parametrized variables\n"
        "- Chain-rule rate propagation\n"
        "- Implicit rate coupling\n"
        "- Constraint velocity and tangent spaces\n"
        "- Operating-point locality\n"
        "- Unit review\n"
        "- Finite-difference stability\n\n"
        "## Modeling implication\n\n"
        "A related-rates result should state the relationship, changing variables, driving rate, operating point, target rate, units, and numerical stability warnings.\n",
        encoding="utf-8"
    )

    print("Advanced related-rates audit generated.")


if __name__ == "__main__":
    main()
