from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class AdvancedInfrastructureInterdependenceReview:
    review_item: str
    status: str
    governance_note: str


def build_reviews() -> list[AdvancedInfrastructureInterdependenceReview]:
    return [
        AdvancedInfrastructureInterdependenceReview("sector_definition", "required", "Define whether sectors represent services, assets, operators, regions, facilities, or institutional functions."),
        AdvancedInfrastructureInterdependenceReview("dependency_semantics", "required", "State whether dependencies are physical, cyber, geographic, operational, economic, institutional, or mixed."),
        AdvancedInfrastructureInterdependenceReview("weight_evidence", "required", "Record whether weights come from operational data, historical events, expert judgment, simulations, or scenario assumptions."),
        AdvancedInfrastructureInterdependenceReview("cascade_assumption", "required", "Document whether the model uses one-step, multi-step, linear, threshold, delayed, or nonlinear propagation."),
        AdvancedInfrastructureInterdependenceReview("redundancy_review", "required", "Document backups, alternative paths, spare capacity, reserves, workarounds, and their duration limits."),
        AdvancedInfrastructureInterdependenceReview("geography_time_capacity", "required", "Review geography, time delays, capacity thresholds, storage, access, and repair constraints."),
        AdvancedInfrastructureInterdependenceReview("data_quality", "required", "Flag missing dependencies, uncertain weights, confidential data gaps, outdated records, and aggregation effects."),
        AdvancedInfrastructureInterdependenceReview("equity_review", "required", "Check whether aggregate service-loss metrics hide concentrated impacts across populations and places."),
        AdvancedInfrastructureInterdependenceReview("validation_status", "required", "Compare modeled cascades against historical disruptions, exercises, operational records, and domain expertise."),
        AdvancedInfrastructureInterdependenceReview("decision_boundary", "required", "Attach interpretation limits, uncertainty notes, review status, and stop-use conditions to outputs."),
    ]


def write_outputs(output_dir: Path) -> None:
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    reviews = build_reviews()
    rows = [asdict(review) for review in reviews]

    with (output_dir / "tables" / "advanced_infrastructure_interdependence_review.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    (output_dir / "json" / "advanced_infrastructure_interdependence_review.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    report = ["# Advanced Infrastructure Interdependence Review\n"]
    for review in reviews:
        report.append(f"- **{review.review_item}** ({review.status}): {review.governance_note}")
    (output_dir / "reports" / "advanced_infrastructure_interdependence_review.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Advanced infrastructure interdependence review complete.")


if __name__ == "__main__":
    main()
