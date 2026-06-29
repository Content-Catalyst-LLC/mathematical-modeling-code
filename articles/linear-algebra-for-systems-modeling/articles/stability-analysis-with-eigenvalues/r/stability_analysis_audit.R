A <- matrix(
  c(
    0.82, 0.12,
    0.18, 0.76
  ),
  nrow = 2,
  byrow = TRUE
)

eigen_result <- eigen(A)
eigenvalues <- eigen_result$values

spectral_radius <- max(Mod(eigenvalues))
largest_real_part <- max(Re(eigenvalues))
dominant_index <- which.max(Mod(eigenvalues))
dominant_eigenvalue <- eigenvalues[dominant_index]
dominant_eigenvector <- eigen_result$vectors[, dominant_index]

discrete_time_classification <- ifelse(
  spectral_radius < 1,
  "asymptotically_stable_discrete_time",
  ifelse(abs(spectral_radius - 1) <= 1e-10, "boundary_or_marginal_discrete_time", "unstable_discrete_time")
)

continuous_time_classification <- ifelse(
  largest_real_part < 0,
  "asymptotically_stable_continuous_time",
  ifelse(abs(largest_real_part) <= 1e-10, "boundary_or_marginal_continuous_time", "unstable_continuous_time")
)

audit_record <- data.frame(
  system_name = "two_mode_stability_audit",
  matrix_entries = paste(round(as.vector(t(A)), 6), collapse = ","),
  eigenvalues = paste(round(Re(eigenvalues), 6), collapse = ","),
  spectral_radius = spectral_radius,
  largest_real_part = largest_real_part,
  dominant_eigenvalue = Re(dominant_eigenvalue),
  dominant_eigenvector = paste(round(Re(dominant_eigenvector), 6), collapse = ","),
  discrete_time_classification = discrete_time_classification,
  continuous_time_classification = continuous_time_classification,
  interpretation_warning = paste(
    "Discrete-time stability uses eigenvalue magnitudes relative to one.",
    "Continuous-time stability uses eigenvalue real parts relative to zero."
  )
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(audit_record, "outputs/tables/r_stability_analysis_audit.csv", row.names = FALSE)
print(audit_record)
