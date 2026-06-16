args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <logistic-final|scope-check> ...")
cmd <- args[[1]]
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default
write_result <- function(name, df) { write.csv(df, file.path(out_dir, paste0(name, ".csv")), row.names = FALSE); print(df) }

logistic_solution <- function(t, x0, growth_rate, carrying_capacity) {
  carrying_capacity / (1 + ((carrying_capacity - x0) / x0) * exp(-growth_rate * t))
}

if (cmd == "logistic-final") {
  x0 <- as.numeric(get_arg(2, "10"))
  r <- as.numeric(get_arg(3, "0.35"))
  k <- as.numeric(get_arg(4, "100"))
  horizon <- as.numeric(get_arg(5, "20"))
  final <- logistic_solution(horizon, x0, r, k)
  write_result("r_logistic_final", data.frame(calculator=cmd, initial_stock=x0, final_stock=final, warning="Synthetic teaching example; do not treat as empirical forecast."))
} else if (cmd == "scope-check") {
  value <- as.numeric(get_arg(2, "0.35"))
  lower <- as.numeric(get_arg(3, "0.1"))
  upper <- as.numeric(get_arg(4, "0.6"))
  in_scope <- value >= lower && value <= upper
  write_result("r_scope_check", data.frame(calculator=cmd, value=value, lower=lower, upper=upper, in_scope=in_scope, warning="Using values outside tested ranges requires review."))
} else {
  stop(paste("Unknown command:", cmd))
}
