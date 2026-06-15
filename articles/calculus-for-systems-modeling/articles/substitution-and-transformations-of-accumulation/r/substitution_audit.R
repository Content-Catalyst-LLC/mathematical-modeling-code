g <- function(x) {
  x^2 + 1
}

g_prime <- function(x) {
  2 * x
}

f <- function(u) {
  sqrt(u)
}

transformed_integrand_x <- function(x) {
  f(g(x)) * g_prime(x)
}

trapezoid_integral <- function(values, points) {
  total <- 0
  for (i in seq_len(length(points) - 1)) {
    step <- points[i + 1] - points[i]
    if (step <= 0) {
      stop("Grid points must be strictly increasing.")
    }
    total <- total + 0.5 * (values[i] + values[i + 1]) * step
  }
  total
}

a <- 1
b <- 3
n <- 400

x_points <- seq(a, b, length.out = n + 1)
direct_values <- transformed_integrand_x(x_points)
direct_integral <- trapezoid_integral(direct_values, x_points)

u_start <- g(a)
u_end <- g(b)
u_points <- seq(u_start, u_end, length.out = n + 1)
u_values <- f(u_points)
transformed_integral <- trapezoid_integral(u_values, u_points)

residual <- direct_integral - transformed_integral
warning <- ""
if (abs(residual) > 1e-3) {
  warning <- "direct and transformed accumulation differ beyond tolerance"
}

result <- data.frame(
  original_start = a,
  original_end = b,
  transformed_start = u_start,
  transformed_end = u_end,
  direct_integral = direct_integral,
  transformed_integral = transformed_integral,
  residual = residual,
  method = "trapezoidal comparison",
  unit_check = "f(u) du equals f(g(x)) g_prime(x) dx",
  warning = warning
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(result, "outputs/tables/r_substitution_audit.csv", row.names = FALSE)
print(result)
