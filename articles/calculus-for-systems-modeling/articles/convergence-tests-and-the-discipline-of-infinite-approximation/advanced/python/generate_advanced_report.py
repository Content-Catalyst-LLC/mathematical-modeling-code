from pathlib import Path
import sys

CURRENT = Path(__file__).resolve()
ADVANCED_DIR = CURRENT.parents[1]
sys.path.insert(0, str(CURRENT.parent))

from advanced_convergence_tests import sample_checks, to_dicts, write_csv, write_json


def main() -> None:
    out = ADVANCED_DIR / "outputs"
    table_dir = out / "tables"
    report_dir = out / "reports"
    json_dir = out / "json"

    checks = to_dicts(sample_checks())
    failures = [row for row in checks if not row["passed"]]

    write_csv(table_dir / "advanced_convergence_test_condition_checks.csv", checks)

    audit = {
        "article": "Convergence Tests and the Discipline of Infinite Approximation",
        "advanced_standard": True,
        "topics": [
            "term_test",
            "geometric_series",
            "p_series",
            "comparison_tests",
            "limit_comparison",
            "ratio_test",
            "root_test",
            "integral_test",
            "alternating_series_test",
            "absolute_vs_conditional_convergence",
            "remainder_bounds",
            "stopping_rules"
        ],
        "condition_failures": failures,
        "warnings": [
            "Terms going to zero does not prove convergence.",
            "A finite partial sum is not an infinite total.",
            "Ratio and root tests can be inconclusive.",
            "Conditional convergence may hide large gross activity.",
            "A correct test used under false conditions gives misleading confidence."
        ]
    }

    write_json(json_dir / "advanced_convergence_test_audit.json", audit)

    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "advanced_convergence_test_audit.md").write_text(
        "# Advanced Mathematical Audit: Convergence Tests and Infinite Approximation\n\n"
        "## Formal topics included\n\n"
        "- Term test\n"
        "- Geometric and p-series tests\n"
        "- Comparison and limit comparison\n"
        "- Ratio and root tests\n"
        "- Integral test tail bounds\n"
        "- Alternating-series error estimates\n"
        "- Absolute and conditional convergence\n"
        "- Remainders and stopping rules\n\n"
        "## Modeling implication\n\n"
        "A responsible convergence-test workflow should identify the selected test, verify its conditions, report the finite partial sum, state the stopping rule, estimate the remainder where possible, and limit the claim when evidence is inconclusive.\n",
        encoding="utf-8"
    )

    print("Advanced convergence-test audit generated.")


if __name__ == "__main__":
    main()
