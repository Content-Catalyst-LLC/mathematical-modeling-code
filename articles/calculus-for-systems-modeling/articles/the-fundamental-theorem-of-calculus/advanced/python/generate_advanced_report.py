from pathlib import Path
import sys

CURRENT = Path(__file__).resolve()
ADVANCED_DIR = CURRENT.parents[1]
sys.path.insert(0, str(CURRENT.parent))

from advanced_fundamental_theorem import sample_checks, to_dicts, write_csv, write_json


def main() -> None:
    out = ADVANCED_DIR / "outputs"
    table_dir = out / "tables"
    report_dir = out / "reports"
    json_dir = out / "json"

    checks = to_dicts(sample_checks())
    failures = [row for row in checks if not row["passed"]]

    write_csv(table_dir / "advanced_fundamental_theorem_condition_checks.csv", checks)

    audit = {
        "article": "The Fundamental Theorem of Calculus",
        "advanced_standard": True,
        "topics": [
            "ftc_part_i",
            "ftc_part_ii",
            "accumulation_function",
            "endpoint_difference",
            "rate_state_reconciliation",
            "baseline_state",
            "unit_consistency",
            "numerical_residual",
            "tolerance_review"
        ],
        "condition_failures": failures,
        "warnings": [
            "FTC Part I needs continuity or more advanced hypotheses for pointwise recovery.",
            "Endpoint difference gives net change, not full trajectory history.",
            "Rate-state reconciliation requires shared interval and units.",
            "Numerical residuals require tolerance and grid documentation.",
            "Endpoint agreement is not causal proof by itself."
        ]
    }

    write_json(json_dir / "advanced_fundamental_theorem_audit.json", audit)

    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "advanced_fundamental_theorem_audit.md").write_text(
        "# Advanced Mathematical Audit: The Fundamental Theorem of Calculus\n\n"
        "## Formal topics included\n\n"
        "- FTC Part I\n"
        "- FTC Part II\n"
        "- Accumulation functions\n"
        "- Endpoint differences\n"
        "- Rate-state reconciliation\n"
        "- Baseline state review\n"
        "- Unit consistency\n"
        "- Numerical residual and tolerance checks\n\n"
        "## Modeling implication\n\n"
        "If a model asserts Q'(t)=r(t), the accumulated rate and endpoint difference should reconcile within documented numerical, measurement, and modeling tolerance.\n",
        encoding="utf-8"
    )

    print("Advanced Fundamental Theorem audit generated.")


if __name__ == "__main__":
    main()
