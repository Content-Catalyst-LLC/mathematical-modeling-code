from __future__ import annotations
import argparse, csv, json, math
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class SpatialAccumulationRecord:
    scenario: str
    cells_in_region: int
    cell_area: float
    total_area: float
    total_density_accumulation: float
    area_weighted_average: float
    population_weighted_burden: float
    population_total: float
    population_weighted_average_exposure: float
    warning: str

def exposure_field(x: float, y: float) -> float:
    return 10.0 + 2.0 * x + 0.5 * y * y

def population_density(x: float, y: float) -> float:
    return 100.0 + 10.0 * y + 5.0 * math.sin(x)

def in_region(x: float, y: float) -> bool:
    return x * x + y * y <= 9.0

def grid_values(step: float) -> list[float]:
    return [round(-3.0 + i * step, 10) for i in range(int(6.0 / step) + 1)]

def compute_spatial_accumulation(step: float, scenario: str) -> SpatialAccumulationRecord:
    xs = grid_values(step)
    ys = grid_values(step)
    cell_area = step * step
    cells = 0
    total_density = 0.0
    total_population = 0.0
    population_burden = 0.0

    for x in xs:
        for y in ys:
            if in_region(x, y):
                exposure = exposure_field(x, y)
                population = population_density(x, y)
                cells += 1
                total_density += exposure * cell_area
                total_population += population * cell_area
                population_burden += exposure * population * cell_area

    total_area = cells * cell_area
    area_weighted_average = total_density / total_area
    population_weighted_average = population_burden / total_population

    warning = (
        "Grid resolution is coarse; spatial accumulation may smooth local variation."
        if step > 0.5
        else "Synthetic grid audit; region mask, cell area, and units should be documented."
    )

    return SpatialAccumulationRecord(
        scenario=scenario,
        cells_in_region=cells,
        cell_area=cell_area,
        total_area=total_area,
        total_density_accumulation=total_density,
        area_weighted_average=area_weighted_average,
        population_weighted_burden=population_burden,
        population_total=total_population,
        population_weighted_average_exposure=population_weighted_average,
        warning=warning,
    )

def write_outputs(output_dir: Path, records: list[SpatialAccumulationRecord]) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    rows = [asdict(r) for r in records]
    with (output_dir / "tables" / "spatial_accumulation_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (output_dir / "json" / "spatial_accumulation_audit.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    records = [
        compute_spatial_accumulation(1.0, "coarse_grid"),
        compute_spatial_accumulation(0.5, "medium_grid"),
        compute_spatial_accumulation(0.25, "fine_grid"),
    ]
    write_outputs(args.output_dir, records)
    print("Spatial accumulation audit complete.")

if __name__ == "__main__":
    main()
