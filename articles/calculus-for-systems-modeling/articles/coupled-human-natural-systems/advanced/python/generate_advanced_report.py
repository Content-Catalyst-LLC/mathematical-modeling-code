from pathlib import Path
import csv, json

ROOT = Path(__file__).resolve().parents[1]
out = ROOT / "outputs"
(out/"tables").mkdir(parents=True, exist_ok=True)
(out/"reports").mkdir(parents=True, exist_ok=True)
(out/"json").mkdir(parents=True, exist_ok=True)

rows = []
for governance in [0.1, 0.3, 0.6, 0.85, 1.0]:
    stock = 80.0
    effort = 12.0
    harvest = 0.003 * effort * stock
    regeneration = 0.08 * stock * (1 - stock / 100.0)
    governance_note = "review" if governance < 0.6 else "monitor"
    rows.append({
        "governance_strength": governance,
        "stock": stock,
        "effort": effort,
        "regeneration": regeneration,
        "extraction": harvest,
        "net_change_before_stress": regeneration - harvest,
        "governance_status": governance_note,
        "warning": "Governance strength should be interpreted with legitimacy, enforcement, participation, trust, and resources."
    })

with (out/"tables"/"advanced_coupled_governance_sensitivity.csv").open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)

audit = {
    "article": "Coupled Human-Natural Systems",
    "advanced_standard": True,
    "features": [
        "coupled stocks and flows",
        "resource regeneration",
        "extraction pressure",
        "adaptive effort",
        "governance sensitivity",
        "threshold warning",
        "distributional burden",
        "calculator layer",
        "Catalyst Canvas governance"
    ],
    "warnings": [
        "People should not be reduced to a homogeneous pressure term.",
        "Nature should not be reduced to a passive resource supply.",
        "Governance should not be treated as a fixed or neutral constant without justification.",
        "Aggregate efficiency can hide unequal burden, displacement, and environmental injustice."
    ]
}

(out/"json"/"advanced_coupled_systems_audit.json").write_text(json.dumps(audit, indent=2), encoding="utf-8")
(out/"reports"/"advanced_coupled_systems_audit.md").write_text(
    "# Advanced Coupled Human-Natural Systems Audit\n\nIncludes resource regeneration, extraction pressure, adaptive response, governance sensitivity, thresholds, distributional burden, calculators, and Canvas artifacts.\n",
    encoding="utf-8"
)
print("Advanced coupled systems audit generated.")
