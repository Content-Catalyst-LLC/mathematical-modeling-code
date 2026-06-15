from pathlib import Path
import sys

CURRENT = Path(__file__).resolve()
ADVANCED_DIR = CURRENT.parents[1]
sys.path.insert(0, str(CURRENT.parent))

from advanced_substitution import sample_checks, to_dicts, write_csv, write_json


def main() -> None:
    out = ADVANCED_DIR / "outputs"
    table_dir = out / "tables"
    report_dir = out / "reports"
    json_dir = out / "json"

    checks = to_dicts(sample_checks())
    failures = [row for row in checks if not row["passed"]]

    write_csv(table_dir / "advanced_substitution_condition_checks.csv", checks)

    audit = {
        "article": "Substitution and Transformations of Accumulation",
        "advanced_standard": True,
        "topics": [
            "change_of_variables",
            "scale_factor",
            "transformed_bounds",
            "differential_meaning",
            "unit_consistency",
            "orientation",
            "monotonicity",
            "density_transformation",
            "residual_diagnostics"
        ],
        "condition_failures": failures,
        "warnings": [
            "Omitting the scale factor usually changes the accumulated quantity.",
            "Keeping old bounds after changing variables mixes incompatible intervals.",
            "Nonmonotonic transformations may require piecewise treatment.",
            "Signed rates and nonnegative densities require different orientation conventions.",
            "Transformed accumulation should be audited against the original representation when possible."
        ]
    }

    write_json(json_dir / "advanced_substitution_audit.json", audit)

    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "advanced_substitution_audit.md").write_text(
        "# Advanced Mathematical Audit: Substitution and Transformations of Accumulation\n\n"
        "## Formal topics included\n\n"
        "- Change of variables\n"
        "- Differential scale factors\n"
        "- Transformed bounds\n"
        "- Chain-rule structure\n"
        "- Unit consistency\n"
        "- Orientation and monotonicity\n"
        "- Density transformations\n"
        "- Direct-versus-transformed residual checks\n\n"
        "## Modeling implication\n\n"
        "A transformed integral should preserve the same accumulated quantity by documenting the original variable, transformed variable, mapping, scale factor, bounds, units, orientation, and interpretation.\n",
        encoding="utf-8"
    )

    print("Advanced substitution audit generated.")


if __name__ == "__main__":
    main()
