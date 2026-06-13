# Base R workflow for uncertainty propagation review.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)

if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}

tables_dir <- file.path(article_root, "outputs", "tables")
figures_dir <- file.path(article_root, "outputs", "figures")
dir.create(tables_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(figures_dir, recursive = TRUE, showWarnings = FALSE)

runs_path <- file.path(tables_dir, "uncertainty_propagation_runs.csv")
register_path <- file.path(tables_dir, "uncertainty_register.csv")

if (!file.exists(runs_path) || !file.exists(register_path)) {
  stop("Missing uncertainty outputs. Run make python first.")
}

runs <- read.csv(runs_path, stringsAsFactors = FALSE)
register <- read.csv(register_path, stringsAsFactors = FALSE)

runs$projected_stock <- as.numeric(runs$projected_stock)

threshold_probability <- mean(runs$below_threshold == "True" | runs$below_threshold == TRUE)

summary_table <- data.frame(
  mean = mean(runs$projected_stock),
  median = median(runs$projected_stock),
  p05 = as.numeric(quantile(runs$projected_stock, 0.05)),
  p25 = as.numeric(quantile(runs$projected_stock, 0.25)),
  p75 = as.numeric(quantile(runs$projected_stock, 0.75)),
  p95 = as.numeric(quantile(runs$projected_stock, 0.95)),
  min = min(runs$projected_stock),
  max = max(runs$projected_stock),
  threshold_probability = threshold_probability,
  n = nrow(runs)
)

register$priority <- ifelse(
  register$uncertainty_risk_score >= 8,
  "high",
  ifelse(register$uncertainty_risk_score >= 6, "medium", "low")
)

write.csv(
  summary_table,
  file.path(tables_dir, "r_uncertainty_interval_review.csv"),
  row.names = FALSE
)

write.csv(
  register,
  file.path(tables_dir, "r_uncertainty_review_queue.csv"),
  row.names = FALSE
)

png(file.path(figures_dir, "r_uncertainty_output_distribution.png"), width = 1000, height = 700)

hist(
  runs$projected_stock,
  breaks = 30,
  xlab = "Projected stock",
  main = "Uncertainty Propagation Output Distribution"
)
abline(v = 45, lty = 2)

dev.off()

print(summary_table)
print(register)
