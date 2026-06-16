from pathlib import Path
import csv, json

ROOT = Path(__file__).resolve().parents[1]
out = ROOT / "outputs"
(out/"tables").mkdir(parents=True, exist_ok=True)
(out/"reports").mkdir(parents=True, exist_ok=True)
(out/"json").mkdir(parents=True, exist_ok=True)

def delay(u):
    if u >= 1.0:
        return 999.0
    return 1.0 * (1.0 + 0.8 * (u / (1.0 - u)))

rows = []
for arrival in [70, 85, 95, 105, 120]:
    u = arrival / 100.0
    rows.append({
        "arrival_rate": arrival,
        "capacity": 100.0,
        "utilization": u,
        "delay_index": delay(min(u, 0.999)),
        "governance_status": "review" if u >= 0.9 else "stable",
        "warning": "Near-capacity operation increases delay sensitivity."
    })

with (out/"tables"/"advanced_infrastructure_utilization_sweep.csv").open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)

audit = {
    "article": "Infrastructure Flow and Capacity Dynamics",
    "advanced_standard": True,
    "features": [
        "queue balance",
        "utilization ratio",
        "nonlinear delay",
        "bottleneck effective capacity",
        "buffer saturation",
        "maintenance decay",
        "resilience records",
        "peak-load scenarios",
        "calculator layer",
        "Catalyst Canvas governance"
    ],
    "warnings": [
        "Nominal capacity may differ from effective capacity.",
        "Average throughput can hide waiting-time and backlog effects.",
        "Capacity should not be assumed fixed without maintenance records.",
        "Spare capacity may be essential resilience, not waste."
    ]
}

(out/"json"/"advanced_infrastructure_audit.json").write_text(json.dumps(audit, indent=2), encoding="utf-8")
(out/"reports"/"advanced_infrastructure_audit.md").write_text(
    "# Advanced Infrastructure Flow and Capacity Audit\n\n"
    "Includes queue balance, utilization, nonlinear delay, bottlenecks, buffer saturation, maintenance decay, resilience records, calculators, and Canvas artifacts.\n",
    encoding="utf-8"
)
print("Advanced infrastructure audit generated.")
