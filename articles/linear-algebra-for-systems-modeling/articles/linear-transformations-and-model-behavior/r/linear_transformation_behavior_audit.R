A <- matrix(
  c(
    1.20, 0.10, 0.00,
    0.20, 0.85, 0.15,
    0.00, 0.25, 0.90
  ),
  nrow = 3,
  byrow = TRUE
)

x <- c(100, 60, 30)
y <- as.vector(A %*% x)

input_norm <- sqrt(sum(x^2))
output_norm <- sqrt(sum(y^2))
amplification_ratio <- output_norm / input_norm
rank_A <- qr(A)$rank
nullity_A <- ncol(A) - rank_A

behavior_warning <- if (amplification_ratio > 1.10) {
  "transformation amplifies this input state"
} else if (amplification_ratio < 0.90) {
  "transformation dampens this input state"
} else {
  "transformation keeps this input norm at a similar scale"
}

audit_record <- data.frame(
  system_name = "three_component_system_response",
  row_count = nrow(A),
  column_count = ncol(A),
  input_state = paste(round(x, 6), collapse = ","),
  output_state = paste(round(y, 6), collapse = ","),
  rank = rank_A,
  nullity = nullity_A,
  input_norm = input_norm,
  output_norm = output_norm,
  amplification_ratio = amplification_ratio,
  behavior_warning = behavior_warning,
  interpretation_warning = paste(
    "Matrix action should be interpreted with row meanings, column meanings,",
    "units, scaling, linearity assumptions, and sensitivity review."
  )
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(audit_record, "outputs/tables/r_linear_transformation_behavior_audit.csv", row.names = FALSE)
print(audit_record)
