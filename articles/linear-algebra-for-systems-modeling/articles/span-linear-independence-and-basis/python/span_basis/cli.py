from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class SpanBasisAudit:
    vector_set_name: str
    ambient_dimension: int
    vector_count: int
    rank: int
    spans_ambient_space: bool
    linearly_independent: bool
    is_basis_for_ambient_space: bool
    modeling_role: str
    interpretation_warning: str


def matrix_rank(matrix: list[list[float]], tolerance: float = 1e-10) -> int:
    rows = [row[:] for row in matrix]
    row_count = len(rows)
    column_count = len(rows[0]) if rows else 0
    rank = 0

    for column in range(column_count):
        pivot = None
        for row in range(rank, row_count):
            if abs(rows[row][column]) > tolerance:
                pivot = row
                break

        if pivot is None:
            continue

        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        pivot_value = rows[rank][column]
        rows[rank] = [value / pivot_value for value in rows[rank]]

        for row in range(row_count):
            if row != rank:
                factor = rows[row][column]
                rows[row] = [
                    current - factor * pivot_current
                    for current, pivot_current in zip(rows[row], rows[rank])
                ]

        rank += 1

    return rank


def build_audit() -> SpanBasisAudit:
    candidate_vectors_as_columns = [
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.5, 0.5, 1.0],
    ]

    matrix = [
        [candidate_vectors_as_columns[col][row] for col in range(len(candidate_vectors_as_columns))]
        for row in range(3)
    ]

    ambient_dimension = 3
    vector_count = len(candidate_vectors_as_columns)
    rank = matrix_rank(matrix)

    spans_ambient_space = rank == ambient_dimension
    linearly_independent = rank == vector_count
    is_basis = spans_ambient_space and linearly_independent

    return SpanBasisAudit(
        vector_set_name="candidate_system_basis",
        ambient_dimension=ambient_dimension,
        vector_count=vector_count,
        rank=rank,
        spans_ambient_space=spans_ambient_space,
        linearly_independent=linearly_independent,
        is_basis_for_ambient_space=is_basis,
        modeling_role="Candidate basis vectors for a simplified system representation.",
        interpretation_warning=(
            "A basis for the mathematical representation is not automatically an adequate "
            "basis for the real system. Component choice and omitted dimensions still matter."
        ),
    )


def write_outputs(output_dir: Path) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    audit = build_audit()
    row = asdict(audit)

    with (output_dir / "tables" / "span_basis_audit.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)

    (output_dir / "json" / "span_basis_audit.json").write_text(
        json.dumps(row, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Span and basis audit complete.")


if __name__ == "__main__":
    main()
