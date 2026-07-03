from __future__ import annotations

import csv
import json
from pathlib import Path


def main() -> None:
    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    result = {
        "calculator": "infrastructure_network_models_calculator",
        "network_name": "synthetic_multilayer_infrastructure_network",
        "node_count": 6,
        "edge_count": 7,
        "layer_count": 6,
        "critical_asset_count": 5,
        "interdependency_edge_count": 3,
        "total_baseline_capacity": 400.0,
        "disrupted_asset": "power_substation",
        "remaining_capacity_after_disruption": 160.0,
        "capacity_loss_fraction": 0.6,
        "warning": "Infrastructure network metrics depend on asset definitions, edge meanings, layer boundaries, capacity semantics, dependency rules, scenarios, provenance, security, and vulnerability interpretation."
    }

    with (output_dir / "infrastructure_network_models_calculator.json").open("w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)

    with (output_dir / "infrastructure_network_models_calculator.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(result.keys()))
        writer.writeheader()
        writer.writerow(result)

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
