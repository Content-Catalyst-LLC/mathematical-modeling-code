objective <- function(x, y) x^2 + 2 * y^2
constraint <- function(x, y) x + y
grad_objective <- function(x, y) c(2 * x, 4 * y)
grad_constraint <- function(x, y) c(1, 1)

solve_budget_constraint <- function(target) {
  y <- target / 3
  x <- 2 * target / 3
  lambda_value <- 2 * x
  c(x = x, y = y, lambda_value = lambda_value)
}

audit_solution <- function(target) {
  solution <- solve_budget_constraint(target)
  x <- solution[["x"]]
  y <- solution[["y"]]
  lambda_value <- solution[["lambda_value"]]
  gf <- grad_objective(x, y)
  gg <- grad_constraint(x, y)
  stationarity <- gf - lambda_value * gg
  stationarity_residual_norm <- sqrt(sum(stationarity^2))
  constraint_value <- constraint(x, y)
  constraint_residual <- constraint_value - target
  feasible <- abs(constraint_residual) <= 1e-9
  warning <- ifelse(
    !feasible,
    "Candidate solution violates the constraint.",
    ifelse(stationarity_residual_norm > 1e-8, "Stationarity residual is large.", "Multiplier interpretation is local and unit-dependent.")
  )

  data.frame(
    x = x, y = y,
    objective_value = objective(x, y),
    constraint_value = constraint_value,
    constraint_target = target,
    constraint_residual = constraint_residual,
    lambda_value = lambda_value,
    gradient_f_x = gf[1],
    gradient_f_y = gf[2],
    gradient_g_x = gg[1],
    gradient_g_y = gg[2],
    stationarity_residual_norm = stationarity_residual_norm,
    feasible = feasible,
    warning = warning
  )
}

results <- rbind(audit_solution(12), audit_solution(18), audit_solution(24))
dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(results, "outputs/tables/r_constrained_optimization_audit.csv", row.names = FALSE)
print(results)
