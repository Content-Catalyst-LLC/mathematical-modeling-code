exponential_solution <- function(t, x0, r) x0 * exp(r * t)
exponential_rate <- function(x, r) r * x
logistic_solution <- function(t, x0, r, capacity) capacity / (1 + ((capacity - x0) / x0) * exp(-r * t))
logistic_rate <- function(x, r, capacity) r * x * (1 - x / capacity)
simulate_model <- function(kind, x0, r, capacity = NA, dt = 0.1, steps = 100) {
  x <- x0; rows <- list()
  for (n in 0:steps) {
    t <- n * dt
    analytical <- if (kind == 'exponential') exponential_solution(t, x0, r) else logistic_solution(t, x0, r, capacity)
    rate <- if (kind == 'exponential') exponential_rate(x, r) else logistic_rate(x, r, capacity)
    rows[[length(rows)+1]] <- data.frame(scenario=paste0(kind,'_growth'), model_type=kind, time=t, analytical_state=analytical, euler_state=x, absolute_error=abs(analytical-x), rate_at_euler_state=rate, growth_rate=r, carrying_capacity=capacity, initial_state=x0, method='analytical_vs_explicit_euler')
    x <- x + dt * rate
  }
  do.call(rbind, rows)
}
results <- rbind(simulate_model('exponential', 10, 0.25), simulate_model('logistic', 10, 0.25, 100))
dir.create('outputs/tables', recursive=TRUE, showWarnings=FALSE)
write.csv(results, 'outputs/tables/r_separable_equation_audit.csv', row.names=FALSE)
print(head(results)); print(tail(results))
