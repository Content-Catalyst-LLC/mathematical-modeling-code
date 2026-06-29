from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

Vector = list[float]


@dataclass(frozen=True)
class OrthogonalityAudit:
    system_name: str
    vector_a: str
    vector_b: str
    dot_product: float
    orthogonal_under_tolerance: bool
    unit_a: str
    unit_b: str
    projection_of_a_onto_b: str
    residual_vector: str
    residual_norm: float
    orthonormality_error: float
    interpretation_warning: str


def dot(a: Vector, b: Vector) -> float:
    return sum(x * y for x, y in zip(a, b))


def norm2(v: Vector) -> float:
    return math.sqrt(dot(v, v))


def scale(v: Vector, c: float) -> Vector:
    return [c * x for x in v]


def subtract(a: Vector, b: Vector) -> Vector:
    return [x - y for x, y in zip(a, b)]


def normalize(v: Vector) -> Vector:
    n = norm2(v)
    if n <= 1e-12:
        raise ValueError("cannot normalize near-zero vector")
    return [x / n for x in v]


def projection(a: Vector, b: Vector) -> Vector:
    denom = dot(b, b)
    if denom <= 1e-12:
        raise ValueError("cannot project onto near-zero vector")
    return scale(b, dot(a, b) / denom)


def vector_to_string(v: Vector) -> str:
    return ",".join(f"{x:.6f}" for x in v)


def build_audit() -> OrthogonalityAudit:
    a = [3.0, 1.0, 2.0]
    b = [1.0, -1.0, -1.0]

    dot_ab = dot(a, b)
    tol = 1e-10
    unit_a = normalize(a)
    unit_b = normalize(b)

    proj_ab = projection(a, b)
    residual = subtract(a, proj_ab)

    q_dot = dot(unit_a, unit_b)
    orthonormality_error = abs(q_dot)

    return OrthogonalityAudit(
        system_name="three_component_orthogonality_audit",
        vector_a=vector_to_string(a),
        vector_b=vector_to_string(b),
        dot_product=round(dot_ab, 12),
        orthogonal_under_tolerance=abs(dot_ab) <= tol,
        unit_a=vector_to_string(unit_a),
        unit_b=vector_to_string(unit_b),
        projection_of_a_onto_b=vector_to_string(proj_ab),
        residual_vector=vector_to_string(residual),
        residual_norm=round(norm2(residual), 12),
        orthonormality_error=round(orthonormality_error, 12),
        interpretation_warning=(
            "Orthogonality depends on the chosen inner product, scaling, units, and tolerance. "
            "A residual that is orthogonal to model directions may still contain important excluded structure."
        ),
    )


def write_outputs(output_dir: Path) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    audit = build_audit()
    row = asdict(audit)

    with (output_dir / "tables" / "orthogonality_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)

    (output_dir / "json" / "orthogonality_audit.json").write_text(
        json.dumps(row, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Orthogonality audit complete.")


if __name__ == "__main__":
    main()
