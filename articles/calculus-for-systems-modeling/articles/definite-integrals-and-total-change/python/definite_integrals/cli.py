from __future__ import annotations

import argparse
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE_ROOT))

from definite_integrals.core import (
    audit_integral,
    rectangle_integral,
    signed_values,
    to_dicts,
    trapezoid_integral,
    write_csv,
    write_json,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()

    times = [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
    rates = signed_values(times)
    audit = audit_integral(times)

    write_csv(args.output_dir / "tables" / "definite_integral_audit.csv", to_dicts([audit]))

    comparison = {
        "article": "Definite Integrals and Total Change",
        "advanced_standard": True,
        "interval": [times[0], times[-1]],
        "trapezoidal_signed": trapezoid_integral(rates, times),
        "rectangle_signed": rectangle_integral(rates, times),
        "trapezoidal_absolute": trapezoid_integral([abs(r) for r in rates], times),
        "diagnostics": [
            "integrand_definition",
            "interval_bounds",
            "sign_convention",
            "signed_vs_absolute_accumulation",
            "unit_check",
            "method_comparison"
        ],
        "warning": "Definite-integral claims require integrand, bounds, sign convention, units, and method documentation."
    }

    write_json(args.output_dir / "json" / "definite_integral_manifest.json", comparison)

    (args.output_dir / "logs").mkdir(parents=True, exist_ok=True)
    (args.output_dir / "logs" / "python_workflow.log").write_text("Definite integral audit completed.\n", encoding="utf-8")
    print("Definite integral audit complete.")


if __name__ == "__main__":
    main()
