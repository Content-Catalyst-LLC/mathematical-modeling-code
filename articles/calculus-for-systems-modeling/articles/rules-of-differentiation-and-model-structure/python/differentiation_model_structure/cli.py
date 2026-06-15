from __future__ import annotations

import argparse
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE_ROOT))

from differentiation_model_structure.core import structural_audit, to_dicts, write_csv, write_json


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()

    rows = structural_audit([0.0, 5.0, 10.0, 20.0])
    row_dicts = to_dicts(rows)
    write_csv(args.output_dir / "tables" / "structural_derivative_audit.csv", row_dicts)

    counts: dict[str, int] = {}
    for row in row_dicts:
        counts[str(row["rule"])] = counts.get(str(row["rule"]), 0) + 1

    write_json(args.output_dir / "json" / "differentiation_rule_manifest.json", {
        "article": "Rules of Differentiation and Model Structure",
        "advanced_standard": True,
        "rules": sorted(counts.keys()),
        "counts_by_rule": counts,
        "warning": "Differentiation rules expose model structure but do not prove causal interpretation."
    })

    (args.output_dir / "logs").mkdir(parents=True, exist_ok=True)
    (args.output_dir / "logs" / "python_workflow.log").write_text("Structural derivative audit completed.\n", encoding="utf-8")
    print("Structural derivative audit complete.")


if __name__ == "__main__":
    main()
