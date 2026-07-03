set.seed(20260629)

state_dimension <- 24
time_steps <- 40
ensemble_runs <- 250

build_transition <- function(n, coupling = 0.08) {
  A <- matrix(0, nrow = n, ncol = n)
  for (i in seq_len(n)) {
    A[i, i] <- 0.82
    if (i > 1) A[i, i - 1] <- coupling
    if (i < n) A[i, i + 1] <- coupling
    if (i + 5 <= n) A[i, i + 5] <- coupling / 3
  }
  radius <- max(Mod(eigen(A)$values))
  if (radius >= 0.98) A <- A / (radius + 0.05)
  A
}

A <- build_transition(state_dimension)
covariance <- 0.015 * diag(state_dimension)
for (i in 1:(state_dimension - 1)) {
  covariance[i, i + 1] <- 0.006
  covariance[i + 1, i] <- 0.006
}

base_state <- seq(1.0, 2.5, length.out = state_dimension)

simulate_one <- function() {
  x <- base_state + rnorm(state_dimension, mean = 0, sd = 0.05)
  for (t in 1:time_steps) {
    shock <- as.numeric(t(chol(covariance)) %*% rnorm(state_dimension))
    input_vector <- 0.03 * sin(t / 6.0) * rep(1, state_dimension)
    x <- A %*% x + input_vector + shock
    x <- pmax(as.numeric(x), 0)
  }
  x
}

final_states <- t(replicate(ensemble_runs, simulate_one()))
final_totals <- rowSums(final_states)
centered <- scale(final_states, center = TRUE, scale = FALSE)
svd_result <- svd(centered)
energy_share <- svd_result$d^2 / sum(svd_result$d^2)
transition_density <- sum(A != 0) / length(A)

audit_record <- data.frame(
  model_name = "synthetic_high_dimensional_simulation_audit",
  state_dimension = state_dimension,
  time_steps = time_steps,
  ensemble_runs = ensemble_runs,
  method = "sparse_linear_state_update_with_correlated_monte_carlo_shocks",
  random_seed = 20260629,
  transition_spectral_radius = max(Mod(eigen(A)$values)),
  transition_density = transition_density,
  final_state_mean_norm = sqrt(sum(colMeans(final_states)^2)),
  final_state_mean_total = mean(final_totals),
  final_state_95th_percentile_total = as.numeric(quantile(final_totals, 0.95)),
  threshold_exceedance_probability = mean(final_totals > quantile(final_totals, 0.90)),
  first_three_component_energy = sum(energy_share[1:3]),
  validation_warning = paste(
    "Simulation results depend on state representation, transition structure,",
    "random seed, shock distribution, covariance, time step, ensemble size, and validation evidence."
  ),
  interpretation_warning = paste(
    "High-dimensional simulation outputs are conditional model outcomes,",
    "not observations of the future."
  )
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(audit_record, "outputs/tables/r_high_dimensional_simulation_audit.csv", row.names = FALSE)
write.csv(data.frame(run_id = seq_along(final_totals) - 1, final_total = final_totals),
          "outputs/tables/r_ensemble_final_totals.csv",
          row.names = FALSE)
write.csv(data.frame(component = seq_along(svd_result$d),
                     singular_value = svd_result$d,
                     energy_share = energy_share),
          "outputs/tables/r_final_state_svd_energy.csv",
          row.names = FALSE)
print(audit_record)
