args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <logistic-next|trajectory-divergence|forecast-horizon> ...")
cmd <- args[[1]]
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default
write_result <- function(name, df) { write.csv(df, file.path(out_dir, paste0(name, ".csv")), row.names = FALSE); print(df) }
logistic_map <- function(x, r) r * x * (1 - x)

if (cmd == "logistic-next") {
  x <- as.numeric(get_arg(2, "0.2")); r <- as.numeric(get_arg(3, "3.9"))
  write_result("r_logistic_next", data.frame(calculator=cmd, x=x, r=r, next_state=logistic_map(x, r)))
} else if (cmd == "trajectory-divergence") {
  x0 <- as.numeric(get_arg(2, "0.2")); perturbation <- as.numeric(get_arg(3, "1e-8")); r <- as.numeric(get_arg(4, "3.9")); steps <- as.integer(get_arg(5, "30"))
  x_ref <- x0; x_per <- x0 + perturbation; rows <- list()
  for (step in 0:steps) {
    rows[[length(rows)+1]] <- data.frame(step=step, x_reference=x_ref, x_perturbed=x_per, absolute_difference=abs(x_ref-x_per))
    x_ref <- logistic_map(x_ref, r); x_per <- logistic_map(x_per, r)
  }
  write_result("r_trajectory_divergence", do.call(rbind, rows))
} else if (cmd == "forecast-horizon") {
  initial_uncertainty <- as.numeric(get_arg(2, "1e-8")); acceptable_error <- as.numeric(get_arg(3, "1e-2")); lyapunov <- as.numeric(get_arg(4, "0.5"))
  horizon <- ifelse(initial_uncertainty > 0 && acceptable_error > 0 && lyapunov > 0, log(acceptable_error/initial_uncertainty)/lyapunov, NA)
  write_result("r_forecast_horizon", data.frame(calculator=cmd, initial_uncertainty=initial_uncertainty, acceptable_error=acceptable_error, lyapunov=lyapunov, forecast_horizon=horizon))
} else {
  stop(paste("Unknown command:", cmd))
}
