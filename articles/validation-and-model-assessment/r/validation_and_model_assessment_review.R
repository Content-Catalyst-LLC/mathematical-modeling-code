# Base R workflow for validation and model assessment diagnostics.

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

error_path <- file.path(tables_dir, "validation_error_diagnostics.csv")
summary_path <- file.path(tables_dir, "validation_scenario_summary.csv")
register_path <- file.path(tables_dir, "validation_register.csv")

if (!file.exists(error_path) || !file.exists(summary_path) || !file.exists(register_path)) {
  stop("Missing validation outputs. Run make python first.")
}

errors <- read.csv(error_path, stringsAsFactors = FALSE)
scenario_summary <- read.csv(summary_path, stringsAsFactors = FALSE)
register <- read.csv(register_path, stringsAsFactors = FALSE)

errors$residual <- as.numeric(errors$residual)
errors$absolute_error <- as.numeric(errors$absolute_error)
scenario_summary$rmse <- as.numeric(scenario_summary$rmse)

register$priority <- ifelse(
  register$validation_risk_score >= 8,
  "high",
  ifelse(register$validation_risk_score >= 6, "medium", "low")
)

overall_review <- data.frame(
  rmse = sqrt(mean(errors$residual ^ 2)),
  mae = mean(errors$absolute_error),
  bias = mean(errors$residual),
  max_abs_error = max(errors$absolute_error),
  n = nrow(errors)
)

overall_review$fitness_for_purpose <- ifelse(
  overall_review$rmse <= 1.25 & overall_review$max_abs_error <= 2.0,
  "adequate for scenario screening",
  ifelse(overall_review$rmse <= 2.5, "limited use requires review", "not adequate without revision")
)

write.csv(
  overall_review,
  file.path(tables_dir, "r_validation_overall_review.csv"),
  row.names = FALSE
)

write.csv(
  register,
  file.path(tables_dir, "r_validation_review_queue.csv"),
  row.names = FALSE
)

png(file.path(figures_dir, "r_validation_residuals.png"), width = 1000, height = 700)

plot(
  errors$time,
  errors$residual,
  type = "b",
  xlab = "Time",
  ylab = "Residual",
  main = "Validation Residual Diagnostics"
)
abline(h = 0, lty = 2)
grid()

dev.off()

print(overall_review)
print(scenario_summary)
print(register)
