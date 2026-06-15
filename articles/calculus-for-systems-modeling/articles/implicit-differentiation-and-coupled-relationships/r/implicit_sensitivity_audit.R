equilibrium_state <- function(parameter) {
  (-parameter + sqrt(parameter^2 + 40)) / 2
}

constraint <- function(x, p) {
  x^2 + p * x - 10
}

partial_state <- function(x, p) {
  2 * x + p
}

partial_parameter <- function(x, p) {
  x
}

implicit_sensitivity <- function(x, p) {
  gx <- partial_state(x, p)
  if (abs(gx) < 1e-8) {
    stop("regularity failure: partial derivative with respect to state is near zero")
  }
  -partial_parameter(x, p) / gx
}

finite_difference_sensitivity <- function(p, h = 1e-5) {
  (equilibrium_state(p + h) - equilibrium_state(p - h)) / (2 * h)
}

audit_parameter <- function(p) {
  x <- equilibrium_state(p)
  gx <- partial_state(x, p)
  gp <- partial_parameter(x, p)
  sens <- implicit_sensitivity(x, p)
  fd <- finite_difference_sensitivity(p)
  error <- abs(sens - fd)

  warning <- ""
  if (abs(gx) < 1e-4) {
    warning <- "near singular state Jacobian; sensitivity may be unstable"
  } else if (error > 1e-5) {
    warning <- "finite-difference check differs from implicit derivative"
  }

  data.frame(
    parameter = p,
    equilibrium_state = x,
    constraint_value = constraint(x, p),
    partial_state = gx,
    partial_parameter = gp,
    implicit_sensitivity = sens,
    finite_difference_check = fd,
    absolute_error = error,
    warning = warning
  )
}

results <- do.call(rbind, lapply(c(-3, -1, 0, 1, 3), audit_parameter))
dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(results, "outputs/tables/r_implicit_sensitivity_audit.csv", row.names = FALSE)
print(results)
