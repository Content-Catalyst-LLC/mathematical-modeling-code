baseline <- matrix(
  c(
    10.0, 2.0, 0.0,
    1.0, 12.0, 3.0,
    0.0, 4.0, 8.0
  ),
  nrow = 3,
  byrow = TRUE
)

intervention_effect <- matrix(
  c(
    1.0, 0.5, 0.0,
    0.2, 1.5, 0.4,
    0.0, 0.7, 1.2
  ),
  nrow = 3,
  byrow = TRUE
)

stress_effect <- matrix(
  c(
    -0.5, -0.2, 0.0,
    -0.1, -0.8, -0.3,
    0.0, -0.4, -0.9
  ),
  nrow = 3,
  byrow = TRUE
)

same_shape <- identical(dim(baseline), dim(intervention_effect)) &&
  identical(dim(baseline), dim(stress_effect))

combined_change <- intervention_effect + 0.5 * stress_effect
future <- baseline + combined_change
difference <- future - baseline

audit_record <- data.frame(
  operation_name = "baseline_plus_weighted_intervention_and_stress",
  matrix_shape = paste(dim(baseline), collapse = "x"),
  row_meaning = "infrastructure subsystem",
  column_meaning = "performance relationship or dependency category",
  units = "normalized condition-effect score",
  weights = "1.0 intervention effect plus 0.5 stress effect",
  compatible_shape = same_shape,
  output_entry_sum = round(sum(difference), 4),
  interpretation_warning = paste(
    "The arithmetic is shape-compatible, but the weighted combination is meaningful",
    "only if rows, columns, units, baselines, and effect definitions align."
  )
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(audit_record, "outputs/tables/r_matrix_arithmetic_audit.csv", row.names = FALSE)
print(audit_record)
