A <- matrix(
  c(
    0.796667, 0.123333,
    0.246667, 0.673333
  ),
  nrow = 2,
  byrow = TRUE
)

eigen_result <- eigen(A)

P <- eigen_result$vectors
D <- diag(eigen_result$values)
P_inv <- solve(P)

A_reconstructed <- P %*% D %*% P_inv
reconstruction_error_frobenius <- sqrt(sum((A - A_reconstructed)^2))

spectral_radius <- max(Mod(eigen_result$values))
dominant_index <- which.max(Mod(eigen_result$values))
dominant_eigenvalue <- eigen_result$values[dominant_index]

x0 <- c(10, 4)
modal_coordinates <- P_inv %*% x0

stability_classification <- ifelse(
  spectral_radius < 1,
  "all_modes_decay_discrete_time",
  ifelse(abs(spectral_radius - 1) <= 1e-10, "persistent_or_marginal_mode_present", "amplifying_mode_present")
)

audit_record <- data.frame(
  system_name = "two_mode_diagonalization_audit",
  matrix_entries = paste(round(as.vector(t(A)), 6), collapse = ","),
  eigenvalues = paste(round(Re(eigen_result$values), 6), collapse = ","),
  reconstruction_error_frobenius = reconstruction_error_frobenius,
  spectral_radius = spectral_radius,
  dominant_eigenvalue = Re(dominant_eigenvalue),
  modal_coordinates = paste(round(Re(modal_coordinates), 6), collapse = ","),
  stability_classification = stability_classification,
  interpretation_warning = paste(
    "Diagonalization decouples the representation, not necessarily the real system.",
    "Check cond(P), eigenpair residuals, spectral gaps, scaling, and domain meaning."
  )
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(audit_record, "outputs/tables/r_diagonalization_audit.csv", row.names = FALSE)
print(audit_record)
