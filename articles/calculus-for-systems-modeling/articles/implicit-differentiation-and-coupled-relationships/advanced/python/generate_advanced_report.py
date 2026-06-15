from pathlib import Path
import sys

CURRENT = Path(__file__).resolve()
ADVANCED_DIR = CURRENT.parents[1]
sys.path.insert(0, str(CURRENT.parent))

from advanced_implicit import sample_checks, to_dicts, write_csv, write_json


def main() -> None:
    out = ADVANCED_DIR / "outputs"
    table_dir = out / "tables"
    report_dir = out / "reports"
    json_dir = out / "json"

    checks = to_dicts(sample_checks())
    failures = [row for row in checks if not row["passed"]]

    write_csv(table_dir / "advanced_implicit_condition_checks.csv", checks)

    audit = {
        "article": "Implicit Differentiation and Coupled Relationships",
        "advanced_standard": True,
        "topics": [
            "implicit_relation",
            "local_branch",
            "total_differential",
            "implicit_function_theorem",
            "regularity_condition",
            "equilibrium_sensitivity",
            "jacobian_conditioning",
            "singular_cases"
        ],
        "condition_failures": failures,
        "warnings": [
            "Implicit derivatives are local and branch-specific.",
            "The relationship held fixed must be stated.",
            "Regularity requires a nonzero partial derivative or invertible Jacobian block.",
            "Ill-conditioned Jacobians can make sensitivity unreliable.",
            "Co-adjustment is not the same as independent causal response."
        ]
    }

    write_json(json_dir / "advanced_implicit_audit.json", audit)

    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "advanced_implicit_audit.md").write_text(
        "# Advanced Mathematical Audit: Implicit Differentiation and Coupled Relationships\n\n"
        "## Formal topics included\n\n"
        "- Implicit relations and local branches\n"
        "- Total differentials and tangent directions\n"
        "- Implicit function theorem\n"
        "- Regularity conditions\n"
        "- Equilibrium sensitivity\n"
        "- Jacobian conditioning\n"
        "- Singular cases and loss of local solvability\n\n"
        "## Modeling implication\n\n"
        "An implicit derivative should state the constraint, branch, regularity condition, conditioning status, and the interpretation of the derivative as local co-adjustment under a coupled relationship.\n",
        encoding="utf-8"
    )

    print("Advanced implicit differentiation audit generated.")


if __name__ == "__main__":
    main()
