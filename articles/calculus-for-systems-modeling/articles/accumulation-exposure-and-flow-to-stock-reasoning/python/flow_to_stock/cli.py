from __future__ import annotations

import argparse
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE_ROOT))

from flow_to_stock.core import audit_flow_to_stock, sample_records, to_dicts, write_csv, write_json


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()

    records = sample_records()
    audit = audit_flow_to_stock(50.0, records)

    write_csv(args.output_dir / "tables" / "flow_to_stock_records.csv", to_dicts(records))
    write_csv(args.output_dir / "tables" / "flow_to_stock_audit.csv", to_dicts([audit]))

    manifest = {
        "article": "Accumulation, Exposure, and Flow-to-Stock Reasoning",
        "advanced_standard": True,
        "initial_stock": audit.initial_stock,
        "ending_stock": audit.ending_stock,
        "net_accumulation": audit.net_accumulation,
        "cumulative_exposure": audit.cumulative_exposure,
        "population_weighted_exposure": audit.population_weighted_exposure,
        "gross_activity": audit.gross_activity,
        "diagnostics": [
            "initial_condition",
            "net_flow",
            "gross_flows",
            "exposure_window",
            "unit_consistency",
            "measurement_window",
            "gross_vs_net_activity"
        ],
        "warning": "Net stock change should not be confused with gross activity, cumulative exposure, or modeled consequence."
    }

    write_json(args.output_dir / "json" / "flow_to_stock_manifest.json", manifest)

    (args.output_dir / "logs").mkdir(parents=True, exist_ok=True)
    (args.output_dir / "logs" / "python_workflow.log").write_text("Flow-to-stock audit completed.\n", encoding="utf-8")
    print("Flow-to-stock audit complete.")


if __name__ == "__main__":
    main()
