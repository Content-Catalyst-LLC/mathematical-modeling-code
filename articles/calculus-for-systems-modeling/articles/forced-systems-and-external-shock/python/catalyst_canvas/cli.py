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
        CanvasCard("forcing-function", "Forcing Function", "model structure", 96, "active", "2026-06-15", "The external input should be justified and documented."),
        CanvasCard("impulse-shock", "Impulse Shock", "scenario design", 95, "review", "2026-06-15", "Impulse shocks should document timing, magnitude, duration, units, and time-scale assumptions."),
        CanvasCard("step-change", "Step Change", "scenario design", 94, "active", "2026-06-15", "Step changes should distinguish temporary disturbance from persistent new conditions."),
        CanvasCard("shock-response", "Shock Response", "diagnostic method", 93, "review", "2026-06-15", "Response metrics should define deviation, recovery time, cumulative loss, or threshold crossing."),
        CanvasCard("shock-governance", "Shock Governance", "governance", 92, "active", "2026-06-15", "Shock scenarios should be labeled as stress tests unless evidence supports forecast claims."),
    ]

def validate(cards: list[CanvasCard]) -> None:
    allowed_status = {"active", "archive", "review", "revise"}
    for card in cards:
        if not isinstance(card.score, int):
            raise TypeError("score must be integer")
        if card.score < 0 or card.score > 100:
            raise ValueError("score must be in [0, 100]")
        if card.status not in allowed_status:
            raise ValueError(f"invalid status: {card.status}")
        if len(card.review_date) != 10:
            raise ValueError("review_date must be YYYY-MM-DD")

def write_outputs(output_dir: Path) -> None:
    cards = build_cards()
    validate(cards)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    rows = [asdict(card) for card in cards]
    (output_dir / "json" / "canvas_cards.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")
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
