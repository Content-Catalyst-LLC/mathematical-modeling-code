result <- data.frame(
  calculator = "case_study_economic_input_output_analysis_calculator",
  workflow_name = "economic_input_output_audit",
  economy_name = "synthetic_three_sector_economy",
  sector_count = 3,
  final_demand_total = 450.0,
  gross_output_total = 763.099081201887,
  highest_multiplier_sector = "manufacturing",
  highest_output_multiplier = 1.951825177111,
  shock_sector = "manufacturing",
  shock_amount = 25.0,
  gross_output_change_total = 48.795629500869,
  leontief_infinity_condition_estimate = 2.147504345667,
  warning = "Input-output multipliers are fixed-coefficient scenario outputs, not automatic policy conclusions."
)

dir.create("outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(result, "outputs/r_case_study_economic_input_output_analysis_calculator.csv", row.names = FALSE)
print(result)
