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
        CanvasCard("flow-definition", "Flow Definition", "model-design", 97, "active", "2026-06-29", "Define what moves, with units and time scale."),
        CanvasCard("capacity-bounds", "Capacity Bounds", "network-diagnostics", 96, "active", "2026-06-29", "Review edge capacity, slack, saturation, and violations."),
        CanvasCard("node-balance", "Node Balance", "linear-algebra", 95, "review", "2026-06-29", "Check source, sink, transshipment, conservation, storage, and loss assumptions."),
        CanvasCard("cut-bottleneck", "Cut and Bottleneck", "optimization", 94, "review", "2026-06-29", "Identify capacity-limiting partitions and vulnerability surfaces."),
        CanvasCard("flow-governance", "Flow Governance", "interpretation", 93, "review", "2026-06-29", "Review costs, uncertainty, solver choices, equity, access, and burden tradeoffs."),
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
