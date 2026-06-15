from pathlib import Path
import sys

CURRENT = Path(__file__).resolve()
ADVANCED_DIR = CURRENT.parents[1]
sys.path.insert(0, str(CURRENT.parent))

from advanced_rule_structure import sample_checks, to_dicts, write_csv, write_json


def main() -> None:
    out = ADVANCED_DIR / "outputs"
    table_dir = out / "tables"
    report_dir = out / "reports"
    json_dir = out / "json"

    checks = to_dicts(sample_checks())
    failures = [row for row in checks if not row["passed"]]
    write_csv(table_dir / "advanced_rule_condition_checks.csv", checks)

    audit = {
        "article": "Rules of Differentiation and Model Structure",
        "advanced_standard": True,
        "topics": [
            "linearity",
            "product_rule_as_leibniz_rule",
            "quotient_denominator_conditions",
            "chain_rule_composition",
            "implicit_regular_conditions",
            "logarithmic_positivity_conditions",
            "automatic_differentiation_warning"
        ],
        "condition_failures": failures,
        "warnings": [
            "Structural derivative decomposition is not the same as causal attribution.",
            "The quotient rule requires nonzero denominators.",
            "The chain rule requires differentiable links.",
            "Implicit differentiation requires regularity conditions.",
            "Logarithmic differentiation requires positivity."
        ]
    }
    write_json(json_dir / "advanced_rule_structure_audit.json", audit)

    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "advanced_rule_structure_audit.md").write_text(
        "# Advanced Mathematical Audit: Rules of Differentiation and Model Structure\n\n"
        "## Formal topics included\n\n"
        "- Derivative operator linearity\n"
        "- Product rule as Leibniz rule\n"
        "- Quotient rule denominator conditions\n"
        "- Chain rule as composition of local linear maps\n"
        "- Implicit differentiation regularity conditions\n"
        "- Logarithmic differentiation positivity conditions\n\n"
        "## Modeling implication\n\n"
        "Differentiation rules expose how a model is assembled, but they do not by themselves prove causal structure, empirical validity, or domain appropriateness.\n",
        encoding="utf-8"
    )
    print("Advanced rule-structure audit generated.")


if __name__ == "__main__":
    main()
