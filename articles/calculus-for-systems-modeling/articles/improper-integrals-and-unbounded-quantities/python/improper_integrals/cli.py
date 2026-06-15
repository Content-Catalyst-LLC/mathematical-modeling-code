from __future__ import annotations

import argparse
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE_ROOT))

from improper_integrals.core import (
    audit_infinite_cutoffs,
    audit_singular_epsilons,
    p_tail_classification,
    to_dicts,
    write_csv,
    write_json,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()

    infinite_rows = audit_infinite_cutoffs([2, 4, 8, 12, 20])
    singular_rows = audit_singular_epsilons([0.1, 0.05, 0.01, 0.005, 0.001])

    write_csv(args.output_dir / "tables" / "improper_integral_audit.csv", to_dicts(infinite_rows))
    write_csv(args.output_dir / "tables" / "singular_endpoint_audit.csv", to_dicts(singular_rows))

    p_values = [0.75, 1.0, 1.25, 2.0]
    manifest = {
        "article": "Improper Integrals and Unbounded Quantities",
        "advanced_standard": True,
        "infinite_horizon_cutoffs": [row.cutoff for row in infinite_rows],
        "singular_endpoint_epsilons": [row.epsilon for row in singular_rows],
        "p_tail_classification": {str(p): p_tail_classification(p) for p in p_values},
        "diagnostics": [
            "limiting_process",
            "convergence_evidence",
            "tail_behavior",
            "truncation_cutoff",
            "singular_endpoint",
            "model_validity_boundary"
        ],
        "warning": "A finite numerical cutoff is not an infinite-horizon result without tail evidence."
    }

    write_json(args.output_dir / "json" / "improper_integral_manifest.json", manifest)

    (args.output_dir / "logs").mkdir(parents=True, exist_ok=True)
    (args.output_dir / "logs" / "python_workflow.log").write_text("Improper-integral audit completed.\n", encoding="utf-8")
    print("Improper-integral audit complete.")


if __name__ == "__main__":
    main()
