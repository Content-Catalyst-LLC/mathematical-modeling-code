from pathlib import Path
import argparse, csv, json
CARDS = [
    {"card_id":"riemann-sum","title":"Riemann Sum","category":"method","score":96,"status":"active","review_date":"2026-06-15","governance_note":"Endpoint convention and spacing should be recorded."},
    {"card_id":"trapezoidal-rule","title":"Trapezoidal Rule","category":"method","score":95,"status":"active","review_date":"2026-06-15","governance_note":"Adjacent-value averaging should be documented."},
    {"card_id":"cumulative-integration","title":"Cumulative Integration","category":"systems use","score":94,"status":"active","review_date":"2026-06-15","governance_note":"Running totals should be preserved."},
    {"card_id":"conservation-check","title":"Conservation Check","category":"governance","score":93,"status":"review","review_date":"2026-06-15","governance_note":"Stock-flow consistency should be checked."}
]
parser = argparse.ArgumentParser()
parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
args = parser.parse_args()
for sub in ("json","tables","reports"):
    (args.output_dir / sub).mkdir(parents=True, exist_ok=True)
(args.output_dir / "json" / "canvas_cards.json").write_text(json.dumps(CARDS, indent=2, sort_keys=True), encoding="utf-8")
with (args.output_dir / "tables" / "canvas_cards.csv").open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(CARDS[0].keys()))
    writer.writeheader()
    writer.writerows(CARDS)
(args.output_dir / "reports" / "canvas_governance_queue.md").write_text("\n".join([f"- **{c['title']}** ({c['status']}): {c['governance_note']}" for c in CARDS]) + "\n", encoding="utf-8")
print("Catalyst Canvas cards generated.")
