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
        CanvasCard("output-record", "Output Record", "model definition", 96, "active", "2026-06-15", "Output growth should not be treated as complete social progress."),
        CanvasCard("growth-record", "Growth Record", "growth governance", 95, "review", "2026-06-15", "Growth-rate assumptions compound strongly over time."),
        CanvasCard("capital-record", "Capital Record", "accumulation governance", 94, "review", "2026-06-15", "Capital stock measures can hide quality, maintenance, and obsolescence."),
        CanvasCard("productivity-record", "Productivity Record", "productivity governance", 93, "review", "2026-06-15", "Productivity should not be used as a residual without interpretation."),
        CanvasCard("adjustment-record", "Adjustment Record", "dynamic governance", 92, "review", "2026-06-15", "Instant adjustment assumptions can hide overshoot and persistence."),
        CanvasCard("constraint-record", "Constraint Record", "systems governance", 91, "review", "2026-06-15", "Unconstrained growth assumptions should be compared with constrained scenarios."),
        CanvasCard("claim-boundary", "Claim Boundary", "governance", 90, "review", "2026-06-15", "Economic conclusions should not exceed output definitions, data evidence, structural assumptions, uncertainty, distributional interpretation, and tested scope."),
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
        "\n".join(["# Economic Growth Canvas Governance Queue", ""] + [f"- **{c.title}** ({c.status}, score {c.score}): {c.governance_note}" for c in cards]) + "\n",
        encoding="utf-8"
    )

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Economic Growth Canvas outputs generated.")

if __name__ == "__main__":
    main()
