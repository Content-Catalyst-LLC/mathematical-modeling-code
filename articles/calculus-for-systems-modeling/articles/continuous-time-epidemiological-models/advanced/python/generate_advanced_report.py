from pathlib import Path
import csv, json, math

ROOT = Path(__file__).resolve().parents[1]
out = ROOT / "outputs"
(out/"tables").mkdir(parents=True, exist_ok=True)
(out/"reports").mkdir(parents=True, exist_ok=True)
(out/"json").mkdir(parents=True, exist_ok=True)

rows = []
for beta in [0.18, 0.22, 0.28, 0.32, 0.38]:
    gamma = 0.10
    r0 = beta / gamma
    growth = beta - gamma
    rows.append({
        "beta": beta,
        "gamma": gamma,
        "r0": r0,
        "doubling_time": math.inf if growth <= 0 else math.log(2) / growth,
        "herd_immunity_threshold": max(0, 1 - 1 / r0),
        "governance_status": "review",
        "warning": "Transmission sensitivity should be interpreted with contact, reporting, and model-structure assumptions."
    })

with (out/"tables"/"advanced_epidemiology_transmission_sweep.csv").open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)

audit = {
    "article": "Continuous-Time Epidemiological Models",
    "advanced_standard": True,
    "features": [
        "SIR simulation",
        "SEIR simulation",
        "force of infection",
        "incidence and prevalence",
        "basic reproduction number",
        "effective reproduction number",
        "doubling time",
        "herd-immunity threshold",
        "vaccination and waning",
        "reporting governance",
        "calculator layer",
        "Catalyst Canvas governance"
    ],
    "warnings": [
        "Reported cases should not be treated as true infections without observation assumptions.",
        "Transmission parameters can hide behavior, contact, biology, and environment.",
        "Intervention effects should not be represented as unexplained reductions.",
        "Epidemiological outputs should be presented with uncertainty and purpose."
    ]
}

(out/"json"/"advanced_epidemiology_audit.json").write_text(json.dumps(audit, indent=2), encoding="utf-8")
(out/"reports"/"advanced_epidemiology_audit.md").write_text(
    "# Advanced Continuous-Time Epidemiological Model Audit\n\n"
    "Includes SIR, SEIR, reproduction numbers, doubling time, threshold analysis, vaccination, waning, reporting assumptions, calculators, and Canvas artifacts.\n",
    encoding="utf-8"
)
print("Advanced epidemiology audit generated.")
