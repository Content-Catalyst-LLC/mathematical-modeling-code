args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <logistic-final|local-sensitivity> ...")
cmd <- args[[1]]
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default
write_result <- function(name, df) { write.csv(df, file.path(out_dir, paste0(name, ".csv")), row.names = FALSE); print(df) }

logistic <- function(t, x0, r, k) {
  k / (1 + ((k - x0) / x0) * exp(-r * t))
}
final_output <- function(r, k, x0=10, stop_time=20) {
  logistic(stop_time, x0, r, k)
}

if (cmd == "logistic-final") {
  r <- as.numeric(get_arg(2, "0.35"))
  k <- as.numeric(get_arg(3, "100"))
  write_result("r_logistic_final", data.frame(calculator=cmd, growth_rate=r, carrying_capacity=k, final_value=final_output(r,k), warning="A single parameter set does not show robustness."))
} else if (cmd == "local-sensitivity") {
  parameter <- get_arg(2, "growth_rate")
  baseline_r <- 0.35
  baseline_k <- 100
  h <- ifelse(parameter == "growth_rate", 0.01, 1)
  baseline <- final_output(baseline_r, baseline_k)
  if (parameter == "growth_rate") {
    forward <- final_output(baseline_r + h, baseline_k)
    backward <- final_output(baseline_r - h, baseline_k)
    baseline_value <- baseline_r
  } else {
    forward <- final_output(baseline_r, baseline_k + h)
    backward <- final_output(baseline_r, baseline_k - h)
    baseline_value <- baseline_k
  }
  sensitivity <- (forward - backward) / (2*h)
  elasticity <- sensitivity * baseline_value / baseline
  write_result("r_local_sensitivity", data.frame(calculator=cmd, parameter=parameter, baseline_value=baseline_value, finite_difference_sensitivity=sensitivity, elasticity_estimate=elasticity, warning="Local sensitivity depends on baseline and perturbation size."))
} else {
  stop(paste("Unknown command:", cmd))
}
