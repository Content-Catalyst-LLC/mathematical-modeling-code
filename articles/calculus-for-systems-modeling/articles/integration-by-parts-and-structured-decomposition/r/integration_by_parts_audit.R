u <- function(x) {
  1 + x
}

u_prime <- function(x) {
  1
}

v <- function(x) {
  exp(-0.3 * x) * sin(x)
}

v_prime <- function(x) {
  exp(-0.3 * x) * (cos(x) - 0.3 * sin(x))
}

trapezoid_integral <- function(values, points) {
  total <- 0
  for (i in seq_len(length(points) - 1)) {
    dx <- points[i + 1] - points[i]
    if (dx <= 0) {
      stop("Grid points must be strictly increasing.")
    }
    total <- total + 0.5 * (values[i] + values[i + 1]) * dx
  }
  total
}

a <- 0
b <- 4
n <- 800
points <- seq(a, b, length.out = n + 1)

direct_values <- u(points) * v_prime(points)
residual_values <- v(points) * u_prime(points)

direct_integral <- trapezoid_integral(direct_values, points)
residual_integral <- trapezoid_integral(residual_values, points)
boundary_term <- u(b) * v(b) - u(a) * v(a)
decomposed_value <- boundary_term - residual_integral
decomposition_residual <- direct_integral - decomposed_value

warning <- ""
if (abs(decomposition_residual) > 1e-3) {
  warning <- "decomposition residual exceeds tolerance"
}

result <- data.frame(
  interval_start = a,
  interval_end = b,
  direct_integral = direct_integral,
  boundary_term = boundary_term,
  residual_integral = residual_integral,
  decomposed_value = decomposed_value,
  decomposition_residual = decomposition_residual,
  method = "trapezoidal comparison",
  unit_check = "u times v units are shared by direct, boundary, and residual terms",
  warning = warning
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(result, "outputs/tables/r_integration_by_parts_audit.csv", row.names = FALSE)
print(result)
