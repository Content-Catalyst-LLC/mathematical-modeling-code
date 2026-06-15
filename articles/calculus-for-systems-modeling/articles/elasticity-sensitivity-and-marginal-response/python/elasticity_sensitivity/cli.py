from __future__ import annotations

import argparse
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE_ROOT))

from elasticity_sensitivity.core import audits, to_dicts, write_csv, write_json


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()

    rows = audits([0.0, 0.5, 1.0, 4.0, 9.0, 24.0])
    row_dicts = to_dicts(rows)

    write_csv(args.output_dir / "tables" / "elasticity_sensitivity_audit.csv", row_dicts)

    write_json(args.output_dir / "json" / "elasticity_sensitivity_manifest.json", {
        "article": "Elasticity, Sensitivity, and Marginal Response",
        "advanced_standard": True,
        "diagnostics": [
            "marginal_response",
            "elasticity",
            "finite_difference_check",
            "near_zero_warning",
            "domain_warning",
            "baseline_record"
        ],
        "warning": "Sensitivity claims require baseline, units, perturbation size, local/global scope, and domain review."
    })

    (args.output_dir / "logs").mkdir(parents=True, exist_ok=True)
    (args.output_dir / "logs" / "python_workflow.log").write_text("Elasticity and sensitivity audit completed.\n", encoding="utf-8")
    print("Elasticity and sensitivity audit complete.")


if __name__ == "__main__":
    main()
