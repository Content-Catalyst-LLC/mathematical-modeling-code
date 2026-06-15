from pathlib import Path
import csv
import json

root = Path(__file__).resolve().parents[1]

required_paths = [
    root / "README.md",
    root / "docs" / "article_notes.md",
    root / "python" / "product_rule_interaction_effects" / "decomposition.py",
    root / "r" / "product_rule_decomposition.R",
    root / "sql" / "schema_product_rule_decomposition.sql",
    root / "canvas" / "cards" / "article_card.json",
    root / "outputs" / "tables" / "product_rule_decomposition_python.csv",
    root / "outputs" / "tables" / "product_rule_summary_python.csv",
]

missing = [str(path.relative_to(root)) for path in required_paths if not path.exists()]
if missing:
    raise SystemExit("Missing required files: " + ", ".join(missing))

with (root / "outputs" / "tables" / "product_rule_summary_python.csv").open(encoding="utf-8") as handle:
    rows = list(csv.DictReader(handle))

summary = {row["metric"]: float(row["value"]) for row in rows}
if summary.get("mean_abs_residual", 999.0) > 0.02:
    raise SystemExit("Mean absolute residual is too large.")

card = json.loads((root / "canvas" / "cards" / "article_card.json").read_text(encoding="utf-8"))
if card["slug"] != "product-rule-interaction-effects":
    raise SystemExit("Article card slug mismatch.")

print("Product Rule and Interaction Effects smoke check passed.")
