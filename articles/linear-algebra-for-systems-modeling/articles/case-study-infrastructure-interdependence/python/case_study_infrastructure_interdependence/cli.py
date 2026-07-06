from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class InfrastructureInterdependenceAudit:
    workflow_name: str
    scenario_name: str
    sector_count: int
    initial_shock_sector: str
    initial_shock_magnitude: float
    highest_dependency_burden_sector: str
    highest_dependency_burden: float
    largest_downstream_loss_sector: str
    largest_downstream_loss: float
    total_estimated_downstream_loss: float
    sensitivity_warning: str
    interpretation_warning: str


SECTORS = ["power", "water", "communications", "transportation", "health"]

DEPENDENCY = [
    [0.00, 0.05, 0.10, 0.10, 0.00],
    [0.70, 0.00, 0.10, 0.20, 0.00],
    [0.60, 0.00, 0.00, 0.10, 0.00],
    [0.30, 0.00, 0.20, 0.00, 0.05],
    [0.80, 0.50, 0.40, 0.30, 0.00],
]


def matvec(matrix: list[list[float]], vector: list[float]) -> list[float]:
    return [sum(row[j] * vector[j] for j in range(len(vector))) for row in matrix]


def column_sums(matrix: list[list[float]]) -> list[float]:
    n = len(matrix)
    return [sum(matrix[i][j] for i in range(n)) for j in range(n)]


def build_audit() -> InfrastructureInterdependenceAudit:
    initial_disruption = [0.0 for _ in SECTORS]
    power_index = SECTORS.index("power")
    initial_disruption[power_index] = 0.40

    downstream_loss = matvec(DEPENDENCY, initial_disruption)
    burden = column_sums(DEPENDENCY)

    highest_burden_index = max(range(len(SECTORS)), key=lambda i: burden[i])
    largest_loss_index = max(range(len(SECTORS)), key=lambda i: downstream_loss[i])

    return InfrastructureInterdependenceAudit(
        workflow_name="infrastructure_interdependence_audit",
        scenario_name="synthetic_power_disruption_dependency_scenario",
        sector_count=len(SECTORS),
        initial_shock_sector="power",
        initial_shock_magnitude=0.40,
        highest_dependency_burden_sector=SECTORS[highest_burden_index],
        highest_dependency_burden=round(burden[highest_burden_index], 12),
        largest_downstream_loss_sector=SECTORS[largest_loss_index],
        largest_downstream_loss=round(downstream_loss[largest_loss_index], 12),
        total_estimated_downstream_loss=round(sum(downstream_loss), 12),
        sensitivity_warning="Dependency weights are scenario assumptions. Results should be compared across alternative weights, redundancy assumptions, time delays, and recovery capacities.",
        interpretation_warning="This one-step linear cascade estimate supports exploratory planning only. It does not predict real failure behavior without geography, capacity, timing, backup systems, operational response, validation evidence, and equity review.",
    )


def write_outputs(output_dir: Path) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)

    audit = build_audit()
    row = asdict(audit)

    with (output_dir / "tables" / "infrastructure_interdependence_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)

    (output_dir / "json" / "infrastructure_interdependence_audit.json").write_text(
        json.dumps(row, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    report = [
        "# Infrastructure Interdependence Audit",
        "",
        f"- Workflow: {audit.workflow_name}",
        f"- Scenario: {audit.scenario_name}",
        f"- Sector count: {audit.sector_count}",
        f"- Initial shock sector: {audit.initial_shock_sector}",
        f"- Initial shock magnitude: {audit.initial_shock_magnitude}",
        f"- Highest dependency-burden sector: {audit.highest_dependency_burden_sector}",
        f"- Highest dependency burden: {audit.highest_dependency_burden}",
        f"- Largest downstream-loss sector: {audit.largest_downstream_loss_sector}",
        f"- Largest downstream loss: {audit.largest_downstream_loss}",
        f"- Total estimated downstream loss: {audit.total_estimated_downstream_loss}",
        "",
        audit.sensitivity_warning,
        "",
        audit.interpretation_warning,
    ]
    (output_dir / "reports" / "infrastructure_interdependence_audit.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Infrastructure interdependence audit complete.")


if __name__ == "__main__":
    main()
