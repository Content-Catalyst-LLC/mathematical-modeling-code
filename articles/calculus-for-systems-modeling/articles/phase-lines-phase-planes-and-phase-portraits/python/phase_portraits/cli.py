from __future__ import annotations
import argparse, csv, json, math
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class PhaseRecord:
    x: float
    y: float
    dxdt: float
    dydt: float
    x_nullcline_residual: float
    y_nullcline_residual: float
    speed: float
    warning: str

def predator_prey_rates(x: float, y: float, alpha: float, beta: float, delta: float, gamma: float) -> tuple[float, float]:
    dxdt = alpha * x - beta * x * y
    dydt = delta * x * y - gamma * y
    return dxdt, dydt

def phase_speed(dxdt: float, dydt: float) -> float:
    return math.sqrt(dxdt * dxdt + dydt * dydt)

def coexistence_equilibrium(alpha: float, beta: float, delta: float, gamma: float) -> tuple[float, float]:
    return gamma / delta, alpha / beta

def build_phase_grid() -> list[PhaseRecord]:
    alpha, beta, delta, gamma = 0.7, 0.05, 0.02, 0.5
    records: list[PhaseRecord] = []
    for x in range(0, 61, 5):
        for y in range(0, 31, 3):
            dxdt, dydt = predator_prey_rates(float(x), float(y), alpha, beta, delta, gamma)
            records.append(PhaseRecord(
                x=float(x),
                y=float(y),
                dxdt=dxdt,
                dydt=dydt,
                x_nullcline_residual=dxdt,
                y_nullcline_residual=dydt,
                speed=phase_speed(dxdt, dydt),
                warning="Vector-field values depend on parameter values, state ranges, and the assumed interaction structure."
            ))
    return records

def write_outputs(output_dir: Path, records: list[PhaseRecord]) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    rows = [asdict(record) for record in records]
    with (output_dir / "tables" / "phase_portrait_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (output_dir / "json" / "phase_portrait_audit.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")
    eq = {
        "extinction": [0.0, 0.0],
        "coexistence": list(coexistence_equilibrium(0.7, 0.05, 0.02, 0.5))
    }
    (output_dir / "json" / "phase_portrait_equilibria.json").write_text(json.dumps(eq, indent=2, sort_keys=True), encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    records = build_phase_grid()
    write_outputs(args.output_dir, records)
    print("Phase portrait audit complete.")

if __name__ == "__main__":
    main()
