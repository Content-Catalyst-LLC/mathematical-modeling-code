args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <euler-step|stability-check|logistic-step> ...")
cmd <- args[[1]]
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default
write_result <- function(name, df) { write.csv(df, file.path(out_dir, paste0(name, ".csv")), row.names = FALSE); print(df) }

if (cmd == "euler-step") {
  t <- as.numeric(get_arg(2, "0"))
  y <- as.numeric(get_arg(3, "100"))
  h <- as.numeric(get_arg(4, "0.1"))
  decay_rate <- as.numeric(get_arg(5, "0.35"))
  updated <- y + h * (-decay_rate * y)
  write_result("r_euler_step", data.frame(calculator=cmd, t=t, y=y, h=h, decay_rate=decay_rate, updated_value=updated))
} else if (cmd == "stability-check") {
  h <- as.numeric(get_arg(2, "0.1"))
  decay_rate <- as.numeric(get_arg(3, "0.35"))
  multiplier <- 1 - h * decay_rate
  status <- ifelse(abs(multiplier) <= 1, "stable_for_simple_decay", "unstable_risk")
  write_result("r_stability_check", data.frame(calculator=cmd, h=h, decay_rate=decay_rate, stability_multiplier=multiplier, stability_status=status))
} else if (cmd == "logistic-step") {
  y <- as.numeric(get_arg(2, "10"))
  r <- as.numeric(get_arg(3, "0.2"))
  k <- as.numeric(get_arg(4, "100"))
  h <- as.numeric(get_arg(5, "1"))
  updated <- y + h * r * y * (1 - y / k)
  write_result("r_logistic_step", data.frame(calculator=cmd, y=y, r=r, k=k, h=h, updated_value=updated))
} else {
  stop(paste("Unknown command:", cmd))
}
