from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class ConvergenceTestAudit:
    series_name: str
    test_used: str
    n_terms: int
    partial_sum: float
    last_term: float
    test_result: str
    estimated_error: float | None
    stopping_rule: str
    warning: str


def geometric(a: float, r: float, n_terms: int) -> ConvergenceTestAudit:
    terms = [a * (r ** n) for n in range(n_terms)]
    partial = sum(terms)
    if abs(r) < 1:
        ref = a / (1 - r)
        return ConvergenceTestAudit(
            f"geometric_r_{r:g}",
            "geometric-series test",
            n_terms,
            partial,
            terms[-1],
            "converges by geometric-series test",
            ref - partial,
            "fixed term count with geometric tail check",
            "",
        )
    return ConvergenceTestAudit(
        f"geometric_r_{r:g}",
        "geometric-series test",
        n_terms,
        partial,
        terms[-1],
        "diverges or lacks geometric convergence",
        None,
        "fixed term count; no finite infinite-total claim",
        "ratio magnitude is not below one",
    )


def pseries(p: float, n_terms: int) -> ConvergenceTestAudit:
    terms = [1.0 / (n ** p) for n in range(1, n_terms + 1)]
    return ConvergenceTestAudit(
        f"p_series_{p:g}",
        "p-series test",
        n_terms,
        sum(terms),
        terms[-1],
        "converges" if p > 1 else "diverges",
        None,
        "fixed term count with p-series classification",
        "" if p > 1 else "p-series diverges for p less than or equal to one",
    )


def harmonic(n_terms: int) -> ConvergenceTestAudit:
    return pseries(1.0, n_terms)


def alternating_harmonic(n_terms: int) -> ConvergenceTestAudit:
    terms = [((-1.0) ** (n + 1)) / n for n in range(1, n_terms + 1)]
    return ConvergenceTestAudit(
        "alternating_harmonic",
        "alternating-series test",
        n_terms,
        sum(terms),
        terms[-1],
        "converges conditionally",
        1.0 / (n_terms + 1),
        "fixed term count with next-term error bound",
        "net convergence depends on sign cancellation; absolute series diverges",
    )


def write_csv(path: Path, records: list[ConvergenceTestAudit]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = [asdict(r) for r in records]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()

    records = [
        geometric(10.0, 0.6, 25),
        geometric(10.0, 1.05, 25),
        harmonic(10000),
        pseries(1.25, 10000),
        pseries(0.75, 10000),
        alternating_harmonic(10000),
    ]

    write_csv(args.output_dir / "tables" / "convergence_test_audit.csv", records)
    manifest = {
        "article": "Convergence Tests and the Discipline of Infinite Approximation",
        "records": [asdict(r) for r in records],
        "warning": "A finite partial sum is not an infinite-series conclusion without test conditions and remainder logic.",
    }
    (args.output_dir / "json").mkdir(parents=True, exist_ok=True)
    (args.output_dir / "json" / "convergence_test_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print("Convergence-test audit complete.")


if __name__ == "__main__":
    main()
