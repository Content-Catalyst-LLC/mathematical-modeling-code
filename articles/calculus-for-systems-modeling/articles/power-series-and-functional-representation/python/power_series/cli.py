from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class PowerSeriesAudit:
    function_name: str
    center: float
    x_value: float
    n_terms: int
    partial_sum: float
    reference_value: float | None
    absolute_error: float | None
    convergence_status: str
    warning: str


def geometric_power_series(x: float, n_terms: int) -> float:
    return sum(x ** n for n in range(n_terms))


def geometric_reference(x: float) -> float | None:
    if x == 1:
        return None
    return 1.0 / (1.0 - x)


def audit_geometric_series(x: float, n_terms: int) -> PowerSeriesAudit:
    partial = geometric_power_series(x, n_terms)
    converges = abs(x) < 1
    reference = geometric_reference(x) if converges else None
    error = abs(reference - partial) if reference is not None else None
    return PowerSeriesAudit(
        function_name="1/(1-x)",
        center=0.0,
        x_value=x,
        n_terms=n_terms,
        partial_sum=partial,
        reference_value=reference,
        absolute_error=error,
        convergence_status="inside radius of convergence" if converges else "outside radius of convergence",
        warning="" if converges else "Power series does not converge for this x value.",
    )


def write_outputs(output_dir: Path, records: list[PowerSeriesAudit]) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    rows = [asdict(r) for r in records]
    with (output_dir / "tables" / "power_series_approximation_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (output_dir / "json" / "power_series_approximation_audit.json").write_text(
        json.dumps(rows, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()

    records = [
        audit_geometric_series(0.25, 5),
        audit_geometric_series(0.25, 10),
        audit_geometric_series(0.75, 5),
        audit_geometric_series(0.75, 20),
        audit_geometric_series(1.25, 10),
    ]
    write_outputs(args.output_dir, records)
    print("Power-series approximation audit complete.")


if __name__ == "__main__":
    main()
