A <- matrix(
  c(
    0.82, 0.12,
    0.18, 0.76
  ),
  nrow = 2,
  byrow = TRUE
)

state_names <- c("infrastructure_stress", "service_delay")
x0 <- c(10.0, 4.0)
horizon <- 20

trajectory <- matrix(NA, nrow = horizon + 1, ncol = length(x0))
trajectory[1, ] <- x0

for (t in seq_len(horizon)) {
  trajectory[t + 1, ] <- A %*% trajectory[t, ]
}

state_norms <- apply(trajectory, 1, function(row) sqrt(sum(row^2)))
eigen_values <- eigen(A)$values
spectral_radius <- max(Mod(eigen_values))

stability_classification <- ifelse(
  spectral_radius < 1,
  "asymptotically_stable_discrete_time",
  ifelse(abs(spectral_radius - 1) <= 1e-10, "boundary_or_marginal_discrete_time", "unstable_discrete_time")
)

audit_record <- data.frame(
  system_name = "two_state_linear_dynamics_audit",
  state_names = paste(state_names, collapse = "|"),
  update_matrix = paste(round(as.vector(t(A)), 6), collapse = ","),
  initial_state = paste(round(x0, 6), collapse = ","),
  horizon = horizon,
  final_state = paste(round(trajectory[horizon + 1, ], 6), collapse = ","),
  initial_norm = state_norms[1],
  final_norm = state_norms[horizon + 1],
  eigenvalues = paste(round(Re(eigen_values), 6), collapse = ","),
  spectral_radius = spectral_radius,
  stability_classification = stability_classification,
  interpretation_warning = paste(
    "Linear dynamics depend on state definitions, units, scaling, time step,",
    "matrix validity, constraint checks, and whether linearity is structural or approximate."
  )
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(audit_record, "outputs/tables/r_linear_dynamics_audit.csv", row.names = FALSE)

trajectory_record <- data.frame(
  step = 0:horizon,
  infrastructure_stress = trajectory[, 1],
  service_delay = trajectory[, 2],
  state_norm = state_norms
)

write.csv(trajectory_record, "outputs/tables/r_linear_dynamics_trajectory.csv", row.names = FALSE)
print(audit_record)
