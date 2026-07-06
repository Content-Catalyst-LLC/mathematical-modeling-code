A_raw <- matrix(
  c(
    1200.0, 0.08,
    1800.0, 0.15,
    900.0, 0.04
  ),
  nrow = 3,
  byrow = TRUE
)

colnames(A_raw) <- c("annual_demand", "outage_exposure")
rownames(A_raw) <- c("zone_a", "zone_b", "zone_c")

A_standardized <- scale(A_raw)
norm2 <- function(x) sqrt(sum(x^2))

audit_record <- data.frame(
  workflow_name = "representation_assumption_audit",
  matrix_shape = paste(dim(A_raw), collapse = "x"),
  row_meaning = "infrastructure_zones",
  column_meaning = "annual_demand_and_outage_exposure",
  value_meaning = "mixed_units_before_standardization",
  zero_meaning = "zero_would_mean_measured_absence_not_missingness",
  missing_value_rule = "missing_values_must_not_be_encoded_as_zero_without_flag",
  raw_column_norm_1 = norm2(A_raw[, 1]),
  raw_column_norm_2 = norm2(A_raw[, 2]),
  standardized_column_norm_1 = norm2(A_standardized[, 1]),
  standardized_column_norm_2 = norm2(A_standardized[, 2]),
  representation_change_warning = paste(
    "Standardization improves comparability but changes interpretation",
    "from original units to relative position."
  ),
  interpretation_warning = paste(
    "Representation choices define what the model can compare, reveal, and hide.",
    "Rows, columns, units, zeros, scaling, missingness, and boundaries should",
    "be documented before computation."
  )
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(audit_record, "outputs/tables/r_representation_assumption_audit.csv", row.names = FALSE)
print(audit_record)
