state <- function(t) {
  50 + 2 * t + 3 * sin(t)
}

rate <- function(t) {
  2 + 3 * cos(t)
}

trapezoid_integral <- function(times) {
  total <- 0
  for (i in seq_len(length(times) - 1)) {
    previous <- times[i]
    current <- times[i + 1]
    dt <- current - previous

    if (dt <= 0) {
      stop("Times must be strictly increasing.")
    }

    total <- total + 0.5 * (rate(previous) + rate(current)) * dt
  }
  total
}

times <- seq(0, 2, by = 0.25)

state_start <- state(min(times))
state_end <- state(max(times))
endpoint_difference <- state_end - state_start
accumulated_rate <- trapezoid_integral(times)
residual <- endpoint_difference - accumulated_rate

warning <- ""
if (abs(residual) > 1e-2) {
  warning <- "endpoint difference and accumulated rate do not closely match"
}

result <- data.frame(
  interval_start = min(times),
  interval_end = max(times),
  state_start = state_start,
  state_end = state_end,
  endpoint_difference = endpoint_difference,
  accumulated_rate = accumulated_rate,
  residual = residual,
  method = "trapezoidal approximation",
  unit_check = "rate units times time units = state units",
  warning = warning
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(result, "outputs/tables/r_fundamental_theorem_audit.csv", row.names = FALSE)
print(result)
