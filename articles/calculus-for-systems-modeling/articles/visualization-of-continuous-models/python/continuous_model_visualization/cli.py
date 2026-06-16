from __future__ import annotations
import argparse, csv, json, math
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class TrajectoryRecord:
    scenario: str
    time: float
    value: float
    growth_rate: float
    carrying_capacity: float
    warning: str

@dataclass(frozen=True)
class VisualizationAuditRecord:
    figure_id: str
    visual_type: str
    model_object: str
    x_axis: str
    y_axis: str
    scale_note: str
    uncertainty_note: str
    interpretation_warning: str

def logistic_solution(t: float, x0: float, growth_rate: float, carrying_capacity: float) -> float:
    if x0 <= 0 or carrying_capacity <= 0:
        raise ValueError("x0 and carrying_capacity must be positive")
    return carrying_capacity / (1.0 + ((carrying_capacity - x0) / x0) * math.exp(-growth_rate * t))

def build_trajectories() -> list[TrajectoryRecord]:
    scenarios = [
        ("low_growth", 0.18, 100.0),
        ("baseline", 0.35, 100.0),
        ("high_growth", 0.55, 100.0),
    ]
    records: list[TrajectoryRecord] = []
    for scenario, r, k in scenarios:
        for step in range(0, 81):
            t = step * 0.25
            records.append(TrajectoryRecord(
                scenario=scenario,
                time=t,
                value=logistic_solution(t, x0=10.0, growth_rate=r, carrying_capacity=k),
                growth_rate=r,
                carrying_capacity=k,
                warning="Trajectory visualization depends on equation, initial condition, parameters, time horizon, axis scale, and scenario selection."
            ))
    return records

def build_audit_records() -> list[VisualizationAuditRecord]:
    return [
        VisualizationAuditRecord(
            "logistic_growth_scenario_trajectories",
            "trajectory_plot",
            "logistic_solution",
            "time",
            "state value",
            "Linear axes; time horizon 0 to 20.",
            "Scenario lines are parameter contrasts, not probability intervals.",
            "The figure shows model-implied trajectories under selected assumptions, not empirical forecasts."
        ),
        VisualizationAuditRecord(
            "phase_portrait_review",
            "phase_portrait",
            "two_state_dynamic_system",
            "state x",
            "state y",
            "State-space window should be documented.",
            "Initial condition selection affects visible trajectories.",
            "Phase portraits show local and geometric behavior, not automatic empirical validity."
        ),
        VisualizationAuditRecord(
            "vector_field_review",
            "vector_field",
            "spatial_flow_field",
            "x coordinate",
            "y coordinate",
            "Arrow scaling should be documented.",
            "Magnitude and direction can be visually distorted by normalization.",
            "Vector fields require unit and boundary interpretation."
        ),
        VisualizationAuditRecord(
            "uncertainty_band_review",
            "uncertainty_band",
            "scenario_spread",
            "time",
            "state value",
            "Band should share axis scale with central trajectory.",
            "The band meaning must be specified: scenario range, confidence interval, or sensitivity envelope.",
            "Uncertainty visualization can imply probability without support if not defined."
        ),
        VisualizationAuditRecord(
            "diagnostic_plot_review",
            "diagnostic_plot",
            "solver_error_or_residuals",
            "time or step",
            "error or residual",
            "Diagnostic axis and units should be explicit.",
            "Diagnostics should be preserved with primary figures.",
            "A clean primary graph may hide numerical artifacts without diagnostics."
        ),
    ]

def write_svg(output_dir: Path, records: list[TrajectoryRecord]) -> None:
    """Write a simple dependency-free SVG line sketch for review."""
    figure_dir = output_dir / "figures"
    figure_dir.mkdir(parents=True, exist_ok=True)
    width, height = 760, 420
    margin = 55
    max_time = max(r.time for r in records)
    max_value = max(r.value for r in records)
    groups = {}
    for record in records:
        groups.setdefault(record.scenario, []).append(record)

    def sx(t: float) -> float:
        return margin + (width - 2 * margin) * (t / max_time)

    def sy(v: float) -> float:
        return height - margin - (height - 2 * margin) * (v / max_value)

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<line x1="{margin}" y1="{height-margin}" x2="{width-margin}" y2="{height-margin}" stroke="black" stroke-width="1"/>',
        f'<line x1="{margin}" y1="{margin}" x2="{margin}" y2="{height-margin}" stroke="black" stroke-width="1"/>',
        '<text x="55" y="30" font-size="16">Logistic growth scenario trajectories</text>',
    ]
    dash_patterns = ["", "5,4", "2,4"]
    for idx, (scenario, rows) in enumerate(sorted(groups.items())):
        points = " ".join(f"{sx(r.time):.2f},{sy(r.value):.2f}" for r in rows)
        dash = f' stroke-dasharray="{dash_patterns[idx % len(dash_patterns)]}"' if dash_patterns[idx % len(dash_patterns)] else ""
        lines.append(f'<polyline points="{points}" fill="none" stroke="black" stroke-width="2"{dash}/>')
        lines.append(f'<text x="{width-margin-160}" y="{margin + idx*20}" font-size="12">{scenario}</text>')
    lines.append('<text x="330" y="400" font-size="12">Time</text>')
    lines.append('<text x="10" y="210" font-size="12" transform="rotate(-90 10,210)">State value</text>')
    lines.append('</svg>')
    (figure_dir / "logistic_growth_scenario_trajectories.svg").write_text("\n".join(lines) + "\n", encoding="utf-8")

def write_outputs(output_dir: Path) -> None:
    records = build_trajectories()
    audit_records = build_audit_records()
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)

    trajectory_rows = [asdict(record) for record in records]
    audit_rows = [asdict(record) for record in audit_records]

    with (output_dir / "tables" / "continuous_model_trajectories.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(trajectory_rows[0].keys()))
        writer.writeheader()
        writer.writerows(trajectory_rows)

    with (output_dir / "tables" / "visualization_audit_records.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(audit_rows[0].keys()))
        writer.writeheader()
        writer.writerows(audit_rows)

    (output_dir / "json" / "continuous_model_trajectories.json").write_text(json.dumps(trajectory_rows, indent=2, sort_keys=True), encoding="utf-8")
    (output_dir / "json" / "visualization_audit_records.json").write_text(json.dumps(audit_rows, indent=2, sort_keys=True), encoding="utf-8")

    report_lines = ["# Visualization Audit Records\n"]
    for record in audit_records:
        report_lines.append(f"- **{record.figure_id}** ({record.visual_type}): {record.interpretation_warning}")
    (output_dir / "reports" / "visualization_audit_records.md").write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    write_svg(output_dir, records)

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Continuous model visualization audit outputs generated.")

if __name__ == "__main__":
    main()
