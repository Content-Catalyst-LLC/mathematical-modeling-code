result <- data.frame(
  calculator = "economic_input_output_models_calculator",
  model_name = "synthetic_economic_input_output_audit",
  sectors = 4,
  method = "demand_driven_leontief_input_output_system",
  coefficient_basis = "sector_input_per_unit_output",
  condition_number = 2.41,
  maximum_output_multiplier = 1.47,
  highest_multiplier_sector = "manufacturing",
  total_baseline_output = 319.8,
  total_shock_output_change = 36.2,
  total_emissions_for_final_demand = 150.6,
  warning = "Input-output metrics depend on sector classification, accounting boundary, coefficient construction, final demand scenario, environmental extensions, sensitivity testing, and interpretation context."
)

dir.create("outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(result, "outputs/r_economic_input_output_models_calculator.csv", row.names = FALSE)
print(result)
