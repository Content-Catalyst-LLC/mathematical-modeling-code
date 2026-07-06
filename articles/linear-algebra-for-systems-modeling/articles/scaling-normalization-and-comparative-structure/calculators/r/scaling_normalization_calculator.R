result <- data.frame(
  calculator = "scaling_normalization_and_comparative_structure_calculator",
  workflow_name = "scaling_normalization_audit",
  matrix_shape = "3x2",
  row_meaning = "infrastructure_zones",
  column_meaning = "annual_demand_and_outage_exposure",
  raw_column_norm_1 = 2345.207880,
  raw_column_norm_2 = 0.174929,
  standardized_column_norm_1 = 1.414214,
  standardized_column_norm_2 = 1.414214,
  first_row_sum_after_row_normalization = 1.0,
  first_row_norm_after_unit_normalization = 1.0,
  raw_condition_proxy = 13406.312329,
  standardized_condition_proxy = 1.0,
  warning = "Scaling and normalization change whether the model compares magnitude, relative position, composition, direction, probability, or numerical balance."
)

dir.create("outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(result, "outputs/r_scaling_normalization_and_comparative_structure_calculator.csv", row.names = FALSE)
print(result)
