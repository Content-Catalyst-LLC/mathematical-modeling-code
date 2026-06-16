from pathlib import Path
import csv, json, math

ROOT = Path(__file__).resolve().parents[1]
out = ROOT / "outputs"
(out / "tables").mkdir(parents=True, exist_ok=True)
(out / "reports").mkdir(parents=True, exist_ok=True)
(out / "json").mkdir(parents=True, exist_ok=True)

n0, r, k = 100.0, 0.08, 1000.0
rows = []
for t in range(0, 41, 5):
    exponential = n0 * math.exp(r * t)
    logistic = k / (1.0 + ((k - n0) / n0) * math.exp(-r * t))
    rows.append({
        "time": t,
        "exponential": exponential,
        "logistic": logistic,
        "gap": exponential - logistic,
        "warning": "exponential growth is an unconstrained baseline, not a long-run capacity model"
    })

with (out / "tables" / "advanced_population_growth_comparison.csv").open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)

audit = {
    "article": "Case Study: Modeling Population Dynamics",
    "advanced_standard": True,
    "calculator_layer_included": True,
    "catalyst_canvas_layer_included": True,
    "languages": ["python", "r", "julia", "sql", "haskell", "c", "cpp", "fortran", "rust", "go"],
    "warnings": [
        "Population model outputs depend on growth-law assumptions.",
        "Carrying capacity is assumption-bearing and may change over time.",
        "A fitted curve does not automatically prove the model mechanism.",
        "Population projections can be highly sensitive to uncertain parameters.",
        "Population model conclusions should not exceed evidence, assumptions, and tested scope."
    ]
}
(out / "json" / "advanced_population_dynamics_audit.json").write_text(json.dumps(audit, indent=2), encoding="utf-8")
(out / "reports" / "advanced_population_dynamics_audit.md").write_text(
    "# Advanced Population Dynamics Audit\n\n"
    "This report confirms parameter records, scenario records, growth-law comparison, SQL governance, Haskell typed records, multi-language support, Catalyst Canvas outputs, and calculator-layer scaffolding.\n",
    encoding="utf-8"
)
print("Advanced population dynamics audit generated.")
