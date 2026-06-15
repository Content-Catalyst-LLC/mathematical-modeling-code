from pathlib import Path
import sys

CURRENT = Path(__file__).resolve()
ADVANCED_DIR = CURRENT.parents[1]
sys.path.insert(0, str(CURRENT.parent))

from advanced_convergence import sample_checks, to_dicts, write_csv, write_json


def main() -> None:
    out = ADVANCED_DIR / "outputs"
    table_dir = out / "tables"
    report_dir = out / "reports"
    json_dir = out / "json"

    checks = to_dicts(sample_checks())
    failures = [row for row in checks if not row["passed"]]

    write_csv(table_dir / "advanced_convergence_condition_checks.csv", checks)

    audit = {
        "article": "Sequences, Series, and the Logic of Convergence",
        "advanced_standard": True,
        "topics": [
            "sequence_definition",
            "series_as_partial_sum_limit",
            "geometric_series",
            "harmonic_series_warning",
            "p_series_classification",
            "stopping_rule",
            "remainder_bound",
            "absolute_vs_conditional_convergence"
        ],
        "condition_failures": failures,
        "warnings": [
            "A stopped computation is not automatically a converged computation.",
            "Small latest terms do not always imply small tails.",
            "A finite partial sum is not an infinite series.",
            "Conditional convergence may hide large gross activity.",
            "Stable-looking early terms can conceal slow divergence."
        ]
    }

    write_json(json_dir / "advanced_convergence_audit.json", audit)

    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "advanced_convergence_audit.md").write_text(
        "# Advanced Mathematical Audit: Sequences, Series, and the Logic of Convergence\n\n"
        "## Formal topics included\n\n"
        "- Sequence limits\n"
        "- Series as limits of partial sums\n"
        "- Geometric convergence\n"
        "- Harmonic divergence\n"
        "- p-series classification\n"
        "- Stopping rules\n"
        "- Remainder bounds\n"
        "- Absolute and conditional convergence\n\n"
        "## Modeling implication\n\n"
        "A responsible convergence workflow should define the sequence or series, state the number of terms or iterations, report partial sums, classify convergence when possible, document the stopping rule, and distinguish finite computation from an infinite limiting claim.\n",
        encoding="utf-8"
    )

    print("Advanced convergence audit generated.")


if __name__ == "__main__":
    main()
