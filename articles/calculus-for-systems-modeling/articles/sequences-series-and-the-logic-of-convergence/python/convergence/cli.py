from __future__ import annotations

import argparse
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE_ROOT))

from convergence.core import (
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
        audit_geometric(a=10.0, r=0.6, n_terms=25),
        audit_geometric(a=10.0, r=1.05, n_terms=25),
        audit_harmonic(n_terms=10000),
        audit_p_series(p=0.75, n_terms=10000),
        audit_p_series(p=1.25, n_terms=10000),
    ]

    write_csv(args.output_dir / "tables" / "sequence_series_convergence_audit.csv", to_dicts(records))

    manifest = {
        "article": "Sequences, Series, and the Logic of Convergence",
        "advanced_standard": True,
        "diagnostics": [
            "sequence_definition",
            "partial_sum_definition",
            "convergence_classification",
            "stopping_rule",
            "remainder_bound",
            "absolute_vs_conditional_convergence",
            "finite_computation_vs_limit_claim"
        ],
        "records": to_dicts(records),
        "warning": "A stopped computation is not automatically a converged computation."
    }

    write_json(args.output_dir / "json" / "sequence_series_convergence_manifest.json", manifest)

    (args.output_dir / "logs").mkdir(parents=True, exist_ok=True)
    (args.output_dir / "logs" / "python_workflow.log").write_text("Sequence and series convergence audit completed.\n", encoding="utf-8")
    print("Sequence and series convergence audit complete.")


if __name__ == "__main__":
    main()
