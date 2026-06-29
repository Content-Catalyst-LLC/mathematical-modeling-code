from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

Vector = list[float]
Matrix = list[list[float]]


@dataclass(frozen=True)
class StateSpaceGeometryAudit:
    system_name: str
    state_a: str
    state_b: str
    difference_vector: str
    dot_product: float
    cosine_similarity: float
    weighted_inner_product: float
    norm_1: float
    norm_2: float
    norm_inf: float
    euclidean_distance: float
    weighted_distance: float
    interpretation_warning: str


def dot(a: Vector, b: Vector) -> float:
    return sum(x * y for x, y in zip(a, b))


def matvec(A: Matrix, x: Vector) -> Vector:
    return [dot(row, x) for row in A]


def weighted_inner_product(x: Vector, y: Vector, W: Matrix) -> float:
    return dot(x, matvec(W, y))


def subtract(a: Vector, b: Vector) -> Vector:
    return [x - y for x, y in zip(a, b)]


def norm1(x: Vector) -> float:
    return sum(abs(v) for v in x)


def norm2(x: Vector) -> float:
    return math.sqrt(sum(v * v for v in x))


def norminf(x: Vector) -> float:
    return max(abs(v) for v in x)


def cosine_similarity(a: Vector, b: Vector) -> float:
    denom = norm2(a) * norm2(b)
    if denom <= 1e-12:
        raise ValueError("cosine similarity undefined for near-zero vector")
    return dot(a, b) / denom


def vector_to_string(x: Vector) -> str:
    return ",".join(f"{v:.6f}" for v in x)


def build_audit() -> StateSpaceGeometryAudit:
    state_a = [12.0, 4.0, 0.8]
    state_b = [10.0, 5.5, 1.1]
    difference = subtract(state_a, state_b)
    W = [
        [1.0, 0.0, 0.0],
        [0.0, 0.5, 0.0],
        [0.0, 0.0, 8.0],
    ]
    weighted_diff_magnitude = math.sqrt(weighted_inner_product(difference, difference, W))

    return StateSpaceGeometryAudit(
        system_name="three_indicator_state_space_geometry_audit",
        state_a=vector_to_string(state_a),
        state_b=vector_to_string(state_b),
        difference_vector=vector_to_string(difference),
        dot_product=round(dot(state_a, state_b), 12),
        cosine_similarity=round(cosine_similarity(state_a, state_b), 12),
        weighted_inner_product=round(weighted_inner_product(state_a, state_b, W), 12),
        norm_1=round(norm1(difference), 12),
        norm_2=round(norm2(difference), 12),
        norm_inf=round(norminf(difference), 12),
        euclidean_distance=round(norm2(difference), 12),
        weighted_distance=round(weighted_diff_magnitude, 12),
        interpretation_warning=(
            "State-space distance depends on units, scaling, norm choice, and weights. "
            "Weighted distances may reflect risk, uncertainty, cost, or priority, but those weights "
            "must be documented and translated back into domain terms."
        ),
    )


def write_outputs(output_dir: Path) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    audit = build_audit()
    row = asdict(audit)

    with (output_dir / "tables" / "state_space_geometry_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)

    (output_dir / "json" / "state_space_geometry_audit.json").write_text(
        json.dumps(row, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("State-space geometry audit complete.")


if __name__ == "__main__":
    main()
