from pathlib import Path
import sys

CURRENT = Path(__file__).resolve()
ADVANCED_DIR = CURRENT.parents[1]
sys.path.insert(0, str(CURRENT.parent))

from advanced_definite_integrals import sample_checks, to_dicts, write_csv, write_json


def main() -> None:
    out = ADVANCED_DIR / "outputs"
    table_dir = out / "tables"
    report_dir = out / "reports"
    json_dir = out / "json"

    checks = to_dicts(sample_checks())
    failures = [row for row in checks if not row["passed"]]

    write_csv(table_dir / "advanced_definite_integral_condition_checks.csv", checks)

    audit = {
        "article": "Definite Integrals and Total Change",
        "advanced_standard": True,
        "topics": [
            "definite_integral",
            "riemann_sum",
            "signed_accumulation",
            "absolute_accumulation",
            "net_change",
            "total_activity",
            "interval_bounds",
            "unit_consistency",
            "numerical_method_review"
        ],
        "condition_failures": failures,
        "warnings": [
            "A definite integral is interval-specific.",
            "Signed accumulation may hide large offsetting activity.",
            "Unit mismatch invalidates total-change interpretation.",
            "Coarse numerical grids can miss spikes, discontinuities, or bursts.",
            "Cumulative estimates require integrand, bounds, sign convention, units, and method documentation."
        ]
    }

    write_json(json_dir / "advanced_definite_integral_audit.json", audit)

    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "advanced_definite_integral_audit.md").write_text(
        "# Advanced Mathematical Audit: Definite Integrals and Total Change\n\n"
        "## Formal topics included\n\n"
        "- Definite integrals\n"
        "- Riemann sums\n"
        "- Signed accumulation\n"
        "- Net change\n"
        "- Total activity through absolute accumulation\n"
        "- Interval bounds and orientation\n"
        "- Unit consistency\n"
        "- Numerical method and grid review\n\n"
        "## Modeling implication\n\n"
        "A total-change estimate should state the integrand, bounds, integration variable, sign convention, units, numerical method, grid, and uncertainty.\n",
        encoding="utf-8"
    )

    print("Advanced definite-integral audit generated.")


if __name__ == "__main__":
    main()
