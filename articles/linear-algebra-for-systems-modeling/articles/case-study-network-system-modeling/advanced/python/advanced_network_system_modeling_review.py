from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class AdvancedNetworkSystemReview:
    review_item: str
    status: str
    governance_note: str


def build_reviews() -> list[AdvancedNetworkSystemReview]:
    return [
        AdvancedNetworkSystemReview("node_definition", "required", "Define whether nodes are facilities, regions, agents, documents, states, sectors, or components."),
        AdvancedNetworkSystemReview("edge_definition", "required", "Define whether edges represent flow, dependency, similarity, communication, probability, cost, or influence."),
        AdvancedNetworkSystemReview("weight_semantics", "required", "State whether larger weights mean stronger, cheaper, riskier, more likely, more costly, or more capacious relationships."),
        AdvancedNetworkSystemReview("directionality", "required", "Document whether the network is directed or undirected and whether in-degree and out-degree require separate interpretation."),
        AdvancedNetworkSystemReview("matrix_construction", "required", "Preserve adjacency, incidence, degree, Laplacian, transition, and stress-test matrices where applicable."),
        AdvancedNetworkSystemReview("connectivity_diagnostics", "required", "Inspect components, reachability, isolated nodes, and weak versus strong connectivity."),
        AdvancedNetworkSystemReview("centrality_review", "required", "Compare metric-specific definitions of importance and avoid universal centrality claims."),
        AdvancedNetworkSystemReview("vulnerability_testing", "required", "Run edge-removal, node-removal, weight-reduction, and boundary-sensitivity scenarios."),
        AdvancedNetworkSystemReview("data_quality", "required", "Flag missing edges, spurious edges, uncertain weights, temporal mismatch, and aggregation effects."),
        AdvancedNetworkSystemReview("visualization_limits", "required", "State whether layout is geographic, algorithmic, schematic, or metric-based."),
        AdvancedNetworkSystemReview("responsible_interpretation", "required", "State what centrality, vulnerability, flow, diffusion, and transition outputs can and cannot prove."),
    ]


def write_outputs(output_dir: Path) -> None:
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    reviews = build_reviews()
    rows = [asdict(review) for review in reviews]

    with (output_dir / "tables" / "advanced_network_system_modeling_review.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    (output_dir / "json" / "advanced_network_system_modeling_review.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    report = ["# Advanced Network System Modeling Review\n"]
    for review in reviews:
        report.append(f"- **{review.review_item}** ({review.status}): {review.governance_note}")
    (output_dir / "reports" / "advanced_network_system_modeling_review.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Advanced network system modeling review complete.")


if __name__ == "__main__":
    main()
