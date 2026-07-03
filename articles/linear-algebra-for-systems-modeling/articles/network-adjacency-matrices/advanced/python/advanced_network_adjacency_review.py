from __future__ import annotations
import argparse, csv, json
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class AdvancedNetworkAdjacencyReview:
    review_item: str
    status: str
    governance_note: str

def build_reviews() -> list[AdvancedNetworkAdjacencyReview]:
    return [
        AdvancedNetworkAdjacencyReview("node_boundary","required","Define which entities are included and excluded from the network."),
        AdvancedNetworkAdjacencyReview("edge_definition","required","Document what relationship produces a nonzero adjacency entry."),
        AdvancedNetworkAdjacencyReview("direction_convention","required","Specify whether rows point to columns or columns point to rows."),
        AdvancedNetworkAdjacencyReview("weight_semantics","required","Define whether weights represent capacity, cost, frequency, probability, exposure, or similarity."),
        AdvancedNetworkAdjacencyReview("normalization","required","Document row, column, symmetric, transition, or Laplacian transformations."),
        AdvancedNetworkAdjacencyReview("provenance_missingness","required","Review source data, missing edges, false edges, stale data, and measurement bias."),
    ]

def write_outputs(output_dir: Path) -> None:
    (output_dir/"reports").mkdir(parents=True, exist_ok=True); (output_dir/"tables").mkdir(parents=True, exist_ok=True); (output_dir/"json").mkdir(parents=True, exist_ok=True)
    rows = [asdict(review) for review in build_reviews()]
    with (output_dir/"tables/advanced_network_adjacency_review.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys())); writer.writeheader(); writer.writerows(rows)
    (output_dir/"json/advanced_network_adjacency_review.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")
    report = ["# Advanced Network Adjacency Review\n"] + [f"- **{r['review_item']}** ({r['status']}): {r['governance_note']}" for r in rows]
    (output_dir/"reports/advanced_network_adjacency_review.md").write_text("\n".join(report)+"\n", encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("--output-dir", type=Path, default=Path("outputs")); args = parser.parse_args()
    write_outputs(args.output_dir); print("Advanced network adjacency review complete.")
if __name__ == "__main__": main()
