from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class TaylorAudit:
    function_name: str
    center: float
    x_value: float
    order: int
    approximation: float
    reference_value: float
    absolute_error: float
    warning: str


def taylor_exp_maclaurin(x: float, order: int) -> float:
    return sum((x ** n) / math.factorial(n) for n in range(order + 1))


def taylor_sin_maclaurin(x: float, order: int) -> float:
    return sum(((-1) ** n) * (x ** (2*n + 1)) / math.factorial(2*n + 1) for n in range(order + 1))


def audit_exp(x: float, order: int) -> TaylorAudit:
    approximation = taylor_exp_maclaurin(x, order)
    reference = math.exp(x)
    return TaylorAudit(
        "exp(x)",
        0.0,
        x,
        order,
        approximation,
        reference,
        abs(reference - approximation),
        "" if abs(x) <= 2 else "Evaluation is far from the Maclaurin center; review truncation error carefully.",
    )


def audit_sin(x: float, order: int) -> TaylorAudit:
    approximation = taylor_sin_maclaurin(x, order)
    reference = math.sin(x)
    return TaylorAudit(
        "sin(x)",
        0.0,
        x,
        order,
        approximation,
        reference,
        abs(reference - approximation),
        "" if abs(x) <= 2 else "Evaluation is far from the Maclaurin center; review truncation error carefully.",
    )


def write_outputs(output_dir: Path, records: list[TaylorAudit]) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    rows = [asdict(r) for r in records]
    with (output_dir / "tables" / "taylor_approximation_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (output_dir / "json" / "taylor_approximation_audit.json").write_text(
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
        audit_sin(1.0, 5),
        audit_sin(3.0, 10),
    ]
    write_outputs(args.output_dir, records)
    print("Taylor approximation audit complete.")


if __name__ == "__main__":
    main()
