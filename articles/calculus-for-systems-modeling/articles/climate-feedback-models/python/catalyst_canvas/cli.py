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
        CanvasCard("forcing-record", "Forcing Record", "model definition", 96, "active", "2026-06-15", "Scenario assumptions should not be presented as predictions."),
        CanvasCard("feedback-record", "Feedback Record", "model structure", 95, "review", "2026-06-15", "Net feedback values can hide component uncertainty."),
        CanvasCard("sign-convention", "Sign Convention", "interpretation governance", 94, "review", "2026-06-15", "Feedback signs must be stated before comparing parameters."),
        CanvasCard("time-scale-record", "Time-Scale Record", "temporal governance", 93, "review", "2026-06-15", "Equilibrium response should not be confused with near-term forecast."),
        CanvasCard("claim-boundary", "Claim Boundary", "governance", 92, "review", "2026-06-15", "Climate feedback conclusions should not exceed evidence, assumptions, uncertainty, and tested scope."),
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
        "\n".join(["# Climate Feedback Canvas Governance Queue", ""] + [f"- **{c.title}** ({c.status}, score {c.score}): {c.governance_note}" for c in cards]) + "\n",
        encoding="utf-8"
    )

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Climate feedback Canvas outputs generated.")

if __name__ == "__main__":
    main()
