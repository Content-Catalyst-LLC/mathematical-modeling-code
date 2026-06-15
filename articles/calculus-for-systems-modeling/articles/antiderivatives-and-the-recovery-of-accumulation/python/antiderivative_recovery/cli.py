from __future__ import annotations

import argparse
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE_ROOT))

from antiderivative_recovery.core import (
    rectangle_recovery,
    to_dicts,
    trapezoid_recovery,
    write_csv,
    write_json,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()

    times = [0, 1, 2, 3, 4, 5, 6]
    initial_stock = 100.0

    trapezoid_rows = trapezoid_recovery(times, initial_stock)
    rectangle_rows = rectangle_recovery(times, initial_stock)

    write_csv(args.output_dir / "tables" / "antiderivative_recovery_audit.csv", to_dicts(trapezoid_rows))
    write_csv(args.output_dir / "tables" / "rectangle_recovery_comparison.csv", to_dicts(rectangle_rows))

    comparison = {
        "article": "Antiderivatives and the Recovery of Accumulation",
        "advanced_standard": True,
        "initial_stock": initial_stock,
        "time_grid": times,
        "methods": ["trapezoidal accumulation", "left-rectangle accumulation"],
        "diagnostics": [
            "baseline_record",
            "net_flow_definition",
            "unit_check",
            "method_warning",
            "time_step_check",
            "missing_flow_review"
        ],
        "warning": "Recovered accumulation depends on initial condition, rate definition, interval, units, and numerical method."
    }

    write_json(args.output_dir / "json" / "antiderivative_recovery_manifest.json", comparison)

    (args.output_dir / "logs").mkdir(parents=True, exist_ok=True)
    (args.output_dir / "logs" / "python_workflow.log").write_text("Antiderivative recovery audit completed.\n", encoding="utf-8")
    print("Antiderivative recovery audit complete.")


if __name__ == "__main__":
    main()
