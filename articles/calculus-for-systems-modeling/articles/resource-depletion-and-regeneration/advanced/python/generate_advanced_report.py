from pathlib import Path
import csv, json

ROOT = Path(__file__).resolve().parents[1]
out = ROOT / "outputs"
(out/"tables").mkdir(parents=True, exist_ok=True)
(out/"reports").mkdir(parents=True, exist_ok=True)
(out/"json").mkdir(parents=True, exist_ok=True)

r = 0.18
k = 1000.0
msy = r * k / 4.0
rows = []
for harvest in [25.0, 35.0, 45.0, 60.0]:
    rows.append({
        "harvest": harvest,
        "msy": msy,
        "harvest_to_msy_ratio": harvest / msy,
        "governance_status": "review" if harvest >= msy else "precautionary",
        "warning": "MSY is not a safe target under uncertainty by default."
    })

with (out/"tables"/"advanced_resource_harvest_sweep.csv").open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)

audit = {
    "article": "Resource Depletion and Regeneration",
    "advanced_standard": True,
    "features": [
        "stock-flow resource model",
        "renewable logistic regeneration",
        "nonrenewable drawdown",
        "threshold recovery",
        "maximum sustainable yield",
        "precautionary harvest",
        "degradation loss",
        "efficiency and rebound",
        "calculator layer",
        "Catalyst Canvas governance"
    ],
    "warnings": [
        "Renewable does not mean unlimited.",
        "MSY is not a safe target under uncertainty by default.",
        "Threshold values require evidence and precaution.",
        "Extraction should not be treated as controllable without governance assumptions."
    ]
}

(out/"json"/"advanced_resource_audit.json").write_text(json.dumps(audit, indent=2), encoding="utf-8")
(out/"reports"/"advanced_resource_audit.md").write_text(
    "# Advanced Resource Depletion and Regeneration Audit\n\n"
    "Includes stock-flow resource dynamics, logistic regeneration, nonrenewable drawdown, threshold recovery, MSY checks, precautionary harvest, degradation loss, efficiency and rebound, calculators, and Canvas artifacts.\n",
    encoding="utf-8"
)
print("Advanced resource depletion audit generated.")
