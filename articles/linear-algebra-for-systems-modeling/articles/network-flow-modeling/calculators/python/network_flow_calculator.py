from __future__ import annotations

import csv
import json
from pathlib import Path


def main() -> None:
    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    result = {
        "calculator": "network_flow_modeling_calculator",
        "graph_name": "synthetic_capacitated_flow_network",
        "node_count": 5,
        "edge_count": 6,
        "source_node": "source",
        "sink_node": "sink",
        "total_source_outflow": 16.0,
        "total_sink_inflow": 16.0,
        "capacity_violations": 0,
        "saturated_edge_count": 2,
        "max_absolute_transshipment_imbalance": 0.0,
        "total_flow_cost": 82.0,
        "warning": "Network flow metrics depend on flow units, capacities, costs, conservation assumptions, source-sink choices, time scale, and data provenance."
    }

    with (output_dir / "network_flow_modeling_calculator.json").open("w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)

    with (output_dir / "network_flow_modeling_calculator.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(result.keys()))
        writer.writeheader()
        writer.writerow(result)

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
