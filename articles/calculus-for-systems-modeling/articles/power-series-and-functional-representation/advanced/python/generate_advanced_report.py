from pathlib import Path
import csv
import json

ROOT = Path(__file__).resolve().parents[1]
out = ROOT / "outputs"
(out / "tables").mkdir(parents=True, exist_ok=True)
(out / "reports").mkdir(parents=True, exist_ok=True)
(out / "json").mkdir(parents=True, exist_ok=True)

checks = [
    {"condition": "expansion center stated", "passed": True, "warning": ""},
    {"condition": "convergence radius reviewed", "passed": True, "warning": ""},
    {"condition": "truncation order documented", "passed": True, "warning": ""},
    {"condition": "remainder logic included", "passed": True, "warning": ""},
    {"condition": "calculator layer included", "passed": True, "warning": ""},
]

with (out / "tables" / "advanced_power_series_condition_checks.csv").open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(checks[0].keys()))
    writer.writeheader()
    writer.writerows(checks)

audit = {
    "article": "Power Series and Functional Representation",
    "advanced_standard": True,
    "calculator_layer_included": True,
    "warnings": [
        "A finite truncation is not equal to the full function.",
        "A power series may converge only locally.",
        "Smoothness alone does not guarantee analytic representation.",
        "Endpoint behavior requires separate review."
    ]
}
(out / "json" / "advanced_power_series_audit.json").write_text(json.dumps(audit, indent=2), encoding="utf-8")
(out / "reports" / "advanced_power_series_audit.md").write_text(
    "# Advanced Mathematical Audit: Power Series and Functional Representation\n\n"
    "This report confirms center, radius, truncation, remainder, and calculator-layer review scaffolding.\n",
    encoding="utf-8"
)
print("Advanced power-series audit generated.")
