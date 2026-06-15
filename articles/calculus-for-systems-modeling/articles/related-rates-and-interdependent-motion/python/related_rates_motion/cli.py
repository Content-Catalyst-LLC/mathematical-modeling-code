from __future__ import annotations

import argparse
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE_ROOT))

from related_rates_motion.core import related_rate_audits, to_dicts, write_csv, write_json


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()

    rows = related_rate_audits([0.0, 5.0, 10.0, 20.0, 40.0])
    row_dicts = to_dicts(rows)

    write_csv(args.output_dir / "tables" / "related_rates_audit.csv", row_dicts)

    write_json(args.output_dir / "json" / "related_rates_manifest.json", {
        "article": "Related Rates and Interdependent Motion",
        "advanced_standard": True,
        "diagnostics": ["driving_rate", "structural_derivative", "inferred_target_rate", "finite_difference_check", "unit_review"],
        "warning": "A related-rates result is local to a relationship, operating point, and driving rate."
    })

    (args.output_dir / "logs").mkdir(parents=True, exist_ok=True)
    (args.output_dir / "logs" / "python_workflow.log").write_text("Related-rates audit completed.\n", encoding="utf-8")
    print("Related-rates audit complete.")


if __name__ == "__main__":
    main()
