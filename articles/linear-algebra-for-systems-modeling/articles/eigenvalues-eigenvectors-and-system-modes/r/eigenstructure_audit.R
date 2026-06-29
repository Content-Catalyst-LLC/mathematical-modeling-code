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
eigenvectors <- eigen_result$vectors

spectral_radius <- max(Mod(eigenvalues))
dominant_index <- which.max(Mod(eigenvalues))
dominant_eigenvalue <- eigenvalues[dominant_index]
dominant_eigenvector <- eigenvectors[, dominant_index]

residual <- A %*% dominant_eigenvector - as.numeric(dominant_eigenvalue) * dominant_eigenvector
eigenpair_residual_norm <- sqrt(sum(Mod(residual)^2))

stability_classification <- ifelse(
  spectral_radius < 1,
  "asymptotically_damped_discrete_time",
  ifelse(abs(spectral_radius - 1) <= 1e-10, "marginal_or_persistent_discrete_time", "amplifying_or_unstable_discrete_time")
)

audit_record <- data.frame(
  system_name = "two_sector_mode_audit",
  matrix_entries = paste(round(as.vector(t(A)), 6), collapse = ","),
  eigenvalues = paste(round(Re(eigenvalues), 6), collapse = ","),
  spectral_radius = spectral_radius,
  dominant_eigenvalue = Re(dominant_eigenvalue),
  dominant_eigenvector = paste(round(Re(dominant_eigenvector), 6), collapse = ","),
  eigenpair_residual_norm = eigenpair_residual_norm,
  stability_classification = stability_classification,
  interpretation_warning = paste(
    "Eigenvalues describe modes of the specified matrix, not automatic causal mechanisms.",
    "Mode interpretation depends on matrix construction, units, scaling, and domain meaning."
  )
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(audit_record, "outputs/tables/r_eigenstructure_audit.csv", row.names = FALSE)
print(audit_record)
