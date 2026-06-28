from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class AdvancedSolutionSpaceReview:
    review_item: str
    status: str
    governance_note: str


def build_reviews() -> list[AdvancedSolutionSpaceReview]:
    return [
        AdvancedSolutionSpaceReview("variable_definition", "required", "Define every unknown and its unit, boundary, and systems meaning."),
        AdvancedSolutionSpaceReview("constraint_definition", "required", "Classify constraints as empirical, physical, institutional, normative, or assumed."),
        AdvancedSolutionSpaceReview("rank_nullity", "required", "Record rank, nullity, method, scaling, and numerical tolerance."),
        AdvancedSolutionSpaceReview("consistency_feasibility", "required", "Separate algebraic consistency from real-world feasibility."),
        AdvancedSolutionSpaceReview("free_variable_interpretation", "required", "Explain whether free variables represent flexibility, ambiguity, or missing information."),
    ]


def write_outputs(output_dir: Path) -> None:
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    reviews = build_reviews()
    rows = [asdict(review) for review in reviews]

    with (output_dir / "tables" / "advanced_solution_space_review.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    (output_dir / "json" / "advanced_solution_space_review.json").write_text(
        json.dumps(rows, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    report = ["# Advanced Solution Space Review\n"]
    for review in reviews:
        report.append(f"- **{review.review_item}** ({review.status}): {review.governance_note}")
    (output_dir / "reports" / "advanced_solution_space_review.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Advanced solution space review complete.")


if __name__ == "__main__":
    main()
