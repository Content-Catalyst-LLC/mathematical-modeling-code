from pathlib import Path
import sys

CURRENT = Path(__file__).resolve()
ADVANCED_DIR = CURRENT.parents[1]
sys.path.insert(0, str(CURRENT.parent))

from advanced_inverse import sample_checks, to_dicts, write_csv, write_json


def main() -> None:
    out = ADVANCED_DIR / "outputs"
    table_dir = out / "tables"
    report_dir = out / "reports"
    json_dir = out / "json"

    checks = to_dicts(sample_checks())
    failures = [row for row in checks if not row["passed"]]

    write_csv(table_dir / "advanced_inverse_condition_checks.csv", checks)

    audit = {
        "article": "Inverse Functions and System Interpretation",
        "advanced_standard": True,
        "topics": [
            "injectivity",
            "domain_codomain_image",
            "inverse_derivative_formula",
            "inverse_function_theorem",
            "local_global_inverse_distinction",
            "identifiability",
            "conditioning",
            "branch_selection"
        ],
        "condition_failures": failures,
        "warnings": [
            "Inverse claims must specify domain and branch.",
            "A local inverse is not automatically global.",
            "A recovered input is not automatically the true cause.",
            "Small forward derivatives amplify inverse uncertainty.",
            "Ill-conditioned Jacobians weaken recoverability and interpretation."
        ]
    }

    write_json(json_dir / "advanced_inverse_audit.json", audit)

    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "advanced_inverse_audit.md").write_text(
        "# Advanced Mathematical Audit: Inverse Functions and System Interpretation\n\n"
        "## Formal topics included\n\n"
        "- Injectivity and domain restriction\n"
        "- Image and codomain distinctions\n"
        "- Inverse derivative formula\n"
        "- Inverse function theorem\n"
        "- Local versus global inversion\n"
        "- Identifiability and practical recoverability\n"
        "- Conditioning and branch selection\n\n"
        "## Modeling implication\n\n"
        "An inverse interpretation should state the forward model, admissible domain, selected branch, forward consistency check, derivative or Jacobian regularity, conditioning status, and uncertainty limits.\n",
        encoding="utf-8"
    )

    print("Advanced inverse-function audit generated.")


if __name__ == "__main__":
    main()
