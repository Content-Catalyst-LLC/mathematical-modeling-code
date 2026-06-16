from pathlib import Path
import csv, json

ROOT = Path(__file__).resolve().parents[1]
out = ROOT / "outputs"
(out/"tables").mkdir(parents=True, exist_ok=True)
(out/"reports").mkdir(parents=True, exist_ok=True)
(out/"json").mkdir(parents=True, exist_ok=True)

rows = []
free_flow_time = 20.0
capacity = 2000.0
for volume in [1400, 1700, 2000, 2300, 2600]:
    travel_time = free_flow_time * (1 + 0.15 * (volume / capacity) ** 4)
    rows.append({
        "volume": volume,
        "capacity": capacity,
        "volume_capacity_ratio": volume / capacity,
        "travel_time": travel_time,
        "delay_above_free_flow": travel_time - free_flow_time,
        "governance_status": "review",
        "warning": "Travel-time sensitivity should be interpreted with capacity, route choice, and multimodal assumptions."
    })

with (out/"tables"/"advanced_urban_bpr_sensitivity.csv").open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)

audit = {
    "article": "Urban Dynamics and Congestion",
    "advanced_standard": True,
    "features": [
        "traffic flow identity",
        "fundamental diagram",
        "queue accumulation",
        "BPR travel-time functions",
        "induced demand",
        "accessibility",
        "curbside occupancy",
        "distributional delay burden",
        "calculator layer",
        "Catalyst Canvas governance"
    ],
    "warnings": [
        "Vehicle flow should not be treated as the only mobility outcome.",
        "Fixed-demand assumptions can mislead in long-run planning.",
        "Average travel-time improvements can hide unequal burden or local harm.",
        "Urban conclusions should not exceed boundary definitions, data evidence, behavioral assumptions, uncertainty, equity review, and tested scope."
    ]
}

(out/"json"/"advanced_urban_congestion_audit.json").write_text(json.dumps(audit, indent=2), encoding="utf-8")
(out/"reports"/"advanced_urban_congestion_audit.md").write_text(
    "# Advanced Urban Dynamics and Congestion Audit\n\nIncludes traffic flow, queueing, BPR travel time, induced demand, accessibility, curbside occupancy, distributional burden, calculators, and Canvas artifacts.\n",
    encoding="utf-8"
)
print("Advanced urban congestion audit generated.")
