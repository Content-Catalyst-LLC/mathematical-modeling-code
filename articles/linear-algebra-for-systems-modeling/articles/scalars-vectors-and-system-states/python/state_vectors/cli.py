from __future__ import annotations
import argparse, csv, json, math
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class StateComponent:
    position: int
    component_name: str
    value: float
    unit: str
    scale_type: str
    interpretation: str
    warning: str

COMPONENTS = [
    StateComponent(1, "road_condition", 72.0, "index_0_to_100", "raw_index", "Road network condition score.", "Index values should not be treated as physical units."),
    StateComponent(2, "bridge_condition", 68.0, "index_0_to_100", "raw_index", "Bridge system condition score.", "Comparable only if index construction is aligned."),
    StateComponent(3, "water_reliability", 0.91, "probability", "proportion", "Estimated reliability of water service.", "Probability scale differs from condition index scale."),
    StateComponent(4, "power_reliability", 0.96, "probability", "proportion", "Estimated reliability of power service.", "Do not directly add probability values to index scores."),
    StateComponent(5, "transit_capacity", 125000.0, "daily_passenger_capacity", "raw_count", "Estimated daily passenger capacity.", "Raw count can dominate vector magnitude without scaling."),
]

def euclidean_norm(values: list[float]) -> float:
    return math.sqrt(sum(value * value for value in values))

def l1_norm(values: list[float]) -> float:
    return sum(abs(value) for value in values)

def change_vector(next_values: list[float], current_values: list[float]) -> list[float]:
    if len(next_values) != len(current_values):
        raise ValueError("state vectors must have the same dimension")
    return [next_value - current_value for next_value, current_value in zip(next_values, current_values)]

def write_outputs(output_dir: Path) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    rows = [asdict(component) for component in COMPONENTS]
    values = [component.value for component in COMPONENTS]
    with (output_dir / "tables" / "state_vector_components.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    summary = {
        "state_name": "infrastructure_condition_state",
        "dimension": len(values),
        "raw_values": values,
        "raw_l1_norm": l1_norm(values),
        "raw_euclidean_norm": euclidean_norm(values),
        "audit_warning": "Raw norm is dominated by high-magnitude components. Use scaling before comparing distances or magnitudes."
    }
    (output_dir / "json" / "state_vector_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("State vector audit complete.")

if __name__ == "__main__":
    main()
