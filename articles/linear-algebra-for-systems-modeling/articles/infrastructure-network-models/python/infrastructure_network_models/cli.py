from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class InfrastructureAsset:
    node: str
    layer: str
    service_role: str
    critical: bool
    baseline_capacity: float


@dataclass(frozen=True)
class InfrastructureEdge:
    source: str
    target: str
    edge_type: str
    capacity: float
    dependency_strength: float


@dataclass(frozen=True)
class InfrastructureNetworkAudit:
    network_name: str
    node_count: int
    edge_count: int
    layer_count: int
    critical_asset_count: int
    interdependency_edge_count: int
    total_baseline_capacity: float
    disrupted_asset: str
    remaining_capacity_after_disruption: float
    capacity_loss_fraction: float
    governance_warning: str


def build_assets() -> list[InfrastructureAsset]:
    return [
        InfrastructureAsset("power_substation", "energy", "electric service", True, 100.0),
        InfrastructureAsset("water_pump", "water", "water pressure", True, 60.0),
        InfrastructureAsset("hospital", "health", "critical care", True, 80.0),
        InfrastructureAsset("road_bridge", "transportation", "access corridor", True, 70.0),
        InfrastructureAsset("communications_hub", "communication", "control and coordination", True, 50.0),
        InfrastructureAsset("warehouse", "logistics", "supply distribution", False, 40.0),
    ]


def build_edges() -> list[InfrastructureEdge]:
    return [
        InfrastructureEdge("power_substation", "water_pump", "functional_dependency", 60.0, 0.95),
        InfrastructureEdge("power_substation", "hospital", "functional_dependency", 80.0, 0.90),
        InfrastructureEdge("communications_hub", "power_substation", "control_dependency", 40.0, 0.70),
        InfrastructureEdge("road_bridge", "hospital", "access_link", 70.0, 0.80),
        InfrastructureEdge("road_bridge", "warehouse", "logistics_link", 40.0, 0.75),
        InfrastructureEdge("warehouse", "hospital", "supply_link", 35.0, 0.65),
        InfrastructureEdge("communications_hub", "hospital", "coordination_link", 35.0, 0.60),
    ]


def impacted_capacity(disrupted_asset: str, assets: list[InfrastructureAsset], edges: list[InfrastructureEdge]) -> float:
    asset_capacity = {asset.node: asset.baseline_capacity for asset in assets}
    impacted = {disrupted_asset}

    for edge in edges:
        if edge.source == disrupted_asset and edge.dependency_strength >= 0.80:
            impacted.add(edge.target)

    return sum(asset_capacity[node] for node in impacted)


def build_audit() -> tuple[InfrastructureNetworkAudit, list[InfrastructureAsset], list[InfrastructureEdge]]:
    assets = build_assets()
    edges = build_edges()
    layers = sorted({asset.layer for asset in assets})
    disrupted_asset = "power_substation"

    baseline_capacity = sum(asset.baseline_capacity for asset in assets)
    lost_capacity = impacted_capacity(disrupted_asset, assets, edges)
    remaining_capacity = baseline_capacity - lost_capacity

    audit = InfrastructureNetworkAudit(
        network_name="synthetic_multilayer_infrastructure_network",
        node_count=len(assets),
        edge_count=len(edges),
        layer_count=len(layers),
        critical_asset_count=sum(1 for asset in assets if asset.critical),
        interdependency_edge_count=sum(1 for edge in edges if "dependency" in edge.edge_type),
        total_baseline_capacity=round(baseline_capacity, 12),
        disrupted_asset=disrupted_asset,
        remaining_capacity_after_disruption=round(remaining_capacity, 12),
        capacity_loss_fraction=round(lost_capacity / baseline_capacity, 12),
        governance_warning=(
            "Infrastructure network results depend on asset definitions, edge definitions, layer boundaries, "
            "capacity units, dependency rules, hazard scenarios, operating conditions, data provenance, "
            "security constraints, and social vulnerability interpretation."
        ),
    )

    return audit, assets, edges


def write_outputs(output_dir: Path) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    audit, assets, edges = build_audit()
    audit_row = asdict(audit)

    with (output_dir / "tables" / "infrastructure_network_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(audit_row.keys()))
        writer.writeheader()
        writer.writerow(audit_row)

    with (output_dir / "tables" / "infrastructure_assets.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(asdict(assets[0]).keys()))
        writer.writeheader()
        writer.writerows(asdict(asset) for asset in assets)

    with (output_dir / "tables" / "infrastructure_edges.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(asdict(edges[0]).keys()))
        writer.writeheader()
        writer.writerows(asdict(edge) for edge in edges)

    (output_dir / "json" / "infrastructure_network_audit.json").write_text(
        json.dumps(audit_row, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Infrastructure network audit complete.")


if __name__ == "__main__":
    main()
