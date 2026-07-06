result <- data.frame(
  calculator = "case_study_infrastructure_interdependence_calculator",
  workflow_name = "infrastructure_interdependence_audit",
  scenario_name = "synthetic_power_disruption_dependency_scenario",
  sector_count = 5,
  initial_shock_sector = "power",
  initial_shock_magnitude = 0.40,
  highest_dependency_burden_sector = "power",
  highest_dependency_burden = 2.40,
  largest_downstream_loss_sector = "health",
  largest_downstream_loss = 0.32,
  total_estimated_downstream_loss = 0.96,
  warning = "Dependency weights are scenario assumptions and cascade estimates require validation."
)

dir.create("outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(result, "outputs/r_case_study_infrastructure_interdependence_calculator.csv", row.names = FALSE)
print(result)
