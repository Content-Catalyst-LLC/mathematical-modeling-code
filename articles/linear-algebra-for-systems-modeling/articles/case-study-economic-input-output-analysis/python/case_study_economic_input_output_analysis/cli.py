from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class EconomicInputOutputAudit:
    workflow_name: str
    economy_name: str
    sector_count: int
    final_demand_total: float
    gross_output_total: float
    highest_multiplier_sector: str
    highest_output_multiplier: float
    shock_sector: str
    shock_amount: float
    gross_output_change_total: float
    leontief_infinity_condition_estimate: float
    solvability_warning: str
    interpretation_warning: str


SECTORS = ["agriculture", "manufacturing", "services"]

TECHNICAL_COEFFICIENTS = [
    [0.10, 0.20, 0.05],
    [0.15, 0.25, 0.10],
    [0.05, 0.10, 0.20],
]

FINAL_DEMAND = [100.0, 150.0, 200.0]


def identity(n: int) -> list[list[float]]:
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def subtract(A: list[list[float]], B: list[list[float]]) -> list[list[float]]:
    return [[A[i][j] - B[i][j] for j in range(len(A))] for i in range(len(A))]


def solve_linear_system(matrix: list[list[float]], rhs: list[float]) -> list[float]:
    n = len(rhs)
    aug = [row[:] + [rhs[i]] for i, row in enumerate(matrix)]

    for pivot in range(n):
        max_row = max(range(pivot, n), key=lambda r: abs(aug[r][pivot]))
        aug[pivot], aug[max_row] = aug[max_row], aug[pivot]

        pivot_value = aug[pivot][pivot]
        if abs(pivot_value) < 1e-12:
            raise ValueError("Leontief matrix is singular or nearly singular.")

        for col in range(pivot, n + 1):
            aug[pivot][col] /= pivot_value

        for row in range(n):
            if row == pivot:
                continue
            factor = aug[row][pivot]
            for col in range(pivot, n + 1):
                aug[row][col] -= factor * aug[pivot][col]

    return [aug[i][n] for i in range(n)]


def leontief_matrix(A: list[list[float]]) -> list[list[float]]:
    return subtract(identity(len(A)), A)


def inverse(matrix: list[list[float]]) -> list[list[float]]:
    n = len(matrix)
    columns = []
    for j in range(n):
        basis = [1.0 if i == j else 0.0 for i in range(n)]
        columns.append(solve_linear_system(matrix, basis))
    return [[columns[j][i] for j in range(n)] for i in range(n)]


def matvec(matrix: list[list[float]], vector: list[float]) -> list[float]:
    return [sum(row[j] * vector[j] for j in range(len(vector))) for row in matrix]


def column_sums(matrix: list[list[float]]) -> list[float]:
    n = len(matrix)
    return [sum(matrix[i][j] for i in range(n)) for j in range(n)]


def infinity_norm(matrix: list[list[float]]) -> float:
    return max(sum(abs(value) for value in row) for row in matrix)


def build_audit() -> EconomicInputOutputAudit:
    L_matrix = leontief_matrix(TECHNICAL_COEFFICIENTS)
    total_requirements = inverse(L_matrix)
    gross_output = matvec(total_requirements, FINAL_DEMAND)
    multipliers = column_sums(total_requirements)

    highest_multiplier_index = max(range(len(SECTORS)), key=lambda i: multipliers[i])

    demand_shock = [0.0, 25.0, 0.0]
    output_change = matvec(total_requirements, demand_shock)

    condition_estimate = infinity_norm(L_matrix) * infinity_norm(total_requirements)

    return EconomicInputOutputAudit(
        workflow_name="economic_input_output_audit",
        economy_name="synthetic_three_sector_economy",
        sector_count=len(SECTORS),
        final_demand_total=round(sum(FINAL_DEMAND), 12),
        gross_output_total=round(sum(gross_output), 12),
        highest_multiplier_sector=SECTORS[highest_multiplier_index],
        highest_output_multiplier=round(multipliers[highest_multiplier_index], 12),
        shock_sector="manufacturing",
        shock_amount=25.0,
        gross_output_change_total=round(sum(output_change), 12),
        leontief_infinity_condition_estimate=round(condition_estimate, 12),
        solvability_warning="The Leontief matrix must be invertible and the solution should be checked for numerical stability, residual error, plausibility, and economically meaningful output levels.",
        interpretation_warning="Input-output results depend on fixed technical coefficients, sector aggregation, domestic/import boundaries, price basis, final-demand assumptions, and capacity limits. Multipliers are not automatic measures of welfare, productivity, or policy priority.",
    )


def write_outputs(output_dir: Path) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)

    audit = build_audit()
    row = asdict(audit)

    with (output_dir / "tables" / "economic_input_output_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)

    (output_dir / "json" / "economic_input_output_audit.json").write_text(
        json.dumps(row, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    report = [
        "# Economic Input-Output Audit",
        "",
        f"- Workflow: {audit.workflow_name}",
        f"- Economy: {audit.economy_name}",
        f"- Sector count: {audit.sector_count}",
        f"- Final demand total: {audit.final_demand_total}",
        f"- Gross output total: {audit.gross_output_total}",
        f"- Highest multiplier sector: {audit.highest_multiplier_sector}",
        f"- Highest output multiplier: {audit.highest_output_multiplier}",
        f"- Shock sector: {audit.shock_sector}",
        f"- Shock amount: {audit.shock_amount}",
        f"- Gross output change total: {audit.gross_output_change_total}",
        f"- Leontief infinity condition estimate: {audit.leontief_infinity_condition_estimate}",
        "",
        audit.solvability_warning,
        "",
        audit.interpretation_warning,
    ]
    (output_dir / "reports" / "economic_input_output_audit.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Economic input-output audit complete.")


if __name__ == "__main__":
    main()
