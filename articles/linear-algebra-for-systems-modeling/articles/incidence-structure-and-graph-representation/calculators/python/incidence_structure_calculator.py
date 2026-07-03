from __future__ import annotations

import csv
import json
from pathlib import Path


def main() -> None:
    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    result = {
        "calculator": "incidence_structure_calculator",
        "graph_name": "synthetic_infrastructure_incidence_graph",
        "node_count": 4,
        "edge_count": 5,
        "signed_incidence": True,
        "nonzero_incidence_entries": 10,
        "incidence_density": 0.5,
        "max_absolute_node_balance": 9.0,
        "laplacian_trace": 10.0,
        "rank_estimate": 3,
        "warning": "Incidence metrics depend on node definitions, edge definitions, sign conventions, weights, conservation assumptions, and data provenance."
    }

    with (output_dir / "incidence_structure_calculator.json").open("w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)

    with (output_dir / "incidence_structure_calculator.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(result.keys()))
        writer.writeheader()
        writer.writerow(result)

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
