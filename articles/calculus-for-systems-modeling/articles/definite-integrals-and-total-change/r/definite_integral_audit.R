net_rate <- function(t) {
  4 * sin(t / 2) + 1
}

trapezoid_integral <- function(values, times) {
  total <- 0
  for (i in seq_len(length(times) - 1)) {
    dt <- times[i + 1] - times[i]
    if (dt <= 0) {
      stop("Times must be strictly increasing.")
    }
    total <- total + 0.5 * (values[i] + values[i + 1]) * dt
  }
  total
}

times <- seq(0, 4, by = 0.5)
rates <- net_rate(times)

signed_accumulation <- trapezoid_integral(rates, times)
absolute_accumulation <- trapezoid_integral(abs(rates), times)

warning <- ""
if (any(rates < 0) && abs(signed_accumulation) < absolute_accumulation) {
  warning <- "signed accumulation includes cancellation"
}

result <- data.frame(
  interval_start = min(times),
  interval_end = max(times),
  method = "trapezoidal approximation",
  signed_accumulation = signed_accumulation,
  absolute_accumulation = absolute_accumulation,
  unit_check = "rate units times time units = accumulated quantity units",
  interpretation = "signed accumulation estimates net change; absolute accumulation estimates total activity",
  warning = warning
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(result, "outputs/tables/r_definite_integral_audit.csv", row.names = FALSE)
print(result)
