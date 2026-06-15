from __future__ import annotations

import argparse
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE_ROOT))

from convergence_tests.core import (
    audit_alternating_harmonic,
    audit_geometric,
    audit_harmonic,
    audit_p_series,
    to_dicts,
    write_csv,
    write_json,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()

    records = [
        audit_geometric(10.0, 0.6, 25),
        audit_geometric(10.0, 1.05, 25),
        audit_harmonic(10000),
        audit_p_series(1.25, 10000),
        audit_p_series(0.75, 10000),
        audit_alternating_harmonic(10000),
    ]

    write_csv(args.output_dir / "tables" / "convergence_test_audit.csv", to_dicts(records))

    manifest = {
        "article": "Convergence Tests and the Discipline of Infinite Approximation",
        "advanced_standard": True,
        "diagnostics": [
            "test_selected",
            "test_conditions",
            "term_test",
            "geometric_test",
            "p_series_test",
            "comparison_logic",
            "ratio_root_inconclusive_cases",
            "integral_tail_bounds",
            "alternating_series_error_bound",
            "absolute_vs_conditional_convergence",
            "stopping_rule",
            "remainder_estimate"
        ],
        "records": to_dicts(records),
        "warning": "A finite partial sum is not an infinite-series conclusion without test conditions and remainder logic."
    }

    write_json(args.output_dir / "json" / "convergence_test_manifest.json", manifest)

    (args.output_dir / "logs").mkdir(parents=True, exist_ok=True)
    (args.output_dir / "logs" / "python_workflow.log").write_text("Convergence-test audit completed.\n", encoding="utf-8")
    print("Convergence-test audit complete.")


if __name__ == "__main__":
    main()
