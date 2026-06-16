from pathlib import Path
import csv, json, math

ROOT = Path(__file__).resolve().parents[1]
out = ROOT / "outputs"
(out/"tables").mkdir(parents=True, exist_ok=True)
(out/"reports").mkdir(parents=True, exist_ok=True)
(out/"json").mkdir(parents=True, exist_ok=True)

def linear_decline(e0, years):
    return [max(0.0, e0 * (1 - y/years)) for y in range(years+1)]

rows = []
for decline_years in [15, 30, 45]:
    pathway = linear_decline(40.0, decline_years)
    cumulative = sum(pathway)
    rows.append({
        "decline_years": decline_years,
        "cumulative_emissions": cumulative,
        "exceeds_500Gt_budget": cumulative > 500.0,
        "warning": "Decline timing changes cumulative burden."
    })

with (out/"tables"/"advanced_carbon_pathway_timing_sweep.csv").open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)

audit = {
    "article": "Case Study: Carbon Accumulation and Emissions Pathways",
    "advanced_standard": True,
    "features": [
        "stock-flow carbon balance",
        "emissions pathways",
        "cumulative emissions",
        "atmospheric burden",
        "impulse response",
        "carbon budget exhaustion",
        "net zero and overshoot",
        "removal governance",
        "calculator layer",
        "Catalyst Canvas governance"
    ],
    "warnings": [
        "Annual-flow values are not enough; cumulative burden matters.",
        "Net zero does not erase past accumulation.",
        "Removals require feasibility, durability, and governance review.",
        "Carbon budgets are conditional estimates, not exact guarantees."
    ]
}

(out/"json"/"advanced_carbon_accumulation_audit.json").write_text(json.dumps(audit, indent=2), encoding="utf-8")
(out/"reports"/"advanced_carbon_accumulation_audit.md").write_text(
    "# Advanced Carbon Accumulation Audit\n\n"
    "Includes stock-flow carbon balance, emissions pathways, cumulative emissions, atmospheric burden, impulse response, carbon budgets, net zero, overshoot, removal governance, calculators, and Canvas artifacts.\n",
    encoding="utf-8"
)
print("Advanced carbon accumulation audit generated.")
