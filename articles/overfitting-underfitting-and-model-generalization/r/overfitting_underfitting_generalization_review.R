# Base R workflow for generalization diagnostics.

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

diagnostics_path <- file.path(tables_dir, "generalization_model_diagnostics.csv")
register_path <- file.path(tables_dir, "generalization_register.csv")

if (!file.exists(diagnostics_path) || !file.exists(register_path)) {
  stop("Missing generalization outputs. Run make python first.")
}

diagnostics <- read.csv(diagnostics_path, stringsAsFactors = FALSE)
register <- read.csv(register_path, stringsAsFactors = FALSE)

diagnostics$training_rmse <- as.numeric(diagnostics$training_rmse)
diagnostics$validation_rmse <- as.numeric(diagnostics$validation_rmse)
diagnostics$overfit_gap <- as.numeric(diagnostics$overfit_gap)
diagnostics$generalization_score <- as.numeric(diagnostics$generalization_score)

diagnostics$review_priority <- ifelse(
  diagnostics$classification %in% c("likely_overfit", "likely_underfit"),
  "high",
  ifelse(diagnostics$classification == "requires_review", "medium", "low")
)

register$priority <- ifelse(
  register$generalization_risk_score >= 8,
  "high",
  ifelse(register$generalization_risk_score >= 6, "medium", "low")
)

selected_model <- diagnostics[which.min(diagnostics$generalization_score), ]

write.csv(
  diagnostics,
  file.path(tables_dir, "r_generalization_diagnostics_review.csv"),
  row.names = FALSE
)

write.csv(
  register,
  file.path(tables_dir, "r_generalization_review_queue.csv"),
  row.names = FALSE
)

write.csv(
  selected_model,
  file.path(tables_dir, "r_generalization_selected_model.csv"),
  row.names = FALSE
)

png(file.path(figures_dir, "r_training_vs_validation_error.png"), width = 1100, height = 750)

mat <- rbind(diagnostics$training_rmse, diagnostics$validation_rmse)
colnames(mat) <- diagnostics$model_id

barplot(
  mat,
  beside = TRUE,
  las = 2,
  ylab = "RMSE",
  main = "Training vs Validation Error"
)
legend("topright", legend = c("Training RMSE", "Validation RMSE"), fill = gray.colors(2))

dev.off()

print(selected_model)
print(diagnostics)
print(register)
