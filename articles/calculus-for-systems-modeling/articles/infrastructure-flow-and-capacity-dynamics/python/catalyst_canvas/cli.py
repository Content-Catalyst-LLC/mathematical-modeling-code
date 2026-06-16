from __future__ import annotations
import argparse, csv, json
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
        CanvasCard("flow-record", "Flow Record", "model definition", 96, "active", "2026-06-15", "Infrastructure outputs cannot be interpreted responsibly if flow definitions are unclear."),
        CanvasCard("capacity-record", "Capacity Record", "capacity governance", 95, "review", "2026-06-15", "Nominal capacity may differ from effective capacity."),
        CanvasCard("queue-record", "Queue Record", "service governance", 94, "review", "2026-06-15", "Average throughput can hide waiting-time and backlog effects."),
        CanvasCard("bottleneck-record", "Bottleneck Record", "network governance", 93, "review", "2026-06-15", "The apparent bottleneck may shift under disruption or demand change."),
        CanvasCard("maintenance-record", "Maintenance Record", "asset governance", 92, "review", "2026-06-15", "Capacity should not be assumed fixed without maintenance records."),
        CanvasCard("resilience-record", "Resilience Record", "stress governance", 91, "review", "2026-06-15", "Spare capacity may be essential resilience, not waste."),
        CanvasCard("claim-boundary", "Claim Boundary", "governance", 90, "review", "2026-06-15", "Infrastructure conclusions should not exceed flow definitions, capacity evidence, operating conditions, uncertainty, governance feasibility, and tested scope."),
    ]

def write_outputs(output_dir: Path) -> None:
    cards = build_cards()
    (output_dir/"json").mkdir(parents=True, exist_ok=True)
    (output_dir/"tables").mkdir(parents=True, exist_ok=True)
    (output_dir/"reports").mkdir(parents=True, exist_ok=True)
    rows = [asdict(card) for card in cards]
    (output_dir/"json"/"canvas_cards.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")
    with (output_dir/"tables"/"canvas_cards.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (output_dir/"reports"/"canvas_governance_queue.md").write_text(
        "\n".join(["# Infrastructure Flow Capacity Canvas Governance Queue", ""] + [f"- **{c.title}** ({c.status}, score {c.score}): {c.governance_note}" for c in cards]) + "\n",
        encoding="utf-8"
    )

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Infrastructure Canvas outputs generated.")

if __name__ == "__main__":
    main()
