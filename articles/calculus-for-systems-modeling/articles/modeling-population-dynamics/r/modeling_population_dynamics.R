exponential_population <- function(n0, r, t) n0 * exp(r * t)
logistic_population <- function(n0, r, k, t) k / (1 + ((k - n0) / n0) * exp(-r * t))
simulate_ode <- function(n0, derivative, dt, steps) {
  n <- n0
  for (i in seq_len(steps)) n <- max(0, n + dt * derivative(n))
  n
}
stochastic_logistic <- function(n0, r, k, sigma, dt, steps, seed = 7) {
  set.seed(seed); n <- n0
  for (i in seq_len(steps)) n <- max(0, n + r*n*(1-n/k)*dt + sigma*n*sqrt(dt)*rnorm(1))
  n
}
n0 <- 100; r <- 0.08; k <- 1000; a <- 75; h <- 12; dt <- 0.1; steps <- 400
scenario_records <- data.frame(
  scenario_name = c("exponential_baseline","logistic_capacity_limited","allee_threshold","harvesting_pressure","stochastic_logistic_path"),
  model_type = c("exponential","logistic","allee_effect","harvesting","stochastic"),
  final_population = c(
    exponential_population(n0, r, 40),
    logistic_population(n0, r, k, 40),
    simulate_ode(n0, function(n) r*n*(1-n/k)*(n/a-1), dt, steps),
    simulate_ode(n0, function(n) r*n*(1-n/k)-h, dt, steps),
    stochastic_logistic(n0, r, k, 0.12, dt, steps)
  ),
  warning = c("unconstrained baseline","capacity-limited assumption","threshold-dependent recovery","management/removal assumption","single stochastic path")
)
dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(scenario_records, "outputs/tables/r_population_advanced_scenarios.csv", row.names = FALSE)
print(scenario_records)
