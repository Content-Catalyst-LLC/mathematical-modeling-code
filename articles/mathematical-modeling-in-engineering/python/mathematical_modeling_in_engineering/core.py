from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
import statistics


@dataclass(frozen=True)
class EngineeringModelRecord:
    key: str
    engineering_domain: str
    model_role: str
    model_family: str
    design_question: str
    status: str


@dataclass(frozen=True)
class BeamDesign:
    key: str
    width_m: float
    height_m: float
    span_m: float
    load_n: float
    allowable_stress_pa: float
    material_density_kg_m3: float


def load_engineering_model_records(path: Path) -> list[EngineeringModelRecord]:
    records: list[EngineeringModelRecord] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            records.append(
                EngineeringModelRecord(
                    key=row["key"],
                    engineering_domain=row["engineering_domain"],
                    model_role=row["model_role"],
                    model_family=row["model_family"],
                    design_question=row["design_question"],
                    status=row["status"],
                )
            )
    if not records:
        raise ValueError("Engineering model register cannot be empty.")
    return records


def load_beam_designs(path: Path) -> list[BeamDesign]:
    designs: list[BeamDesign] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            designs.append(
                BeamDesign(
                    key=row["key"],
                    width_m=float(row["width_m"]),
                    height_m=float(row["height_m"]),
                    span_m=float(row["span_m"]),
                    load_n=float(row["load_n"]),
                    allowable_stress_pa=float(row["allowable_stress_pa"]),
                    material_density_kg_m3=float(row["material_density_kg_m3"]),
                )
            )
    if not designs:
        raise ValueError("Beam design table cannot be empty.")
    return designs


def evaluate_beam(design: BeamDesign) -> dict[str, object]:
    # Simple center-point load model for a simply supported beam:
    # maximum bending moment M = P L / 4.
    # Rectangular section: I = b h^3 / 12, c = h / 2.
    moment = design.load_n * design.span_m / 4.0
    inertia = design.width_m * design.height_m**3 / 12.0
    c_value = design.height_m / 2.0
    stress = moment * c_value / inertia
    margin = design.allowable_stress_pa - stress
    safety_factor = design.allowable_stress_pa / stress if stress > 0 else float("inf")
    volume = design.width_m * design.height_m * design.span_m
    mass = volume * design.material_density_kg_m3

    return {
        **asdict(design),
        "bending_moment_nm": round(moment, 8),
        "second_moment_area_m4": round(inertia, 12),
        "max_stress_pa": round(stress, 8),
        "stress_margin_pa": round(margin, 8),
        "safety_factor": round(safety_factor, 8),
        "estimated_mass_kg": round(mass, 8),
        "passes_stress_constraint": stress <= design.allowable_stress_pa,
        "review_class": "acceptable" if stress <= design.allowable_stress_pa else "fails_constraint",
    }


def engineering_priority(record: EngineeringModelRecord) -> float:
    score = {"active": 1.0, "review": 5.0, "revise": 8.0, "archive": 2.0}.get(
        record.status.lower(),
        4.0,
    )
    text = f"{record.model_role} {record.model_family} {record.design_question}".lower()
    for term in ["safety", "validation", "uncertainty", "constraint", "optimization", "margin"]:
        if term in text:
            score += 1.0
    return round(score, 8)


def design_summary(rows: list[dict[str, object]]) -> dict[str, object]:
    if not rows:
        raise ValueError("Design summary requires at least one design row.")
    safety_factors = [float(row["safety_factor"]) for row in rows]
    masses = [float(row["estimated_mass_kg"]) for row in rows]
    failures = sum(1 for row in rows if not bool(row["passes_stress_constraint"]))
    acceptable_rows = [row for row in rows if bool(row["passes_stress_constraint"])]
    lightest_acceptable = min(acceptable_rows, key=lambda row: float(row["estimated_mass_kg"])) if acceptable_rows else None

    return {
        "mean_safety_factor": round(statistics.mean(safety_factors), 8),
        "min_safety_factor": round(min(safety_factors), 8),
        "max_safety_factor": round(max(safety_factors), 8),
        "mean_mass_kg": round(statistics.mean(masses), 8),
        "failed_design_count": failures,
        "design_count": len(rows),
        "lightest_acceptable_design": None if lightest_acceptable is None else lightest_acceptable["key"],
    }


def build_engineering_design_review_card(
    register_rows: list[dict[str, object]],
    design_rows: list[dict[str, object]],
) -> dict[str, object]:
    return {
        "article": "Mathematical Modeling in Engineering",
        "design_summary": design_summary(design_rows),
        "engineering_model_register": register_rows,
        "beam_design_review": design_rows,
        "use_limit": "This simplified beam workflow is illustrative and does not replace engineering standards, professional review, detailed structural analysis, or applicable design codes.",
        "diagnostic_checks": [
            "requirements and constraints are stated",
            "stress margin is computed",
            "failed designs are flagged",
            "tradeoff between mass and safety is visible",
            "validation evidence is required before use",
            "use limits are stated explicitly",
        ],
    }


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"No rows supplied for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
