from __future__ import annotations
import argparse, csv, json, math
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class OscillationRecord:
    scenario: str
    time: float
    position: float
    velocity: float
    acceleration: float
    damping_ratio: float
    natural_frequency: float
    forcing: float
    method: str
    warning: str

def forcing_function(t: float, amplitude: float = 0.0, frequency: float = 1.0) -> float:
    return amplitude * math.cos(frequency * t)

def acceleration(position: float, velocity: float, time: float, damping_ratio: float, natural_frequency: float, forcing_amplitude: float, forcing_frequency: float) -> float:
    force = forcing_function(time, forcing_amplitude, forcing_frequency)
    damping = 2.0 * damping_ratio * natural_frequency * velocity
    restoring = natural_frequency * natural_frequency * position
    return force - damping - restoring

def classify_damping(damping_ratio: float) -> str:
    if damping_ratio == 0:
        return "undamped"
    if 0 < damping_ratio < 1:
        return "underdamped"
    if damping_ratio == 1:
        return "critically_damped"
    return "overdamped"

def simulate_oscillator(scenario: str, x0: float, v0: float, damping_ratio: float, natural_frequency: float, forcing_amplitude: float, forcing_frequency: float, dt: float, steps: int) -> list[OscillationRecord]:
    x = x0
    v = v0
    records: list[OscillationRecord] = []
    for n in range(steps + 1):
        t = n * dt
        a = acceleration(x, v, t, damping_ratio, natural_frequency, forcing_amplitude, forcing_frequency)
        records.append(OscillationRecord(
            scenario=scenario,
            time=t,
            position=x,
            velocity=v,
            acceleration=a,
            damping_ratio=damping_ratio,
            natural_frequency=natural_frequency,
            forcing=forcing_function(t, forcing_amplitude, forcing_frequency),
            method="explicit_euler_first_order_system",
            warning="Explicit Euler is transparent but can distort oscillatory systems if the step size is too large."
        ))
        v = v + dt * a
        x = x + dt * v
    return records

def write_outputs(output_dir: Path, records: list[OscillationRecord]) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    rows = [asdict(record) for record in records]
    with (output_dir / "tables" / "second_order_oscillation_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (output_dir / "json" / "second_order_oscillation_audit.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    records: list[OscillationRecord] = []
    records.extend(simulate_oscillator("underdamped_unforced", 1.0, 0.0, 0.2, 1.0, 0.0, 1.0, 0.02, 500))
    records.extend(simulate_oscillator("forced_near_resonance", 1.0, 0.0, 0.1, 1.0, 0.2, 1.0, 0.02, 500))
    write_outputs(args.output_dir, records)
    print("Second-order oscillation audit complete.")

if __name__ == "__main__":
    main()
