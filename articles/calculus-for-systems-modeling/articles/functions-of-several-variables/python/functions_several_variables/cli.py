from __future__ import annotations
import argparse, csv, json
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class MultivariableFunctionRecord:
    x: float
    y: float
    output: float
    feasible: bool
    warning: str

def system_response(x: float, y: float) -> float:
    return 3.0 * x + 2.0 * y + 0.5 * x * y

def is_feasible(x: float, y: float, budget: float = 10.0) -> bool:
    return x >= 0 and y >= 0 and x + y <= budget

def evaluate_grid() -> list[MultivariableFunctionRecord]:
    records = []
    for x in [0, 2, 4, 6, 8, 10]:
        for y in [0, 2, 4, 6, 8, 10]:
            feasible = is_feasible(float(x), float(y))
            records.append(MultivariableFunctionRecord(float(x), float(y), system_response(float(x), float(y)), feasible, "" if feasible else "Input combination is outside the feasible region."))
    return records

def write_outputs(output_dir: Path, records: list[MultivariableFunctionRecord]) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    rows = [asdict(r) for r in records]
    with (output_dir / "tables" / "multivariable_function_grid.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (output_dir / "json" / "multivariable_function_grid.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir, evaluate_grid())
    print("Multivariable function grid audit complete.")

if __name__ == "__main__":
    main()
