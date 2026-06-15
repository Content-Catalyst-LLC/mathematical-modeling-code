from __future__ import annotations
import argparse, csv, json
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class CoupledSystemRecord:
    scenario: str
    time: float
    prey: float
    predator: float
    prey_rate: float
    predator_rate: float
    alpha: float
    beta: float
    delta: float
    gamma: float
    method: str
    warning: str

def predator_prey_rates(prey: float, predator: float, alpha: float, beta: float, delta: float, gamma: float) -> tuple[float, float]:
    prey_rate = alpha * prey - beta * prey * predator
    predator_rate = delta * prey * predator - gamma * predator
    return prey_rate, predator_rate

def coexistence_equilibrium(alpha: float, beta: float, delta: float, gamma: float) -> tuple[float, float]:
    return gamma / delta, alpha / beta

def simulate_predator_prey(prey0: float, predator0: float, alpha: float, beta: float, delta: float, gamma: float, dt: float, steps: int) -> list[CoupledSystemRecord]:
    prey = prey0
    predator = predator0
    records: list[CoupledSystemRecord] = []
    for n in range(steps + 1):
        t = n * dt
        prey_rate, predator_rate = predator_prey_rates(prey, predator, alpha, beta, delta, gamma)
        records.append(CoupledSystemRecord(
            scenario="predator_prey_coupled_system",
            time=t,
            prey=prey,
            predator=predator,
            prey_rate=prey_rate,
            predator_rate=predator_rate,
            alpha=alpha,
            beta=beta,
            delta=delta,
            gamma=gamma,
            method="explicit_euler",
            warning="Predator-prey terms are illustrative and assume continuous well-mixed interaction."
        ))
        prey = max(0.0, prey + dt * prey_rate)
        predator = max(0.0, predator + dt * predator_rate)
    return records

def write_outputs(output_dir: Path, records: list[CoupledSystemRecord]) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    rows = [asdict(record) for record in records]
    with (output_dir / "tables" / "coupled_system_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (output_dir / "json" / "coupled_system_audit.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")
    eq_prey, eq_predator = coexistence_equilibrium(records[0].alpha, records[0].beta, records[0].delta, records[0].gamma)
    (output_dir / "json" / "coupled_system_equilibrium.json").write_text(json.dumps({"coexistence_prey": eq_prey, "coexistence_predator": eq_predator}, indent=2, sort_keys=True), encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    records = simulate_predator_prey(prey0=40.0, predator0=9.0, alpha=0.7, beta=0.05, delta=0.02, gamma=0.5, dt=0.01, steps=2000)
    write_outputs(args.output_dir, records)
    print("Coupled system audit complete.")

if __name__ == "__main__":
    main()
