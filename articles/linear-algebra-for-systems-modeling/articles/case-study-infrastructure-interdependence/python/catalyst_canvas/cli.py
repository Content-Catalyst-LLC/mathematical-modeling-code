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
        CanvasCard("sector-semantics", "Sector Semantics", "representation", 98, "active", "2026-06-29", "Define infrastructure layers, service meanings, and model boundaries."),
        CanvasCard("dependency-matrix", "Dependency Matrix", "matrix-structure", 97, "active", "2026-06-29", "Record cross-sector reliance, weight semantics, and evidence quality."),
        CanvasCard("cascade-scenario", "Cascade Scenario", "scenario-analysis", 96, "review", "2026-06-29", "Apply initial shocks and estimate downstream service loss."),
        CanvasCard("redundancy-equity", "Redundancy and Equity", "resilience", 95, "review", "2026-06-29", "Review backup capacity and uneven distributional risk."),
        CanvasCard("responsible-use", "Responsible Use", "governance", 94, "review", "2026-06-29", "Keep scenario outputs tied to validation, uncertainty, and decision boundaries."),
    ]


def write_outputs(output_dir: Path) -> None:
    cards = build_cards()
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)

    rows = [asdict(card) for card in cards]
    (output_dir / "json" / "canvas_cards.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    with (output_dir / "tables" / "canvas_cards.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    report = ["# Catalyst Canvas Governance Queue\n"]
    for card in cards:
        report.append(f"- **{card.title}** ({card.status}, score {card.score}): {card.governance_note}")
    (output_dir / "reports" / "canvas_governance_queue.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Catalyst Canvas cards and governance queue generated.")


if __name__ == "__main__":
    main()
