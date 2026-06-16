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
        CanvasCard("stock-flow-record", "Stock-Flow Record", "model definition", 96, "active", "2026-06-15", "Carbon pathway outputs cannot be interpreted responsibly if stock-flow definitions are unclear."),
        CanvasCard("pathway-record", "Pathway Record", "scenario governance", 95, "review", "2026-06-15", "Pathway scenarios should not be presented as guaranteed futures."),
        CanvasCard("sink-record", "Sink Record", "carbon-cycle governance", 94, "review", "2026-06-15", "Fixed sink assumptions can hide nonlinear carbon-cycle feedback."),
        CanvasCard("budget-record", "Budget Record", "constraint governance", 93, "review", "2026-06-15", "Carbon budgets are conditional estimates, not exact guarantees."),
        CanvasCard("removal-record", "Removal Record", "net-zero governance", 92, "review", "2026-06-15", "Net-zero and overshoot claims require removal governance."),
        CanvasCard("claim-boundary", "Claim Boundary", "governance", 91, "review", "2026-06-15", "Carbon pathway conclusions should not exceed accounting boundaries, evidence, assumptions, uncertainty, and tested scope."),
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
        "\n".join(["# Carbon Pathway Canvas Governance Queue", ""] + [f"- **{c.title}** ({c.status}, score {c.score}): {c.governance_note}" for c in cards]) + "\n",
        encoding="utf-8"
    )

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Carbon pathway Canvas outputs generated.")

if __name__ == "__main__":
    main()
