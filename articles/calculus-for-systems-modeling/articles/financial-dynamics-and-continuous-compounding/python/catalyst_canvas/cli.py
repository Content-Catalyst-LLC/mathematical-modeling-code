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
        CanvasCard("rate-record", "Rate Record", "rate governance", 96, "active", "2026-06-15", "Rate convention must be documented before comparing financial outcomes."),
        CanvasCard("cash-flow-record", "Cash-Flow Record", "cash-flow governance", 95, "review", "2026-06-15", "Cash-flow timing can dominate financial conclusions."),
        CanvasCard("compounding-record", "Compounding Record", "model convention", 94, "review", "2026-06-15", "Compounding convention should match contract terms or model purpose."),
        CanvasCard("discount-record", "Discount Record", "valuation governance", 93, "review", "2026-06-15", "Discount-rate choices can dominate long-horizon conclusions."),
        CanvasCard("debt-record", "Debt Record", "debt governance", 92, "review", "2026-06-15", "Debt may grow if payment does not exceed interest accumulation."),
        CanvasCard("risk-record", "Risk Record", "risk governance", 91, "review", "2026-06-15", "Expected return does not guarantee realized compounded outcome."),
        CanvasCard("claim-boundary", "Claim Boundary", "governance", 90, "review", "2026-06-15", "Financial conclusions should not exceed rate conventions, cash-flow evidence, risk assumptions, uncertainty, and tested scope."),
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
        "\n".join(["# Financial Dynamics Canvas Governance Queue", ""] + [f"- **{c.title}** ({c.status}, score {c.score}): {c.governance_note}" for c in cards]) + "\n",
        encoding="utf-8"
    )

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Financial Dynamics Canvas outputs generated.")

if __name__ == "__main__":
    main()
