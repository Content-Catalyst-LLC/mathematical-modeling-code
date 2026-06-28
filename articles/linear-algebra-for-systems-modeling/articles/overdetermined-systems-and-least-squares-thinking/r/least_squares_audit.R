A <- matrix(
  c(
    1, 1,
    1, 2,
    1, 3,
    1, 4
  ),
  nrow = 4,
  byrow = TRUE
)

b <- c(2.0, 2.9, 4.1, 5.1)

fit <- lm.fit(A, b)
solution <- fit$coefficients
fitted_values <- as.vector(A %*% solution)
residuals <- b - fitted_values
residual_norm <- sqrt(sum(residuals^2))
rank_A <- qr(A)$rank

audit_record <- data.frame(
  system_name = "four_observation_linear_calibration",
  row_count = nrow(A),
  column_count = ncol(A),
  overdetermined = nrow(A) > ncol(A),
  rank = rank_A,
  solution = paste(round(solution, 6), collapse = ","),
  fitted_values = paste(round(fitted_values, 6), collapse = ","),
  residuals = paste(round(residuals, 6), collapse = ","),
  residual_norm = residual_norm,
  solver_method = "R lm.fit QR-based least-squares workflow",
  interpretation_warning = paste(
    "Least squares fit should be reviewed with residuals,",
    "rank, conditioning, scaling, and model purpose."
  )
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(audit_record, "outputs/tables/r_least_squares_audit.csv", row.names = FALSE)
print(audit_record)
