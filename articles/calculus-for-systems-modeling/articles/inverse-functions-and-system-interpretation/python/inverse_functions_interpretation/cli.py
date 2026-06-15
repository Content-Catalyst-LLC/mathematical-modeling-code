from __future__ import annotations

import argparse
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE_ROOT))

from inverse_functions_interpretation.core import inverse_audits, to_dicts, write_csv, write_json


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()

    rows = inverse_audits([0.0, 0.5, 1.0, 1.5, 2.0])
    row_dicts = to_dicts(rows)

    write_csv(args.output_dir / "tables" / "inverse_interpretation_audit.csv", row_dicts)

    write_json(args.output_dir / "json" / "inverse_functions_manifest.json", {
        "article": "Inverse Functions and System Interpretation",
        "advanced_standard": True,
        "diagnostics": ["forward_check", "domain_validity", "inverse_sensitivity", "conditioning_warning", "identifiability_review"],
        "warning": "A recovered input is model-dependent and should not be treated as causal proof without identifiability, uncertainty, and domain review."
    })

    (args.output_dir / "logs").mkdir(parents=True, exist_ok=True)
    (args.output_dir / "logs" / "python_workflow.log").write_text("Inverse interpretation audit completed.\n", encoding="utf-8")
    print("Inverse interpretation audit complete.")


if __name__ == "__main__":
    main()
