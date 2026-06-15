from __future__ import annotations

import argparse
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE_ROOT))

from substitution_accumulation.core import audit_substitution, to_dicts, write_csv, write_json


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()

    record = audit_substitution(1.0, 3.0, 400)
    write_csv(args.output_dir / "tables" / "substitution_audit.csv", to_dicts([record]))

    manifest = {
        "article": "Substitution and Transformations of Accumulation",
        "advanced_standard": True,
        "original_interval": [record.original_start, record.original_end],
        "transformed_interval": [record.transformed_start, record.transformed_end],
        "direct_integral": record.direct_integral,
        "transformed_integral": record.transformed_integral,
        "residual": record.residual,
        "diagnostics": [
            "original_variable",
            "transformed_variable",
            "scale_factor",
            "transformed_bounds",
            "unit_check",
            "orientation_review",
            "monotonicity_review"
        ],
        "warning": "Transformed accumulation should preserve the same quantity only when scale factors, bounds, units, and orientation are handled correctly."
    }

    write_json(args.output_dir / "json" / "substitution_manifest.json", manifest)

    (args.output_dir / "logs").mkdir(parents=True, exist_ok=True)
    (args.output_dir / "logs" / "python_workflow.log").write_text("Substitution audit completed.\n", encoding="utf-8")
    print("Substitution audit complete.")


if __name__ == "__main__":
    main()
