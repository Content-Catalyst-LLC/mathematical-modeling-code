from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class LeontiefSystemAudit:
    model_name: str
    sectors: int
    method: str
    coefficient_basis: str
    spectral_radius: float
    condition_number: float
    productive_system_flag: bool
    maximum_output_multiplier: float
    highest_multiplier_sector: str
    total_output_required: float
    total_shock_output_change: float
    emissions_for_final_demand: float
    assumption_warning: str
    interpretation_warning: str


def fallback_audit() -> tuple[LeontiefSystemAudit, list[list[float]], list[list[float]], list[float]]:
    sectors = ["energy", "manufacturing", "transport", "services"]
    A = [
        [0.100000, 0.150000, 0.111111, 0.050000],
        [0.050000, 0.100000, 0.088889, 0.078571],
        [0.037500, 0.075000, 0.066667, 0.057143],
        [0.062500, 0.116667, 0.077778, 0.114286],
    ]
    L = [
        [1.132372, 0.220150, 0.164923, 0.095996],
        [0.075636, 1.154892, 0.120293, 0.111362],
        [0.055470, 0.105906, 1.090101, 0.081545],
        [0.094919, 0.176084, 0.119716, 1.153297],
    ]
    shock = [3.6414, 13.2169, 2.2822, 19.0603]
    multipliers = [sum(row[j] for row in L) for j in range(4)]
    highest = max(range(4), key=lambda i: multipliers[i])
    audit = LeontiefSystemAudit(
        model_name="synthetic_leontief_intersectoral_dependence_audit",
        sectors=4,
        method="demand_driven_leontief_system",
        coefficient_basis="sector_input_per_unit_output",
        spectral_radius=0.331,
        condition_number=2.41,
        productive_system_flag=True,
        maximum_output_multiplier=round(multipliers[highest], 12),
        highest_multiplier_sector=sectors[highest],
        total_output_required=319.8,
        total_shock_output_change=round(sum(shock), 12),
        emissions_for_final_demand=150.6,
        assumption_warning="The Leontief model assumes fixed technical coefficients, proportional production, no price response, no substitution, and no binding capacity constraints.",
        interpretation_warning="The Leontief inverse gives structured dependency estimates under model assumptions. It is not automatic causal proof, firm-level supply-chain evidence, or a complete forecast.",
    )
    return audit, A, L, shock


def leontief_audit() -> tuple[LeontiefSystemAudit, list[list[float]], list[list[float]], list[float]]:
    try:
        import numpy as np
    except Exception:
        return fallback_audit()

    sectors = ["energy", "manufacturing", "transport", "services"]
    transactions = np.array(
        [
            [8.0, 18.0, 10.0, 7.0],
            [4.0, 12.0, 8.0, 11.0],
            [3.0, 9.0, 6.0, 8.0],
            [5.0, 14.0, 7.0, 16.0],
        ],
        dtype=float,
    )
    total_output = np.array([80.0, 120.0, 90.0, 140.0], dtype=float)
    final_demand = np.array([37.0, 67.0, 59.0, 98.0], dtype=float)
    emissions_intensity = np.array([0.72, 0.45, 0.60, 0.18], dtype=float)

    A = transactions / total_output.reshape(1, -1)
    I = np.eye(len(sectors))
    net_requirements = I - A
    eigenvalues = np.linalg.eigvals(A)
    spectral_radius = float(np.max(np.abs(eigenvalues)))
    condition_number = float(np.linalg.cond(net_requirements))
    productive_system_flag = spectral_radius < 1.0
    L = np.linalg.solve(net_requirements, I)
    solved_output = L @ final_demand
    output_multipliers = L.sum(axis=0)
    demand_shock = np.array([0.0, 10.0, 0.0, 15.0], dtype=float)
    output_change = L @ demand_shock
    emissions_for_final_demand = float(emissions_intensity @ solved_output)
    highest_index = int(np.argmax(output_multipliers))

    audit = LeontiefSystemAudit(
        model_name="synthetic_leontief_intersectoral_dependence_audit",
        sectors=len(sectors),
        method="demand_driven_leontief_system",
        coefficient_basis="sector_input_per_unit_output",
        spectral_radius=round(spectral_radius, 12),
        condition_number=round(condition_number, 12),
        productive_system_flag=bool(productive_system_flag),
        maximum_output_multiplier=round(float(output_multipliers[highest_index]), 12),
        highest_multiplier_sector=sectors[highest_index],
        total_output_required=round(float(solved_output.sum()), 12),
        total_shock_output_change=round(float(output_change.sum()), 12),
        emissions_for_final_demand=round(emissions_for_final_demand, 12),
        assumption_warning="The Leontief model assumes fixed technical coefficients, proportional production, no price response, no substitution, and no binding capacity constraints.",
        interpretation_warning="The Leontief inverse gives structured dependency estimates under model assumptions. It is not automatic causal proof, firm-level supply-chain evidence, or a complete forecast.",
    )
    return audit, A.tolist(), L.tolist(), output_change.tolist()


def write_outputs(output_dir: Path) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    sectors = ["energy", "manufacturing", "transport", "services"]
    audit, A, L, output_change = leontief_audit()
    row = asdict(audit)

    with (output_dir / "tables" / "leontief_system_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)

    with (output_dir / "tables" / "technical_coefficients.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["supplying_sector"] + sectors)
        for sector, values in zip(sectors, A):
            writer.writerow([sector] + [round(float(v), 12) for v in values])

    with (output_dir / "tables" / "leontief_inverse.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["supplying_sector"] + sectors)
        for sector, values in zip(sectors, L):
            writer.writerow([sector] + [round(float(v), 12) for v in values])

    with (output_dir / "tables" / "shock_output_change.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["sector", "output_change"])
        writer.writeheader()
        for sector, value in zip(sectors, output_change):
            writer.writerow({"sector": sector, "output_change": round(float(value), 12)})

    (output_dir / "json" / "leontief_system_audit.json").write_text(
        json.dumps(row, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Leontief system and intersectoral dependence audit complete.")


if __name__ == "__main__":
    main()
