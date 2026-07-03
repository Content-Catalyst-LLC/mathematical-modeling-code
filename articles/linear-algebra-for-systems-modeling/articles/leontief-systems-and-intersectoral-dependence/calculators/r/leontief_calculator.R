result <- data.frame(
  calculator = "leontief_systems_and_intersectoral_dependence_calculator",
  model_name = "synthetic_leontief_intersectoral_dependence_audit",
  sectors = 4,
  method = "demand_driven_leontief_system",
  coefficient_basis = "sector_input_per_unit_output",
  spectral_radius = 0.331,
  condition_number = 2.41,
  productive_system_flag = TRUE,
  maximum_output_multiplier = 1.47,
  highest_multiplier_sector = "manufacturing",
  total_output_required = 319.8,
  total_shock_output_change = 36.2,
  emissions_for_final_demand = 150.6,
  warning = "Leontief metrics depend on coefficient construction, productivity conditions, matrix conditioning, scenario definition, environmental extensions, sensitivity testing, and interpretation context."
)

dir.create("outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(result, "outputs/r_leontief_systems_and_intersectoral_dependence_calculator.csv", row.names = FALSE)
print(result)
