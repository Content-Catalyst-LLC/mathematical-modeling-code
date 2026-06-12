from __future__ import annotations

import argparse
from dataclasses import asdict
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from spatial_models_geometric_representation.core import (
    accessibility_rows,
    build_spatial_audit_card,
    load_locations,
    load_records,
    spatial_risk_score,
    write_csv,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the spatial model and geometric representation workflow.")
    parser.add_argument("--location-file", type=Path, default=Path("data/spatial_locations.csv"))
    parser.add_argument("--register-file", type=Path, default=Path("data/spatial_model_register.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tables_dir = args.output_dir / "tables"
    json_dir = args.output_dir / "json"

    locations = load_locations(args.location_file)
    records = load_records(args.register_file)
    access = accessibility_rows(locations)

    register_rows = [
        {**asdict(record), "spatial_risk_score": spatial_risk_score(record)}
        for record in records
    ]

    summary_rows = [{
        "location_count": len(locations),
        "demand_location_count": sum(1 for location in locations if location.kind == "demand"),
        "service_location_count": sum(1 for location in locations if location.kind == "service"),
        "mean_accessibility_score": round(sum(float(row["accessibility_score"]) for row in access) / len(access), 8),
        "max_low_access_exposure_score": round(max(float(row["low_access_exposure_score"]) for row in access), 8),
    }]

    write_csv(tables_dir / "spatial_model_register.csv", register_rows)
    write_csv(tables_dir / "spatial_locations.csv", [asdict(item) for item in locations])
    write_csv(tables_dir / "spatial_accessibility_diagnostics.csv", access)
    write_csv(tables_dir / "spatial_summary.csv", summary_rows)
    write_json(json_dir / "spatial_model_audit_card.json", build_spatial_audit_card(records, locations, access))

    print("Spatial models and geometric representation workflow complete.")
    print(f"Spatial records: {len(records)}")
    print(f"Locations: {len(locations)}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
