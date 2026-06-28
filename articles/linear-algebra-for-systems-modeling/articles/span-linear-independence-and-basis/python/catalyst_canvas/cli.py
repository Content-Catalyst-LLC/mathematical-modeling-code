from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class CanvasCard:
    card_id: str
    title: str
    category: str
    score: int
    status: str
    review_date: str
    governance_note: str


def build_cards() -> list[CanvasCard]:
    return [
        CanvasCard("span-claim", "Span Claim", "representational capacity", 96, "active", "2026-06-28", "Document what the vector set can generate and what remains outside the span."),
        CanvasCard("independence-check", "Independence Check", "redundancy", 95, "active", "2026-06-28", "Check whether each vector contributes a genuinely new mathematical direction."),
        CanvasCard("basis-record", "Basis Record", "coordinates", 94, "review", "2026-06-28", "Record the basis, coordinate meaning, and interpretive cost of the coordinate system."),
        CanvasCard("rank-diagnostic", "Rank Diagnostic", "model capacity", 93, "review", "2026-06-28", "Document effective independent dimension, tolerance, scaling, and near-dependence warnings."),
        CanvasCard("redundancy-warning", "Redundancy Warning", "governance", 92, "active", "2026-06-28", "Identify duplicated indicators, features, scenarios, or interventions that may be overcounted."),
    ]


def validate(cards: list[CanvasCard]) -> None:
    allowed_status = {"active", "archive", "review", "revise"}
    for card in cards:
        if card.status not in allowed_status:
            raise ValueError(f"invalid status: {card.status}")
        if card.score < 0 or card.score > 100:
            raise ValueError("score must be in [0, 100]")


def write_outputs(output_dir: Path) -> None:
    cards = build_cards()
    validate(cards)

    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)

    rows = [asdict(card) for card in cards]
    (output_dir / "json" / "canvas_cards.json").write_text(
        json.dumps(rows, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    with (output_dir / "tables" / "canvas_cards.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    report_lines = ["# Catalyst Canvas Governance Queue\n"]
    for card in cards:
        report_lines.append(f"- **{card.title}** ({card.status}, score {card.score}): {card.governance_note}")
    (output_dir / "reports" / "canvas_governance_queue.md").write_text("\n".join(report_lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Catalyst Canvas cards and governance queue generated.")


if __name__ == "__main__":
    main()
