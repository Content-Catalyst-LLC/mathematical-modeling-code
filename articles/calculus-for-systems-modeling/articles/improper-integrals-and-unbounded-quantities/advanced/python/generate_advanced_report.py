from pathlib import Path
import sys

CURRENT = Path(__file__).resolve()
ADVANCED_DIR = CURRENT.parents[1]
sys.path.insert(0, str(CURRENT.parent))

from advanced_improper_integrals import sample_checks, to_dicts, write_csv, write_json


def main() -> None:
    out = ADVANCED_DIR / "outputs"
    table_dir = out / "tables"
    report_dir = out / "reports"
    json_dir = out / "json"

    checks = to_dicts(sample_checks())
    failures = [row for row in checks if not row["passed"]]

    write_csv(table_dir / "advanced_improper_integral_condition_checks.csv", checks)

    audit = {
        "article": "Improper Integrals and Unbounded Quantities",
        "advanced_standard": True,
        "topics": [
            "limiting_process",
            "infinite_interval",
            "singular_endpoint",
            "convergence",
            "divergence",
            "tail_behavior",
            "truncation_sensitivity",
            "model_validity_boundary"
        ],
        "condition_failures": failures,
        "warnings": [
            "A finite cutoff is not an infinite-horizon result.",
            "A rate approaching zero may still diverge.",
            "An unbounded integrand may still have finite accumulation.",
            "Numerical stability alone does not prove convergence.",
            "Mathematical limits can extend beyond credible model domain."
        ]
    }

    write_json(json_dir / "advanced_improper_integral_audit.json", audit)

    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "advanced_improper_integral_audit.md").write_text(
        "# Advanced Mathematical Audit: Improper Integrals and Unbounded Quantities\n\n"
        "## Formal topics included\n\n"
        "- Infinite intervals\n"
        "- Singular endpoints\n"
        "- Limiting processes\n"
        "- Convergence and divergence\n"
        "- Tail behavior\n"
        "- Truncation sensitivity\n"
        "- Comparison reasoning\n"
        "- Model-validity boundary review\n\n"
        "## Modeling implication\n\n"
        "A responsible improper-integral workflow should state the limiting process, convergence evidence, truncation cutoffs, tail estimates, unit meaning, numerical sensitivity, and model-validity boundary.\n",
        encoding="utf-8"
    )

    print("Advanced improper-integral audit generated.")


if __name__ == "__main__":
    main()
