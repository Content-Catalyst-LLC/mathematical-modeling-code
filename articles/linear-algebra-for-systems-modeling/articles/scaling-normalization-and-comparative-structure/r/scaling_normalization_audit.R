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

norm2 <- function(x) sqrt(sum(x^2))

minmax_columns <- function(A) {
  apply(A, 2, function(col) {
    rng <- max(col) - min(col)
    if (rng == 0) rep(0, length(col)) else (col - min(col)) / rng
  })
}

row_sum_normalize <- function(A) {
  totals <- rowSums(A)
  totals[totals == 0] <- 1
  A / totals
}

unit_row_normalize <- function(A) {
  norms <- apply(A, 1, norm2)
  norms[norms == 0] <- 1
  A / norms
}

condition_proxy <- function(A) {
  column_norms <- apply(A, 2, norm2)
  max(column_norms) / max(min(column_norms), 1e-15)
}

A_standardized <- scale(A_raw)
A_minmax <- minmax_columns(A_raw)
A_row_sum <- row_sum_normalize(A_raw)
A_unit_rows <- unit_row_normalize(A_raw)

audit_record <- data.frame(
  workflow_name = "scaling_normalization_audit",
  matrix_shape = paste(dim(A_raw), collapse = "x"),
  row_meaning = "infrastructure_zones",
  column_meaning = "annual_demand_and_outage_exposure",
  raw_column_norm_1 = norm2(A_raw[, 1]),
  raw_column_norm_2 = norm2(A_raw[, 2]),
  standardized_column_norm_1 = norm2(A_standardized[, 1]),
  standardized_column_norm_2 = norm2(A_standardized[, 2]),
  minmax_column_min_1 = min(A_minmax[, 1]),
  minmax_column_max_1 = max(A_minmax[, 1]),
  first_row_sum_after_row_normalization = sum(A_row_sum[1, ]),
  first_row_norm_after_unit_normalization = norm2(A_unit_rows[1, ]),
  raw_condition_proxy = condition_proxy(A_raw),
  standardized_condition_proxy = condition_proxy(A_standardized),
  comparison_warning = paste(
    "Raw units compare magnitude; standardized columns compare relative position;",
    "row normalization compares composition; unit-vector normalization compares direction."
  ),
  interpretation_warning = paste(
    "Scaling and normalization change what comparison means.",
    "Every transformed matrix should record original units, transformation rule,",
    "purpose, and interpretation limits."
  )
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(audit_record, "outputs/tables/r_scaling_normalization_audit.csv", row.names = FALSE)
print(audit_record)
