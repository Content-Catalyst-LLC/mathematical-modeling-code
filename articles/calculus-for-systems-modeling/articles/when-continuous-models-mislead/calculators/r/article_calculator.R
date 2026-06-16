args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <smoothness-risk|aggregation-risk> ...")
cmd <- args[[1]]
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default
write_result <- function(name, df) { write.csv(df, file.path(out_dir, paste0(name, ".csv")), row.names = FALSE); print(df) }
risk_label <- function(score) ifelse(score >= 3, "high", ifelse(score >= 1, "moderate", "low"))

if (cmd == "smoothness-risk") {
  breaks <- as.integer(get_arg(2, "1"))
  thresholds <- as.integer(get_arg(3, "1"))
  heterogeneity <- as.integer(get_arg(4, "1"))
  solver_warnings <- as.integer(get_arg(5, "0"))
  score <- sum(c(breaks, thresholds, heterogeneity, solver_warnings))
  write_result("r_smoothness_risk", data.frame(calculator=cmd, risk_score=score, risk=risk_label(score), warning="Smooth mathematical output does not prove smooth system behavior."))
} else if (cmd == "aggregation-risk") {
  mean_value <- as.numeric(get_arg(2, "50"))
  maximum <- as.numeric(get_arg(3, "95"))
  threshold <- as.numeric(get_arg(4, "80"))
  exceeds <- maximum >= threshold && mean_value < threshold
  write_result("r_aggregation_risk", data.frame(calculator=cmd, max_mean_gap=maximum-mean_value, hidden_threshold_exceedance=exceeds, warning="An average can hide local stress, inequality, or bottlenecks."))
} else {
  stop(paste("Unknown command:", cmd))
}
