from pathlib import Path
import argparse, csv, json

CARDS = [
    {"card_id":"grid","title":"Grid","category":"model structure","score":96,"status":"active","review_date":"2026-06-15","governance_note":"Grid spacing and time step should be documented."},
    {"card_id":"stencil","title":"Stencil","category":"method","score":95,"status":"active","review_date":"2026-06-15","governance_note":"Stencil choice encodes local interaction and derivative approximation."},
    {"card_id":"explicit-update","title":"Explicit Update","category":"method","score":94,"status":"review","review_date":"2026-06-15","governance_note":"Explicit schemes require stability checks before interpretation."},
    {"card_id":"boundary-rule","title":"Boundary Rule","category":"governance","score":93,"status":"review","review_date":"2026-06-15","governance_note":"Boundary assumptions can dominate modeled behavior."}
]
parser = argparse.ArgumentParser()
parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
args = parser.parse_args()
for sub in ("json","tables","reports"):
    (args.output_dir / sub).mkdir(parents=True, exist_ok=True)
(args.output_dir / "json" / "canvas_cards.json").write_text(json.dumps(CARDS, indent=2, sort_keys=True), encoding="utf-8")
with (args.output_dir / "tables" / "canvas_cards.csv").open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(CARDS[0].keys()))
    writer.writeheader()
    writer.writerows(CARDS)
(args.output_dir / "reports" / "canvas_governance_queue.md").write_text("\n".join([f"- **{card['title']}** ({card['status']}): {card['governance_note']}" for card in CARDS]) + "\n", encoding="utf-8")
print("Catalyst Canvas cards generated.")
