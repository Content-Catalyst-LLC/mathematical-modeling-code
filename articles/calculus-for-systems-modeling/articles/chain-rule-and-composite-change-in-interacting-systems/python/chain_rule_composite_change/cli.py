from __future__ import annotations

import argparse
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE_ROOT))

from chain_rule_composite_change.core import chain_rule_audits, to_dicts, write_csv, write_json


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()

    rows = chain_rule_audits([0.0, 5.0, 10.0, 20.0, 40.0])
    row_dicts = to_dicts(rows)

    write_csv(args.output_dir / "tables" / "chain_rule_pathway_audit.csv", row_dicts)

    write_json(args.output_dir / "json" / "chain_rule_manifest.json", {
        "article": "The Chain Rule and Composite Change in Interacting Systems",
        "advanced_standard": True,
        "diagnostics": ["local_sensitivity_records", "chain_rule_product", "finite_difference_check", "pathway_warning"],
        "warning": "A chain-rule derivative is a local pathway claim and should not be treated as global or causal without additional evidence."
    })

    (args.output_dir / "logs").mkdir(parents=True, exist_ok=True)
    (args.output_dir / "logs" / "python_workflow.log").write_text("Chain-rule pathway audit completed.\n", encoding="utf-8")
    print("Chain-rule pathway audit complete.")


if __name__ == "__main__":
    main()
