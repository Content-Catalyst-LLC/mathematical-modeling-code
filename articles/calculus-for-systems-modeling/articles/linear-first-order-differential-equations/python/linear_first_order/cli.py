from __future__ import annotations
import argparse, csv, json, math
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class LinearFirstOrderRecord:
    scenario: str
    time: float
    analytical_state: float
    euler_state: float
    absolute_error: float
    input_rate: float
    loss_rate: float
    equilibrium: float
    initial_state: float
    method: str
    warning: str

def equilibrium(input_rate: float, loss_rate: float) -> float:
    return input_rate / loss_rate

def analytical_solution(t: float, y0: float, input_rate: float, loss_rate: float) -> float:
    eq = equilibrium(input_rate, loss_rate)
    return eq + (y0 - eq) * math.exp(-loss_rate * t)

def rate_law(y: float, input_rate: float, loss_rate: float) -> float:
    return input_rate - loss_rate * y

def simulate_linear_input_loss(y0: float, input_rate: float, loss_rate: float, dt: float, steps: int) -> list[LinearFirstOrderRecord]:
    y = y0
    eq = equilibrium(input_rate, loss_rate)
    records: list[LinearFirstOrderRecord] = []
    for n in range(steps + 1):
        t = n * dt
        analytical = analytical_solution(t, y0, input_rate, loss_rate)
        records.append(LinearFirstOrderRecord(
            scenario="input_loss_balance",
            time=t,
            analytical_state=analytical,
            euler_state=y,
            absolute_error=abs(analytical - y),
            input_rate=input_rate,
            loss_rate=loss_rate,
            equilibrium=eq,
            initial_state=y0,
            method="analytical_vs_explicit_euler",
            warning="Assumes constant input and proportional loss."
        ))
        y = y + dt * rate_law(y, input_rate, loss_rate)
    return records

def write_outputs(output_dir: Path, records: list[LinearFirstOrderRecord]) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    rows = [asdict(record) for record in records]
    with (output_dir / "tables" / "linear_first_order_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (output_dir / "json" / "linear_first_order_audit.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    records = simulate_linear_input_loss(y0=20.0, input_rate=12.0, loss_rate=0.4, dt=0.1, steps=100)
    write_outputs(args.output_dir, records)
    print("Linear first-order audit complete.")

if __name__ == "__main__":
    main()
