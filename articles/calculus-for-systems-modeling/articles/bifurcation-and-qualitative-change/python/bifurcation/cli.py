from __future__ import annotations
import argparse, csv, json, math
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class BifurcationRecord:
    model: str
    parameter_mu: float
    equilibrium: float | None
    derivative_value: float | None
    stability: str
    branch_status: str
    warning: str

def saddle_node_equilibria(mu: float) -> list[float]:
    if mu < 0:
        return []
    if abs(mu) < 1e-12:
        return [0.0]
    root = math.sqrt(mu)
    return [-root, root]

def saddle_node_derivative(x: float) -> float:
    return -2.0 * x

def transcritical_equilibria(mu: float) -> list[float]:
    return [0.0, mu]

def transcritical_derivative(x: float, mu: float) -> float:
    return mu - 2.0 * x

def pitchfork_equilibria(mu: float) -> list[float]:
    if mu < 0:
        return [0.0]
    if abs(mu) < 1e-12:
        return [0.0]
    root = math.sqrt(mu)
    return [0.0, -root, root]

def pitchfork_derivative(x: float, mu: float) -> float:
    return mu - 3.0 * x * x

def classify_scalar_stability(derivative_value: float, tolerance: float = 1e-8) -> str:
    if derivative_value < -tolerance:
        return "locally_stable"
    if derivative_value > tolerance:
        return "locally_unstable"
    return "inconclusive_at_critical_value"

def build_saddle_node_records(start: int = -20, stop: int = 40) -> list[BifurcationRecord]:
    records: list[BifurcationRecord] = []
    for step in range(start, stop + 1):
        mu = step / 10.0
        equilibria = saddle_node_equilibria(mu)
        if not equilibria:
            records.append(BifurcationRecord(
                model="saddle_node_normal_form",
                parameter_mu=mu,
                equilibrium=None,
                derivative_value=None,
                stability="no_real_equilibrium",
                branch_status="equilibrium_absent",
                warning="For mu below zero, the saddle-node normal form has no real equilibrium."
            ))
            continue
        for eq in equilibria:
            derivative_value = saddle_node_derivative(eq)
            records.append(BifurcationRecord(
                model="saddle_node_normal_form",
                parameter_mu=mu,
                equilibrium=eq,
                derivative_value=derivative_value,
                stability=classify_scalar_stability(derivative_value),
                branch_status="critical_branch" if abs(mu) < 1e-12 else "equilibrium_present",
                warning="Bifurcation interpretation depends on model form, parameter meaning, and domain validity."
            ))
    return records

def write_outputs(output_dir: Path, records: list[BifurcationRecord]) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    rows = [asdict(record) for record in records]
    with (output_dir / "tables" / "bifurcation_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (output_dir / "json" / "bifurcation_audit.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    records = build_saddle_node_records()
    write_outputs(args.output_dir, records)
    print("Bifurcation audit complete.")

if __name__ == "__main__":
    main()
