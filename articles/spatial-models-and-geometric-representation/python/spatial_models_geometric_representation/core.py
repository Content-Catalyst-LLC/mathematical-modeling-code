from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
import math


@dataclass(frozen=True)
class SpatialRecord:
    key: str
    component_type: str
    geometry_or_structure: str
    interpretation: str
    review_question: str
    status: str


@dataclass(frozen=True)
class Location:
    key: str
    kind: str
    x: float
    y: float
    value: float


def validate_location(location: Location) -> None:
    if location.kind not in {"demand", "service"}:
        raise ValueError("Location kind must be demand or service.")
    if not math.isfinite(location.x) or not math.isfinite(location.y):
        raise ValueError("Location coordinates must be finite.")
    if location.value < 0:
        raise ValueError("Location value must be nonnegative.")


def euclidean_distance(a: Location, b: Location) -> float:
    validate_location(a)
    validate_location(b)
    return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)


def accessibility_rows(locations: list[Location]) -> list[dict[str, object]]:
    demand = [item for item in locations if item.kind == "demand"]
    services = [item for item in locations if item.kind == "service"]

    if not demand:
        raise ValueError("At least one demand location is required.")
    if not services:
        raise ValueError("At least one service location is required.")

    rows: list[dict[str, object]] = []
    for area in demand:
        nearest_service = min(services, key=lambda service: euclidean_distance(area, service))
        nearest_distance = euclidean_distance(area, nearest_service)
        accessibility = sum(service.value / (1.0 + euclidean_distance(area, service)) for service in services)
        low_access_exposure = area.value / (1.0 + accessibility)

        rows.append({
            "demand_location": area.key,
            "population_or_demand": round(area.value, 8),
            "nearest_service": nearest_service.key,
            "nearest_distance": round(nearest_distance, 8),
            "accessibility_score": round(accessibility, 8),
            "low_access_exposure_score": round(low_access_exposure, 8),
        })

    return rows


def spatial_risk_score(record: SpatialRecord) -> float:
    score = {"active": 1.0, "review": 5.0, "revise": 8.0, "archive": 2.0}.get(
        record.status.lower(),
        4.0,
    )
    text = f"{record.component_type} {record.geometry_or_structure} {record.review_question}".lower()
    for term in ["distance", "geometry", "access", "boundary", "scale", "uncertainty", "coordinate"]:
        if term in text:
            score += 1.0
    return round(score, 8)


def load_records(path: Path) -> list[SpatialRecord]:
    records: list[SpatialRecord] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            records.append(
                SpatialRecord(
                    key=row["key"],
                    component_type=row["component_type"],
                    geometry_or_structure=row["geometry_or_structure"],
                    interpretation=row["interpretation"],
                    review_question=row["review_question"],
                    status=row["status"],
                )
            )
    return records


def load_locations(path: Path) -> list[Location]:
    locations: list[Location] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            location = Location(
                key=row["key"],
                kind=row["kind"],
                x=float(row["x"]),
                y=float(row["y"]),
                value=float(row["value"]),
            )
            validate_location(location)
            locations.append(location)
    return locations


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


def build_spatial_audit_card(
    records: list[SpatialRecord],
    locations: list[Location],
    access_rows: list[dict[str, object]],
) -> dict[str, object]:
    register_rows = [
        {**asdict(record), "spatial_risk_score": spatial_risk_score(record)}
        for record in records
    ]

    return {
        "article": "Spatial Models and Geometric Representation",
        "location_count": len(locations),
        "demand_location_count": sum(1 for location in locations if location.kind == "demand"),
        "service_location_count": sum(1 for location in locations if location.kind == "service"),
        "records": register_rows,
        "accessibility_diagnostics": access_rows,
        "high_priority_spatial_records": [
            row for row in register_rows if float(row["spatial_risk_score"]) >= 8.0
        ],
        "audit_checks": [
            "coordinate system is documented",
            "geometry type matches model purpose",
            "distance metric is justified",
            "scale and aggregation are reviewed",
            "spatial uncertainty is communicated",
        ],
    }
