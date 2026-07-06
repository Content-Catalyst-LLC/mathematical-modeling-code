result <- data.frame(
  calculator = "representation_choices_and_model_assumptions_calculator",
  workflow_name = "representation_assumption_audit",
  matrix_shape = "3x2",
  row_meaning = "infrastructure_zones",
  column_meaning = "annual_demand_and_outage_exposure",
  value_meaning = "mixed_units_before_standardization",
  zero_meaning = "zero_would_mean_measured_absence_not_missingness",
  raw_column_norm_1 = 2345.207880,
  raw_column_norm_2 = 0.174929,
  standardized_column_norm_1 = 1.414214,
  standardized_column_norm_2 = 1.414214,
  warning = "Representation choices define what the model can compare, reveal, hide, and justify."
)

dir.create("outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(result, "outputs/r_representation_choices_and_model_assumptions_calculator.csv", row.names = FALSE)
print(result)
