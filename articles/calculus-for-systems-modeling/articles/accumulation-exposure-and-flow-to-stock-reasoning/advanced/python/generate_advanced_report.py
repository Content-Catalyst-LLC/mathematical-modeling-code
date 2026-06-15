from pathlib import Path
import sys

CURRENT = Path(__file__).resolve()
ADVANCED_DIR = CURRENT.parents[1]
sys.path.insert(0, str(CURRENT.parent))

from advanced_flow_to_stock import sample_checks, to_dicts, write_csv, write_json


def main() -> None:
    out = ADVANCED_DIR / "outputs"
    table_dir = out / "tables"
    report_dir = out / "reports"
    json_dir = out / "json"

    checks = to_dicts(sample_checks())
    failures = [row for row in checks if not row["passed"]]

    write_csv(table_dir / "advanced_flow_to_stock_condition_checks.csv", checks)

    audit = {
        "article": "Accumulation, Exposure, and Flow-to-Stock Reasoning",
        "advanced_standard": True,
        "topics": [
            "initial_condition",
            "stock_flow_equation",
            "net_flow",
            "gross_flows",
            "exposure_window",
            "unit_consistency",
            "measurement_window",
            "accumulated_exposure_vs_consequence"
        ],
        "condition_failures": failures,
        "warnings": [
            "Rate reduction is not the same as stock reduction.",
            "Net stock change can hide large gross flows.",
            "Peak exposure is not cumulative exposure.",
            "Exposure is not harm without a response model.",
            "Measurement windows shape cumulative claims."
        ]
    }

    write_json(json_dir / "advanced_flow_to_stock_audit.json", audit)

    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "advanced_flow_to_stock_audit.md").write_text(
        "# Advanced Mathematical Audit: Accumulation, Exposure, and Flow-to-Stock Reasoning\n\n"
        "## Formal topics included\n\n"
        "- Flow-to-stock equations\n"
        "- Initial conditions\n"
        "- Net flow and gross flows\n"
        "- Cumulative exposure\n"
        "- Population-weighted exposure\n"
        "- Unit consistency\n"
        "- Measurement windows\n"
        "- Accumulated exposure versus modeled consequence\n\n"
        "## Modeling implication\n\n"
        "A responsible accumulation workflow should state the stock, flows, initial condition, sign convention, units, measurement window, data resolution, numerical method, and distinction between net change, gross activity, exposure, and consequence.\n",
        encoding="utf-8"
    )

    print("Advanced flow-to-stock audit generated.")


if __name__ == "__main__":
    main()
