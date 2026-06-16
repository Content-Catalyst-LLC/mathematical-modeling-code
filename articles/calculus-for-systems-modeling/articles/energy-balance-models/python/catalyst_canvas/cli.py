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
        CanvasCard("boundary-record", "Boundary Record", "model definition", 96, "active", "2026-06-15", "Energy balance conclusions are not meaningful without a defined boundary."),
        CanvasCard("flow-record", "Flow Record", "energy flow governance", 95, "review", "2026-06-15", "Omitted flows can change the interpretation of imbalance."),
        CanvasCard("storage-record", "Storage Record", "storage governance", 94, "review", "2026-06-15", "Equilibrium should not be confused with immediate response."),
        CanvasCard("forcing-record", "Forcing Record", "forcing governance", 93, "review", "2026-06-15", "Forcing assumptions should be documented as historical, scenario-based, or experimental."),
        CanvasCard("feedback-record", "Feedback Record", "feedback governance", 92, "review", "2026-06-15", "Feedback terms can hide multiple physical processes."),
        CanvasCard("calibration-record", "Calibration Record", "calibration governance", 91, "review", "2026-06-15", "A model can fit temperature while misrepresenting mechanism."),
        CanvasCard("claim-boundary", "Claim Boundary", "governance", 90, "review", "2026-06-15", "Energy balance conclusions should not exceed boundary definitions, data evidence, uncertainty, domain review, and tested scope."),
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
        "\n".join(["# Energy Balance Canvas Governance Queue", ""] + [f"- **{c.title}** ({c.status}, score {c.score}): {c.governance_note}" for c in cards]) + "\n",
        encoding="utf-8"
    )

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Energy Balance Canvas outputs generated.")

if __name__ == "__main__":
    main()
