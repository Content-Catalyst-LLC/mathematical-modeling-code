# Base R workflow for calibration and residual diagnostics.

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

residual_path <- file.path(tables_dir, "fitted_model_residuals.csv")
score_path <- file.path(tables_dir, "parameter_candidate_scores.csv")
register_path <- file.path(tables_dir, "calibration_register.csv")

if (!file.exists(residual_path) || !file.exists(score_path) || !file.exists(register_path)) {
  stop("Missing calibration outputs. Run make python first.")
}

residuals_data <- read.csv(residual_path, stringsAsFactors = FALSE)
scores <- read.csv(score_path, stringsAsFactors = FALSE)
register <- read.csv(register_path, stringsAsFactors = FALSE)

residuals_data$residual <- as.numeric(residuals_data$residual)
scores$sse <- as.numeric(scores$sse)
scores$rmse <- as.numeric(scores$rmse)

best_fit <- scores[which.min(scores$sse), ]

register$priority <- ifelse(
  register$calibration_risk_score >= 8,
  "high",
  ifelse(register$calibration_risk_score >= 6, "medium", "low")
)

residual_summary <- data.frame(
  residual_mean = mean(residuals_data$residual),
  residual_sd = sd(residuals_data$residual),
  residual_min = min(residuals_data$residual),
  residual_max = max(residuals_data$residual),
  rmse = best_fit$rmse[1],
  growth_rate = best_fit$growth_rate[1],
  carrying_capacity = best_fit$carrying_capacity[1]
)

write.csv(
  residual_summary,
  file.path(tables_dir, "r_calibration_residual_summary.csv"),
  row.names = FALSE
)

write.csv(
  register,
  file.path(tables_dir, "r_calibration_review_queue.csv"),
  row.names = FALSE
)

png(file.path(figures_dir, "r_calibration_residuals.png"), width = 1000, height = 700)

plot(
  residuals_data$time,
  residuals_data$residual,
  type = "b",
  xlab = "Time",
  ylab = "Residual",
  main = "Calibration Residual Diagnostics"
)
abline(h = 0, lty = 2)
grid()

dev.off()

print(residual_summary)
print(register)
