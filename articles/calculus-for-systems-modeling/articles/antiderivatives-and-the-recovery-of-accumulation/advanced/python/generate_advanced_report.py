from pathlib import Path
import sys

CURRENT = Path(__file__).resolve()
ADVANCED_DIR = CURRENT.parents[1]
sys.path.insert(0, str(CURRENT.parent))

from advanced_antiderivative_recovery import sample_checks, to_dicts, write_csv, write_json


def main() -> None:
    out = ADVANCED_DIR / "outputs"
    table_dir = out / "tables"
    report_dir = out / "reports"
    json_dir = out / "json"

    checks = to_dicts(sample_checks())
    failures = [row for row in checks if not row["passed"]]

    write_csv(table_dir / "advanced_antiderivative_recovery_condition_checks.csv", checks)

    audit = {
        "article": "Antiderivatives and the Recovery of Accumulation",
        "advanced_standard": True,
        "topics": [
            "antiderivative_family",
            "constant_of_integration",
            "initial_condition",
            "flow_to_stock_recovery",
            "marginal_to_total_recovery",
            "unit_consistency",
            "numerical_accumulation",
            "domain_interval_review",
            "missing_flow_review"
        ],
        "condition_failures": failures,
        "warnings": [
            "A rate function determines a family of possible accumulated quantities, not a unique state.",
            "Initial conditions select recovered trajectories.",
            "Unit mismatch invalidates accumulation.",
            "Numerical accumulation depends on time step and method.",
            "Missing inflows or outflows can produce false stock recovery."
        ]
    }

    write_json(json_dir / "advanced_antiderivative_recovery_audit.json", audit)

    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "advanced_antiderivative_recovery_audit.md").write_text(
        "# Advanced Mathematical Audit: Antiderivatives and the Recovery of Accumulation\n\n"
        "## Formal topics included\n\n"
        "- Antiderivative families\n"
        "- Constants of integration\n"
        "- Initial conditions\n"
        "- Flow-to-stock recovery\n"
        "- Marginal-to-total recovery\n"
        "- Unit consistency\n"
        "- Numerical accumulation\n"
        "- Missing-flow review\n"
        "- Domain interval review\n\n"
        "## Modeling implication\n\n"
        "A recovered accumulation should state the rate definition, baseline, interval, integration variable, numerical method, units, and missing-flow assumptions.\n",
        encoding="utf-8"
    )

    print("Advanced antiderivative recovery audit generated.")


if __name__ == "__main__":
    main()
