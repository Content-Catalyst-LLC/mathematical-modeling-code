from pathlib import Path
import sys

CURRENT = Path(__file__).resolve()
ADVANCED_DIR = CURRENT.parents[1]
sys.path.insert(0, str(CURRENT.parent))

from advanced_integration_by_parts import sample_checks, to_dicts, write_csv, write_json


def main() -> None:
    out = ADVANCED_DIR / "outputs"
    table_dir = out / "tables"
    report_dir = out / "reports"
    json_dir = out / "json"

    checks = to_dicts(sample_checks())
    failures = [row for row in checks if not row["passed"]]

    write_csv(table_dir / "advanced_integration_by_parts_condition_checks.csv", checks)

    audit = {
        "article": "Integration by Parts and Structured Decomposition",
        "advanced_standard": True,
        "topics": [
            "product_rule_origin",
            "choice_of_parts",
            "boundary_term",
            "residual_integral",
            "weighted_accumulation",
            "unit_consistency",
            "direct_vs_decomposed_residual",
            "causal_overclaim_review"
        ],
        "condition_failures": failures,
        "warnings": [
            "Integration by parts is an accounting identity, not causal proof.",
            "Boundary terms depend strongly on interval choice.",
            "Residual terms may be unstable when derivatives are estimated from noisy data.",
            "A valid algebraic decomposition may still lack system meaning.",
            "Direct and decomposed calculations should be compared when used computationally."
        ]
    }

    write_json(json_dir / "advanced_integration_by_parts_audit.json", audit)

    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "advanced_integration_by_parts_audit.md").write_text(
        "# Advanced Mathematical Audit: Integration by Parts and Structured Decomposition\n\n"
        "## Formal topics included\n\n"
        "- Product-rule origin\n"
        "- Boundary terms\n"
        "- Residual integrals\n"
        "- Choice of parts\n"
        "- Weighted accumulation\n"
        "- Unit consistency\n"
        "- Direct-versus-decomposed numerical residuals\n"
        "- Causal overclaim review\n\n"
        "## Modeling implication\n\n"
        "A useful integration-by-parts decomposition should report direct accumulation, boundary contribution, residual accumulation, decomposition residual, units, interval, numerical method, and interpretive purpose.\n",
        encoding="utf-8"
    )

    print("Advanced integration-by-parts audit generated.")


if __name__ == "__main__":
    main()
