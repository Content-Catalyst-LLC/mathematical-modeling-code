from pathlib import Path
import sys

CURRENT = Path(__file__).resolve()
ADVANCED_DIR = CURRENT.parents[1]
sys.path.insert(0, str(CURRENT.parent))

from advanced_chain_rule import sample_checks, to_dicts, write_csv, write_json


def main() -> None:
    out = ADVANCED_DIR / "outputs"
    table_dir = out / "tables"
    report_dir = out / "reports"
    json_dir = out / "json"

    checks = to_dicts(sample_checks())
    failures = [row for row in checks if not row["passed"]]

    write_csv(table_dir / "advanced_chain_rule_condition_checks.csv", checks)

    audit = {
        "article": "The Chain Rule and Composite Change in Interacting Systems",
        "advanced_standard": True,
        "topics": [
            "composite_function",
            "derivative_as_local_linear_map",
            "domain_compatibility",
            "differentiable_links",
            "jacobian_composition",
            "feedback_direct_indirect_terms",
            "automatic_differentiation_warning"
        ],
        "condition_failures": failures,
        "warnings": [
            "A chain-rule derivative is local, not global.",
            "Every pathway link must be differentiable.",
            "The image of each inner function must lie in the next domain.",
            "Automatic differentiation differentiates implemented code.",
            "Pathway decomposition is not automatic causal proof."
        ]
    }

    write_json(json_dir / "advanced_chain_rule_audit.json", audit)

    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "advanced_chain_rule_audit.md").write_text(
        "# Advanced Mathematical Audit: The Chain Rule and Composite Change in Interacting Systems\n\n"
        "## Formal topics included\n\n"
        "- Composite functions and domain compatibility\n"
        "- Derivative as local linear map\n"
        "- Chain rule as composition of derivative maps\n"
        "- Jacobian composition\n"
        "- Feedback-mediated direct and indirect terms\n"
        "- Automatic-differentiation implementation warnings\n\n"
        "## Modeling implication\n\n"
        "A chain-rule claim should identify every pathway link, local derivative, domain condition, differentiability assumption, and whether the derivative describes a model, a program, or an empirically supported system pathway.\n",
        encoding="utf-8"
    )

    print("Advanced chain-rule audit generated.")


if __name__ == "__main__":
    main()
