from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class AdvancedIncidenceReview:
    review_item: str
    status: str
    governance_note: str


def build_reviews() -> list[AdvancedIncidenceReview]:
    return [
        AdvancedIncidenceReview("node_boundary", "required", "Define graph boundary and node inclusion rules."),
        AdvancedIncidenceReview("edge_definition", "required", "Document what relationship or channel produces each incidence column."),
        AdvancedIncidenceReview("sign_convention", "required", "Specify source, target, tail, head, and signed-entry convention."),
        AdvancedIncidenceReview("edge_flow_units", "required", "Define units and time scale for edge-flow vectors."),
        AdvancedIncidenceReview("flow_conservation", "required", "Document conservation, accumulation, source, sink, and storage assumptions."),
        AdvancedIncidenceReview("laplacian_construction", "recommended", "State whether the Laplacian is unweighted, weighted, normalized, or domain-specific."),
        AdvancedIncidenceReview("sparse_representation", "recommended", "Report nonzero count, density, and sparse storage choices."),
        AdvancedIncidenceReview("provenance_missingness", "required", "Review source data, missing edges, false edges, stale data, and measurement bias."),
    ]


def write_outputs(output_dir: Path) -> None:
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    reviews = build_reviews()
    rows = [asdict(review) for review in reviews]

    with (output_dir / "tables" / "advanced_incidence_structure_review.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    (output_dir / "json" / "advanced_incidence_structure_review.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    report = ["# Advanced Incidence Structure Review\n"]
    for review in reviews:
        report.append(f"- **{review.review_item}** ({review.status}): {review.governance_note}")
    (output_dir / "reports" / "advanced_incidence_structure_review.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Advanced incidence structure review complete.")


if __name__ == "__main__":
    main()
