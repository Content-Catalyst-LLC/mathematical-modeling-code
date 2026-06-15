net_flow <- function(t) {
  inflow <- 12 + 0.5 * t
  outflow <- 7 + 0.2 * t
  inflow - outflow
}

recover_stock <- function(times, initial_stock) {
  if (length(times) < 2) {
    stop("At least two time points are required.")
  }

  stock <- initial_stock
  records <- data.frame(
    time = times[1],
    net_flow = net_flow(times[1]),
    recovered_stock = stock,
    method = "initial condition",
    unit_check = "stock units = initial stock units",
    warning = "baseline determines recovered level"
  )

  for (i in 2:length(times)) {
    previous <- times[i - 1]
    current <- times[i]
    dt <- current - previous

    if (dt <= 0) {
      stop("Times must be strictly increasing.")
    }

    area <- 0.5 * (net_flow(previous) + net_flow(current)) * dt
    stock <- stock + area

    warning <- ""
    if (dt > 2) {
      warning <- "large time step; accumulation may be coarse"
    }

    records <- rbind(
      records,
      data.frame(
        time = current,
        net_flow = net_flow(current),
        recovered_stock = stock,
        method = "trapezoidal accumulation",
        unit_check = "flow units times time units = stock units",
        warning = warning
      )
    )
  }

  records
}

results <- recover_stock(0:6, initial_stock = 100)
dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(results, "outputs/tables/r_antiderivative_recovery_audit.csv", row.names = FALSE)
print(results)
