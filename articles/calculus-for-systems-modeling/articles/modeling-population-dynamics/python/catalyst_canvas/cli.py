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
        CanvasCard("growth-law", "Growth Law", "model structure", 96, "active", "2026-06-15", "A growth law is an assumption, not a universal description."),
        CanvasCard("threshold-dynamics", "Threshold Dynamics", "qualitative change", 95, "review", "2026-06-15", "Threshold parameters can be difficult to identify from limited data."),
        CanvasCard("stochastic-structure", "Stochastic Structure", "uncertainty", 94, "review", "2026-06-15", "A single stochastic path is not a distribution."),
        CanvasCard("structured-population", "Structured Population", "model structure", 93, "review", "2026-06-15", "Aggregate population size may hide reproductive composition."),
        CanvasCard("identifiability", "Identifiability", "calibration governance", 92, "review", "2026-06-15", "A fitted curve does not automatically prove parameter meaning or mechanism."),
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
    (output_dir/"reports"/"canvas_governance_queue.md").write_text("\n".join(["# Population Dynamics Canvas Queue", ""] + [f"- **{c.title}**: {c.governance_note}" for c in cards]) + "\n", encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Advanced population Canvas outputs generated.")

if __name__ == "__main__":
    main()
