args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <impulse-shock|step-forcing|periodic-forcing|forced-recovery> ...")
cmd <- args[[1]]
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default
write_result <- function(name, df) { write.csv(df, file.path(out_dir, paste0(name, ".csv")), row.names = FALSE); print(df) }
restoring_rate <- function(x, equilibrium, recovery_rate) -recovery_rate * (x - equilibrium)
impulse_shock <- function(time, shock_time, shock_magnitude, tolerance = 1e-12) ifelse(abs(time - shock_time) < tolerance, shock_magnitude, 0)
step_forcing <- function(time, start_time, level) ifelse(time >= start_time, level, 0)
periodic_forcing <- function(time, amplitude, angular_frequency, phase) amplitude * sin(angular_frequency * time + phase)

if (cmd == "impulse-shock") {
  time <- as.numeric(get_arg(2, "10")); shock_time <- as.numeric(get_arg(3, "10")); shock_magnitude <- as.numeric(get_arg(4, "-30"))
  write_result("r_impulse_shock", data.frame(calculator=cmd, time=time, shock_time=shock_time, shock_magnitude=shock_magnitude, shock_value=impulse_shock(time, shock_time, shock_magnitude)))
} else if (cmd == "step-forcing") {
  time <- as.numeric(get_arg(2, "12")); start_time <- as.numeric(get_arg(3, "10")); level <- as.numeric(get_arg(4, "5"))
  write_result("r_step_forcing", data.frame(calculator=cmd, time=time, start_time=start_time, level=level, forcing_value=step_forcing(time, start_time, level)))
} else if (cmd == "periodic-forcing") {
  time <- as.numeric(get_arg(2, "1.57079632679")); amplitude <- as.numeric(get_arg(3, "2")); angular_frequency <- as.numeric(get_arg(4, "1")); phase <- as.numeric(get_arg(5, "0"))
  write_result("r_periodic_forcing", data.frame(calculator=cmd, time=time, amplitude=amplitude, angular_frequency=angular_frequency, phase=phase, forcing_value=periodic_forcing(time, amplitude, angular_frequency, phase)))
} else if (cmd == "forced-recovery") {
  initial_state <- as.numeric(get_arg(2, "100")); equilibrium <- as.numeric(get_arg(3, "100")); recovery_rate <- as.numeric(get_arg(4, "0.15")); shock_time <- as.numeric(get_arg(5, "10")); shock_magnitude <- as.numeric(get_arg(6, "-30")); dt <- as.numeric(get_arg(7, "0.1")); steps <- as.integer(get_arg(8, "300"))
  baseline <- initial_state; forced <- initial_state; rows <- list()
  for (step in 0:steps) {
    time <- step * dt
    shock_value <- impulse_shock(time, shock_time, shock_magnitude)
    rows[[length(rows)+1]] <- data.frame(step=step, time=time, baseline_state=baseline, forced_state=forced, shock_value=shock_value, absolute_deviation=abs(forced-baseline))
    baseline <- baseline + dt * restoring_rate(baseline, equilibrium, recovery_rate)
    if (shock_value != 0) forced <- forced + shock_value
    forced <- forced + dt * restoring_rate(forced, equilibrium, recovery_rate)
  }
  write_result("r_forced_recovery", do.call(rbind, rows))
} else {
  stop(paste("Unknown command:", cmd))
}
