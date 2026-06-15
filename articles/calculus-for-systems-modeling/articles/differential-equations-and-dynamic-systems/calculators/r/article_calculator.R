args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <exponential-rate|logistic-rate|euler-step> ...")
cmd <- args[[1]]
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default
write_result <- function(name, df) { write.csv(df, file.path(out_dir, paste0(name, ".csv")), row.names = FALSE); print(df) }

if (cmd == "exponential-rate") {
  state <- as.numeric(get_arg(2, "10")); r <- as.numeric(get_arg(3, "0.35"))
  write_result("r_exponential_rate", data.frame(calculator=cmd, state=state, growth_rate=r, rate=r*state))
} else if (cmd == "logistic-rate") {
  state <- as.numeric(get_arg(2, "10")); r <- as.numeric(get_arg(3, "0.35")); capacity <- as.numeric(get_arg(4, "100"))
  rate <- r*state*(1-state/capacity)
  write_result("r_logistic_rate", data.frame(calculator=cmd, state=state, growth_rate=r, capacity=capacity, rate=rate))
} else if (cmd == "euler-step") {
  state <- as.numeric(get_arg(2, "10")); rate <- as.numeric(get_arg(3, "3.5")); dt <- as.numeric(get_arg(4, "0.1"))
  write_result("r_euler_step", data.frame(calculator=cmd, state=state, rate=rate, dt=dt, next_state=state + dt*rate))
} else {
  stop(paste("Unknown command:", cmd))
}
