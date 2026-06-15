from __future__ import annotations

import argparse
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE_ROOT))

from quotient_rule_relative_change.core import quotient_audits, to_dicts, write_csv, write_json


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()

    rows = quotient_audits([0.0, 5.0, 10.0, 20.0, 40.0])
    row_dicts = to_dicts(rows)

    write_csv(args.output_dir / "tables" / "quotient_rule_ratio_audit.csv", row_dicts)

    write_json(args.output_dir / "json" / "quotient_rule_manifest.json", {
        "article": "The Quotient Rule and Relative Change",
        "advanced_standard": True,
        "diagnostics": ["numerator_effect", "denominator_effect", "relative_rate_identity", "denominator_warning"],
        "warning": "Ratio indicators require denominator validity, positivity checks, and absolute as well as relative interpretation."
    })

    (args.output_dir / "logs").mkdir(parents=True, exist_ok=True)
    (args.output_dir / "logs" / "python_workflow.log").write_text("Quotient-rule audit completed.\n", encoding="utf-8")
    print("Quotient-rule audit complete.")


if __name__ == "__main__":
    main()
