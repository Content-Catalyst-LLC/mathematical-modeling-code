args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <exponential|logistic> ...")
cmd <- args[[1]]
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default
write_result <- function(name, df) { write.csv(df, file.path(out_dir, paste0(name, ".csv")), row.names = FALSE); print(df) }

if (cmd == "exponential") {
  n0 <- as.numeric(get_arg(2, "100"))
  r <- as.numeric(get_arg(3, "0.08"))
  t <- as.numeric(get_arg(4, "40"))
  population <- n0 * exp(r * t)
  write_result("r_exponential", data.frame(calculator=cmd, n0=n0, r=r, t=t, population=population, warning="Exponential growth is a baseline model."))
} else if (cmd == "logistic") {
  n0 <- as.numeric(get_arg(2, "100"))
  r <- as.numeric(get_arg(3, "0.08"))
  k <- as.numeric(get_arg(4, "1000"))
  t <- as.numeric(get_arg(5, "40"))
  population <- k / (1 + ((k - n0) / n0) * exp(-r * t))
  write_result("r_logistic", data.frame(calculator=cmd, n0=n0, r=r, k=k, t=t, population=population, capacity_fraction=population/k, warning="Carrying capacity is assumption-bearing."))
} else {
  stop(paste("Unknown command:", cmd))
}
