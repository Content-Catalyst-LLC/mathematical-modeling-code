from pathlib import Path
import sys

CURRENT = Path(__file__).resolve()
ADVANCED_DIR = CURRENT.parents[1]
sys.path.insert(0, str(CURRENT.parent))

from advanced_quotient_rule import sample_checks, to_dicts, write_csv, write_json


def main() -> None:
    out = ADVANCED_DIR / "outputs"
    table_dir = out / "tables"
    report_dir = out / "reports"
    json_dir = out / "json"

    checks = to_dicts(sample_checks())
    failures = [row for row in checks if not row["passed"]]

    write_csv(table_dir / "advanced_quotient_condition_checks.csv", checks)

    audit = {
        "article": "The Quotient Rule and Relative Change",
        "advanced_standard": True,
        "topics": [
            "quotient_as_product_with_reciprocal",
            "nonzero_denominator_condition",
            "numerator_denominator_decomposition",
            "relative_rate_identity",
            "elasticity_of_ratio",
            "near_zero_denominator_instability",
            "indicator_validity"
        ],
        "condition_failures": failures,
        "warnings": [
            "A ratio is not automatically substantively meaningful.",
            "The denominator must be nonzero and meaningful.",
            "Near-zero denominators can dominate interpretation.",
            "Relative-rate interpretations require positivity.",
            "Ratio improvement can coexist with absolute deterioration."
        ]
    }

    write_json(json_dir / "advanced_quotient_rule_audit.json", audit)

    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "advanced_quotient_rule_audit.md").write_text(
        "# Advanced Mathematical Audit: The Quotient Rule and Relative Change\n\n"
        "## Formal topics included\n\n"
        "- Quotient as product with reciprocal\n"
        "- Nonzero denominator condition\n"
        "- Numerator and denominator effect decomposition\n"
        "- Relative-rate identity\n"
        "- Elasticity of a ratio\n"
        "- Near-zero denominator instability\n"
        "- Ratio indicator validity\n\n"
        "## Modeling implication\n\n"
        "A quotient-rule claim should state numerator, denominator, units, domain, positivity conditions, denominator reliability, and whether relative-rate interpretation is meaningful.\n",
        encoding="utf-8"
    )

    print("Advanced quotient-rule audit generated.")


if __name__ == "__main__":
    main()
