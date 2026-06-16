args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <rk4-solver-step|tolerance-threshold|stiffness-indicator> ...")
cmd <- args[[1]]
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default
write_result <- function(name, df) { write.csv(df, file.path(out_dir, paste0(name, ".csv")), row.names = FALSE); print(df) }

rate <- function(t, y, decay_rate) -decay_rate * y
rk4_step <- function(t, y, h, decay_rate) {
  k1 <- rate(t, y, decay_rate)
  k2 <- rate(t + h / 2, y + h * k1 / 2, decay_rate)
  k3 <- rate(t + h / 2, y + h * k2 / 2, decay_rate)
  k4 <- rate(t + h, y + h * k3, decay_rate)
  y + (h / 6) * (k1 + 2*k2 + 2*k3 + k4)
}

if (cmd == "rk4-solver-step") {
  t <- as.numeric(get_arg(2, "0"))
  y <- as.numeric(get_arg(3, "100"))
  h <- as.numeric(get_arg(4, "0.5"))
  decay_rate <- as.numeric(get_arg(5, "0.35"))
  write_result("r_rk4_solver_step", data.frame(calculator=cmd, t=t, y=y, h=h, decay_rate=decay_rate, updated_value=rk4_step(t,y,h,decay_rate)))
} else if (cmd == "tolerance-threshold") {
  atol <- as.numeric(get_arg(2, "1e-8"))
  rtol <- as.numeric(get_arg(3, "1e-6"))
  state <- as.numeric(get_arg(4, "100"))
  write_result("r_tolerance_threshold", data.frame(calculator=cmd, atol=atol, rtol=rtol, state=state, tolerance_threshold=atol + rtol * abs(state)))
} else if (cmd == "stiffness-indicator") {
  fast_rate <- as.numeric(get_arg(2, "100"))
  slow_rate <- as.numeric(get_arg(3, "1"))
  ratio <- abs(fast_rate / slow_rate)
  status <- ifelse(ratio >= 100, "possible_stiffness_review_needed", "mild_or_moderate_scale_separation")
  write_result("r_stiffness_indicator", data.frame(calculator=cmd, fast_rate=fast_rate, slow_rate=slow_rate, rate_scale_ratio=ratio, review_status=status))
} else {
  stop(paste("Unknown command:", cmd))
}
