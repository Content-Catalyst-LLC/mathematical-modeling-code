from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class AdvancedGraphTheoryReview:
    review_item: str
    status: str
    governance_note: str


def build_reviews() -> list[AdvancedGraphTheoryReview]:
    return [
        AdvancedGraphTheoryReview("node_definition", "required", "Define graph nodes, node boundary, and units of analysis."),
        AdvancedGraphTheoryReview("edge_definition", "required", "Document what relationships produce graph edges."),
        AdvancedGraphTheoryReview("graph_type", "required", "State whether the graph is directed, undirected, weighted, bipartite, temporal, multilayer, or simplified."),
        AdvancedGraphTheoryReview("weight_semantics", "required", "Define whether weights represent distance, capacity, cost, frequency, probability, exposure, or similarity."),
        AdvancedGraphTheoryReview("pathway_metrics", "recommended", "Review walks, paths, cycles, components, reachability, and shortest paths."),
        AdvancedGraphTheoryReview("centrality_metrics", "recommended", "Choose centrality measures only when they match the systems question."),
        AdvancedGraphTheoryReview("algorithmic_fit", "recommended", "Align traversal, shortest path, flow, clustering, and ranking algorithms with graph semantics."),
        AdvancedGraphTheoryReview("provenance_missingness", "required", "Review source data, missing nodes, missing edges, false edges, stale weights, and measurement bias."),
    ]


def write_outputs(output_dir: Path) -> None:
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    reviews = build_reviews()
    rows = [asdict(review) for review in reviews]

    with (output_dir / "tables" / "advanced_graph_theory_foundations_review.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    (output_dir / "json" / "advanced_graph_theory_foundations_review.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    report = ["# Advanced Graph Theory Foundations Review\n"]
    for review in reviews:
        report.append(f"- **{review.review_item}** ({review.status}): {review.governance_note}")
    (output_dir / "reports" / "advanced_graph_theory_foundations_review.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Advanced graph theory foundations review complete.")


if __name__ == "__main__":
    main()
