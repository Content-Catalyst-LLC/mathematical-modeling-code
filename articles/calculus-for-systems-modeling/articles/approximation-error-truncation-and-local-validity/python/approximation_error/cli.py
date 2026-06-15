from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class ApproximationAudit:
    method: str
    function_name: str
    center: float
    x_value: float
    order: int
    approximation: float
    reference_value: float
    absolute_error: float
    relative_error: float
    warning: str


def taylor_exp_maclaurin(x: float, order: int) -> float:
    return sum((x ** n) / math.factorial(n) for n in range(order + 1))


def audit_exp(x: float, order: int) -> ApproximationAudit:
    approximation = taylor_exp_maclaurin(x, order)
    reference = math.exp(x)
    absolute_error = abs(reference - approximation)
    relative_error = absolute_error / abs(reference)
    return ApproximationAudit(
        method="Maclaurin truncation",
        function_name="exp(x)",
        center=0.0,
        x_value=x,
        order=order,
        approximation=approximation,
        reference_value=reference,
        absolute_error=absolute_error,
        relative_error=relative_error,
        warning="" if abs(x) <= 2 else "Evaluation is far from the expansion center; review local validity.",
    )


def write_outputs(output_dir: Path, records: list[ApproximationAudit]) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    rows = [asdict(r) for r in records]
    with (output_dir / "tables" / "approximation_error_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (output_dir / "json" / "approximation_error_audit.json").write_text(
        json.dumps(rows, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()

    records = [
        audit_exp(0.5, 2),
        audit_exp(0.5, 5),
        audit_exp(1.0, 5),
        audit_exp(1.0, 10),
        audit_exp(3.0, 10),
    ]
    write_outputs(args.output_dir, records)
    print("Approximation error audit complete.")


if __name__ == "__main__":
    main()
