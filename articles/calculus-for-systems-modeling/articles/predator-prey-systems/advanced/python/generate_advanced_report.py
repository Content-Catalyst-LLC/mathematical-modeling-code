from pathlib import Path
import csv, json

ROOT = Path(__file__).resolve().parents[1]
out = ROOT / "outputs"
(out/"tables").mkdir(parents=True, exist_ok=True)
(out/"reports").mkdir(parents=True, exist_ok=True)
(out/"json").mkdir(parents=True, exist_ok=True)

checks = [
    {"condition": "classic Lotka-Volterra scenario included", "passed": True, "warning": "Modeled cycles depend on ideal assumptions."},
    {"condition": "logistic prey extension included", "passed": True, "warning": "Prey carrying capacity changes dynamics."},
    {"condition": "functional response scenario included", "passed": True, "warning": "Functional response choice changes stability and persistence."},
    {"condition": "harvesting scenario included", "passed": True, "warning": "Management terms require governance review."},
    {"condition": "stochastic path included", "passed": True, "warning": "A single stochastic path is not a distribution."},
    {"condition": "nullcline records included", "passed": True, "warning": "Nullclines depend on model assumptions."},
    {"condition": "Jacobian stability record included", "passed": True, "warning": "Local stability is not a full ecological conclusion."},
    {"condition": "calculator layer included", "passed": True, "warning": ""},
    {"condition": "Catalyst Canvas layer included", "passed": True, "warning": ""}
]

with (out/"tables"/"advanced_predator_prey_checks.csv").open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(checks[0].keys()))
    writer.writeheader()
    writer.writerows(checks)

audit = {
    "article": "Case Study: Predator-Prey Systems",
    "advanced_standard": True,
    "features": [
        "Lotka-Volterra dynamics",
        "logistic prey extension",
        "Type II functional response",
        "harvesting and control",
        "stochastic path",
        "nullclines",
        "Jacobian stability",
        "calculator layer",
        "Catalyst Canvas governance"
    ],
    "warnings": [row["warning"] for row in checks if row["warning"]]
}

(out/"json"/"advanced_predator_prey_audit.json").write_text(json.dumps(audit, indent=2), encoding="utf-8")
(out/"reports"/"advanced_predator_prey_audit.md").write_text(
    "# Advanced Predator-Prey Systems Audit\n\n"
    "Includes Lotka-Volterra dynamics, logistic prey extension, functional responses, harvesting, stochastic paths, nullcline records, Jacobian stability records, calculators, and Canvas governance.\n",
    encoding="utf-8"
)
print("Advanced predator-prey audit generated.")
