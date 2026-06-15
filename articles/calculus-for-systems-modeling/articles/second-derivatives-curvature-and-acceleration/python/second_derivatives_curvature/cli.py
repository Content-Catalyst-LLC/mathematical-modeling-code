from __future__ import annotations

import argparse
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE_ROOT))

from second_derivatives_curvature.core import second_derivative_audits, to_dicts, write_csv, write_json


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()

    rows = second_derivative_audits([-4.0, -2.0, -1.0, 0.0, 1.0, 2.0, 4.0])
    row_dicts = to_dicts(rows)

    write_csv(args.output_dir / "tables" / "second_derivative_audit.csv", row_dicts)

    write_json(args.output_dir / "json" / "second_derivative_manifest.json", {
        "article": "Second Derivatives, Curvature, and Acceleration",
        "advanced_standard": True,
        "diagnostics": ["first_derivative", "second_derivative", "curvature", "concavity", "finite_difference_check", "noise_warning"],
        "warning": "Second-derivative claims require smoothness, local validity, finite-difference robustness, and noise review."
    })

    (args.output_dir / "logs").mkdir(parents=True, exist_ok=True)
    (args.output_dir / "logs" / "python_workflow.log").write_text("Second-derivative audit completed.\n", encoding="utf-8")
    print("Second-derivative audit complete.")


if __name__ == "__main__":
    main()
