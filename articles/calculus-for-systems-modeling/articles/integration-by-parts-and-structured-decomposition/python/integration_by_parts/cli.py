from __future__ import annotations

import argparse
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE_ROOT))

from integration_by_parts.core import audit_integration_by_parts, to_dicts, write_csv, write_json


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()

    record = audit_integration_by_parts(0.0, 4.0, 800)
    write_csv(args.output_dir / "tables" / "integration_by_parts_audit.csv", to_dicts([record]))

    manifest = {
        "article": "Integration by Parts and Structured Decomposition",
        "advanced_standard": True,
        "interval": [record.interval_start, record.interval_end],
        "direct_integral": record.direct_integral,
        "boundary_term": record.boundary_term,
        "residual_integral": record.residual_integral,
        "decomposed_value": record.decomposed_value,
        "decomposition_residual": record.decomposition_residual,
        "diagnostics": [
            "choice_of_parts",
            "boundary_term",
            "residual_integral",
            "unit_check",
            "decomposition_residual",
            "interpretive_purpose"
        ],
        "warning": "Integration by parts is a decomposition identity, not automatic causal attribution."
    }

    write_json(args.output_dir / "json" / "integration_by_parts_manifest.json", manifest)

    (args.output_dir / "logs").mkdir(parents=True, exist_ok=True)
    (args.output_dir / "logs" / "python_workflow.log").write_text("Integration-by-parts audit completed.\n", encoding="utf-8")
    print("Integration-by-parts audit complete.")


if __name__ == "__main__":
    main()
