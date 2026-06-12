# Base R workflow for model comparison and selection diagnostics.

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

comparison_path <- file.path(tables_dir, "model_comparison_table.csv")
register_path <- file.path(tables_dir, "model_selection_register.csv")

if (!file.exists(comparison_path) || !file.exists(register_path)) {
  stop("Missing model comparison outputs. Run make python first.")
}

comparison <- read.csv(comparison_path, stringsAsFactors = FALSE)
register <- read.csv(register_path, stringsAsFactors = FALSE)

comparison$calibration_rmse <- as.numeric(comparison$calibration_rmse)
comparison$validation_rmse <- as.numeric(comparison$validation_rmse)
comparison$overfit_gap <- as.numeric(comparison$overfit_gap)
comparison$comparison_score <- as.numeric(comparison$comparison_score)

comparison$overfit_risk <- ifelse(
  comparison$overfit_gap > 1.0,
  "high overfit risk",
  ifelse(comparison$overfit_gap > 0.5, "moderate overfit risk", "lower overfit risk")
)

register$priority <- ifelse(
  register$selection_risk_score >= 8,
  "high",
  ifelse(register$selection_risk_score >= 6, "medium", "low")
)

selected_model <- comparison[which.min(comparison$comparison_score), ]

write.csv(
  comparison,
  file.path(tables_dir, "r_model_comparison_review.csv"),
  row.names = FALSE
)

write.csv(
  register,
  file.path(tables_dir, "r_model_selection_review_queue.csv"),
  row.names = FALSE
)

write.csv(
  selected_model,
  file.path(tables_dir, "r_selected_model_summary.csv"),
  row.names = FALSE
)

png(file.path(figures_dir, "r_model_comparison_error_plot.png"), width = 1100, height = 750)

mat <- rbind(comparison$calibration_rmse, comparison$validation_rmse)
colnames(mat) <- comparison$model_id

barplot(
  mat,
  beside = TRUE,
  las = 2,
  ylab = "RMSE",
  main = "Calibration vs Validation Error"
)
legend("topright", legend = c("Calibration RMSE", "Validation RMSE"), fill = gray.colors(2))

dev.off()

print(selected_model)
print(comparison)
print(register)
