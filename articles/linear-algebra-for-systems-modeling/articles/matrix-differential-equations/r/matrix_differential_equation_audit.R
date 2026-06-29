A <- matrix(
  c(
    -0.28, 0.08,
     0.12, -0.34
  ),
  nrow = 2,
  byrow = TRUE
)

state_names <- c("infrastructure_stress", "service_delay")
x0 <- c(10.0, 4.0)
horizon <- 10.0
dt <- 0.01
steps <- as.integer(round(horizon / dt))

trajectory <- matrix(NA, nrow = steps + 1, ncol = length(x0))
trajectory[1, ] <- x0

for (k in seq_len(steps)) {
  dx <- A %*% trajectory[k, ]
  trajectory[k + 1, ] <- trajectory[k, ] + dt * as.numeric(dx)
}

state_norms <- apply(trajectory, 1, function(row) sqrt(sum(row^2)))
eigen_values <- eigen(A)$values
max_real_part <- max(Re(eigen_values))

stability_classification <- ifelse(
  max_real_part < 0,
  "asymptotically_stable_continuous_time",
  ifelse(abs(max_real_part) <= 1e-10, "boundary_or_marginal_continuous_time", "unstable_continuous_time")
)

audit_record <- data.frame(
  system_name = "two_state_matrix_differential_equation_audit",
  state_names = paste(state_names, collapse = "|"),
  system_matrix = paste(round(as.vector(t(A)), 6), collapse = ","),
  initial_state = paste(round(x0, 6), collapse = ","),
  time_horizon = horizon,
  final_state_estimate = paste(round(trajectory[steps + 1, ], 6), collapse = ","),
  initial_norm = state_norms[1],
  final_norm = state_norms[steps + 1],
  eigenvalues = paste(round(Re(eigen_values), 6), collapse = ","),
  max_real_part = max_real_part,
  stability_classification = stability_classification,
  interpretation_warning = paste(
    "Matrix differential equations require continuous-time stability rules,",
    "time-scale clarity, solver review, stiffness checks, and domain interpretation."
  )
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(audit_record, "outputs/tables/r_matrix_differential_equation_audit.csv", row.names = FALSE)

trajectory_record <- data.frame(
  time = seq(0, horizon, by = dt),
  infrastructure_stress = trajectory[, 1],
  service_delay = trajectory[, 2],
  state_norm = state_norms
)

write.csv(trajectory_record, "outputs/tables/r_matrix_differential_equation_trajectory.csv", row.names = FALSE)
print(audit_record)
