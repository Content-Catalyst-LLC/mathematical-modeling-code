args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <residual|candidate-loss> ...")
cmd <- args[[1]]
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default
write_result <- function(name, df) { write.csv(df, file.path(out_dir, paste0(name, ".csv")), row.names = FALSE); print(df) }

logistic <- function(t, x0, r, k) {
  k / (1 + ((k - x0) / x0) * exp(-r * t))
}

data <- data.frame(
  time = c(0, 2, 4, 6, 8, 10, 12),
  observed = c(10.0, 17.5, 29.2, 44.1, 60.5, 74.0, 83.2)
)

if (cmd == "residual") {
  observed <- as.numeric(get_arg(2, "17.5"))
  predicted <- as.numeric(get_arg(3, "17.2"))
  residual <- observed - predicted
  write_result("r_residual", data.frame(calculator=cmd, observed=observed, predicted=predicted, residual=residual, squared_residual=residual^2, warning="Residuals should be inspected as a pattern not only summarized."))
} else if (cmd == "candidate-loss") {
  r <- as.numeric(get_arg(2, "0.34"))
  k <- as.numeric(get_arg(3, "105"))
  predicted <- logistic(data$time, 10, r, k)
  residual <- data$observed - predicted
  write_result("r_candidate_loss", data.frame(calculator=cmd, growth_rate=r, carrying_capacity=k, loss=sum(residual^2), mean_absolute_residual=mean(abs(residual)), max_absolute_residual=max(abs(residual)), warning="Candidate loss does not prove model validity."))
} else {
  stop(paste("Unknown command:", cmd))
}
