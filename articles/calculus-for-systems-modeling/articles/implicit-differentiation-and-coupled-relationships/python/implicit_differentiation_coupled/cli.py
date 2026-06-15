from __future__ import annotations

import argparse
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE_ROOT))

from implicit_differentiation_coupled.core import implicit_audits, to_dicts, write_csv, write_json


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()

    rows = implicit_audits([-3.0, -1.0, 0.0, 1.0, 3.0])
    row_dicts = to_dicts(rows)

    write_csv(args.output_dir / "tables" / "implicit_sensitivity_audit.csv", row_dicts)

    write_json(args.output_dir / "json" / "implicit_relationship_manifest.json", {
        "article": "Implicit Differentiation and Coupled Relationships",
        "advanced_standard": True,
        "diagnostics": ["constraint_residual", "regularity_condition", "implicit_sensitivity", "finite_difference_check", "conditioning_warning"],
        "warning": "Implicit derivatives describe local co-adjustment under a stated relationship, not unconstrained causal response."
    })

    (args.output_dir / "logs").mkdir(parents=True, exist_ok=True)
    (args.output_dir / "logs" / "python_workflow.log").write_text("Implicit sensitivity audit completed.\n", encoding="utf-8")
    print("Implicit sensitivity audit complete.")


if __name__ == "__main__":
    main()
