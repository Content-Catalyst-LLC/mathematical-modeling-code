from __future__ import annotations

import argparse
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE_ROOT))

from fundamental_theorem.core import (
    audit,
    left_rectangle_integral,
    to_dicts,
    trapezoid_integral,
    write_csv,
    write_json,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()

    times = [0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0]
    record = audit(times)

    write_csv(args.output_dir / "tables" / "fundamental_theorem_audit.csv", to_dicts([record]))

    manifest = {
        "article": "The Fundamental Theorem of Calculus",
        "advanced_standard": True,
        "interval": [times[0], times[-1]],
        "trapezoidal_accumulated_rate": trapezoid_integral(times),
        "left_rectangle_accumulated_rate": left_rectangle_integral(times),
        "endpoint_difference": record.endpoint_difference,
        "residual": record.residual,
        "diagnostics": [
            "rate_state_consistency",
            "endpoint_difference",
            "accumulated_rate",
            "numerical_residual",
            "unit_check",
            "grid_step_review"
        ],
        "warning": "If Q'(t)=r(t), accumulated rate and endpoint difference should reconcile within documented tolerance."
    }

    write_json(args.output_dir / "json" / "fundamental_theorem_manifest.json", manifest)

    (args.output_dir / "logs").mkdir(parents=True, exist_ok=True)
    (args.output_dir / "logs" / "python_workflow.log").write_text("Fundamental Theorem audit completed.\n", encoding="utf-8")
    print("Fundamental Theorem audit complete.")


if __name__ == "__main__":
    main()
