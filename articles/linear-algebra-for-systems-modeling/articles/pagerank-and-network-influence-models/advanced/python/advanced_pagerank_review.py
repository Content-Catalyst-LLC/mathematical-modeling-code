from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class AdvancedPageRankReview:
    review_item: str
    status: str
    governance_note: str


def build_reviews() -> list[AdvancedPageRankReview]:
    return [
        AdvancedPageRankReview("node_definition", "required", "Define ranked entities and graph boundary."),
        AdvancedPageRankReview("directed_edge_meaning", "required", "Document whether links represent citation, endorsement, dependence, exposure, attention, or flow."),
        AdvancedPageRankReview("transition_normalization", "required", "State row or column stochastic convention and normalization rule."),
        AdvancedPageRankReview("dangling_node_handling", "required", "Define redistribution rule for nodes with no outgoing links."),
        AdvancedPageRankReview("damping_teleportation", "required", "Document damping factor and teleportation or personalization vector."),
        AdvancedPageRankReview("convergence_diagnostics", "required", "Report tolerance, iteration count, residuals, and convergence status."),
        AdvancedPageRankReview("sensitivity_testing", "recommended", "Test edge perturbations, weight perturbations, damping changes, and graph-boundary alternatives."),
        AdvancedPageRankReview("ranking_governance", "required", "Review manipulation incentives, feedback loops, provenance, and interpretive limits."),
    ]


def write_outputs(output_dir: Path) -> None:
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    reviews = build_reviews()
    rows = [asdict(review) for review in reviews]

    with (output_dir / "tables" / "advanced_pagerank_review.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    (output_dir / "json" / "advanced_pagerank_review.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    report = ["# Advanced PageRank and Network Influence Review\n"]
    for review in reviews:
        report.append(f"- **{review.review_item}** ({review.status}): {review.governance_note}")
    (output_dir / "reports" / "advanced_pagerank_review.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Advanced PageRank review complete.")


if __name__ == "__main__":
    main()
