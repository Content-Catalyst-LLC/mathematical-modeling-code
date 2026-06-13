# Base R workflow for residual diagnostics and model error review.

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

residual_path <- file.path(tables_dir, "residual_diagnostics.csv")
register_path <- file.path(tables_dir, "diagnostic_register.csv")

if (!file.exists(residual_path) || !file.exists(register_path)) {
  stop("Missing diagnostic outputs. Run make python first.")
}

residuals <- read.csv(residual_path, stringsAsFactors = FALSE)
register <- read.csv(register_path, stringsAsFactors = FALSE)

residuals$residual <- as.numeric(residuals$residual)
residuals$absolute_error <- as.numeric(residuals$absolute_error)
residuals$time <- as.integer(residuals$time)

overall_review <- data.frame(
  mean_error = mean(residuals$residual),
  mae = mean(residuals$absolute_error),
  rmse = sqrt(mean(residuals$residual ^ 2)),
  median_absolute_error = median(residuals$absolute_error),
  max_absolute_error = max(residuals$absolute_error),
  n = nrow(residuals)
)

group_review <- aggregate(
  cbind(residual, absolute_error) ~ group,
  data = residuals,
  FUN = mean
)

names(group_review) <- c("group", "mean_residual", "mean_absolute_error")

register$priority <- ifelse(
  register$diagnostic_risk_score >= 8,
  "high",
  ifelse(register$diagnostic_risk_score >= 6, "medium", "low")
)

write.csv(
  overall_review,
  file.path(tables_dir, "r_overall_diagnostic_review.csv"),
  row.names = FALSE
)

write.csv(
  group_review,
  file.path(tables_dir, "r_group_diagnostic_review.csv"),
  row.names = FALSE
)

write.csv(
  register,
  file.path(tables_dir, "r_diagnostic_review_queue.csv"),
  row.names = FALSE
)

png(file.path(figures_dir, "r_residuals_over_time.png"), width = 1000, height = 700)

plot(
  residuals$time,
  residuals$residual,
  type = "b",
  xlab = "Time",
  ylab = "Residual",
  main = "Residuals Over Time"
)
abline(h = 0, lty = 2)
grid()

dev.off()

png(file.path(figures_dir, "r_absolute_error_by_group.png"), width = 1000, height = 700)

barplot(
  group_review$mean_absolute_error,
  names.arg = group_review$group,
  las = 2,
  ylab = "Mean absolute error",
  main = "Mean Absolute Error by Diagnostic Group"
)

dev.off()

print(overall_review)
print(group_review)
print(register)
