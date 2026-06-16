args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <logistic-point|visualization-risk-score> ...")
cmd <- args[[1]]
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default
write_result <- function(name, df) { write.csv(df, file.path(out_dir, paste0(name, ".csv")), row.names = FALSE); print(df) }

logistic <- function(t, x0, r, k) {
  k / (1 + ((k - x0) / x0) * exp(-r * t))
}

if (cmd == "logistic-point") {
  t <- as.numeric(get_arg(2, "10"))
  x0 <- as.numeric(get_arg(3, "10"))
  r <- as.numeric(get_arg(4, "0.35"))
  k <- as.numeric(get_arg(5, "100"))
  write_result("r_logistic_point", data.frame(calculator=cmd, time=t, x0=x0, growth_rate=r, carrying_capacity=k, value=logistic(t,x0,r,k), warning="A plotted point is model-implied not empirical evidence."))
} else if (cmd == "visualization-risk-score") {
  axis_risk <- as.integer(get_arg(2, "2"))
  uncertainty_risk <- as.integer(get_arg(3, "3"))
  smoothing_risk <- as.integer(get_arg(4, "1"))
  metadata_risk <- as.integer(get_arg(5, "2"))
  score <- axis_risk + uncertainty_risk + smoothing_risk + metadata_risk
  level <- ifelse(score >= 8, "high_review_priority", ifelse(score >= 4, "moderate_review_priority", "low_review_priority"))
  write_result("r_visualization_risk_score", data.frame(calculator=cmd, risk_score=score, review_level=level, warning="Risk score is a governance heuristic not a statistical measure."))
} else {
  stop(paste("Unknown command:", cmd))
}
