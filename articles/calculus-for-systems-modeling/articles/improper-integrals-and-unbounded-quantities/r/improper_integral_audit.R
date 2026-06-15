tail_function <- function(x) {
  exp(-0.4 * x)
}

exact_reference <- function() {
  1 / 0.4
}

trapezoid_integral <- function(func, a, b, n = 4000) {
  if (b <= a) {
    stop("Upper bound must exceed lower bound.")
  }

  points <- seq(a, b, length.out = n + 1)
  values <- func(points)
  dx <- diff(points)

  sum(0.5 * (values[-length(values)] + values[-1]) * dx)
}

cutoffs <- c(2, 4, 8, 12, 20)
reference <- exact_reference()

rows <- lapply(cutoffs, function(cutoff) {
  truncated <- trapezoid_integral(tail_function, 0, cutoff)
  tail_error <- reference - truncated

  warning <- ""
  if (abs(tail_error) > 0.05) {
    warning <- "tail contribution remains material at this cutoff"
  }

  data.frame(
    cutoff = cutoff,
    truncated_value = truncated,
    reference_value = reference,
    tail_error = tail_error,
    method = "trapezoidal truncation audit",
    convergence_interpretation = "exponential decay produces finite infinite-horizon accumulation",
    warning = warning
  )
})

result <- do.call(rbind, rows)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(result, "outputs/tables/r_improper_integral_audit.csv", row.names = FALSE)

print(result)
