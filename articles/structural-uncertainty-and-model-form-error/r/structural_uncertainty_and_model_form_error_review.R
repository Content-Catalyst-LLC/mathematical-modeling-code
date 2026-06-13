# Base R workflow for structural sensitivity and model-form review.

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

comparison_path <- file.path(tables_dir, "model_form_comparison.csv")
register_path <- file.path(tables_dir, "structural_uncertainty_register.csv")

if (!file.exists(comparison_path) || !file.exists(register_path)) {
  stop("Missing structural uncertainty outputs. Run make python first.")
}

comparison <- read.csv(comparison_path, stringsAsFactors = FALSE)
register <- read.csv(register_path, stringsAsFactors = FALSE)

comparison$projected_stock <- as.numeric(comparison$projected_stock)
comparison$distance_to_threshold <- as.numeric(comparison$distance_to_threshold)

comparison <- comparison[order(comparison$projected_stock), ]

summary_table <- data.frame(
  mean_output = mean(comparison$projected_stock),
  min_output = min(comparison$projected_stock),
  max_output = max(comparison$projected_stock),
  structural_spread = max(comparison$projected_stock) - min(comparison$projected_stock),
  threshold_disagreement = length(unique(comparison$below_threshold)) > 1,
  model_count = nrow(comparison)
)

register$priority <- ifelse(
  register$structural_risk_score >= 8,
  "high",
  ifelse(register$structural_risk_score >= 6, "medium", "low")
)

write.csv(
  comparison,
  file.path(tables_dir, "r_model_form_comparison_review.csv"),
  row.names = FALSE
)

write.csv(
  summary_table,
  file.path(tables_dir, "r_structural_uncertainty_summary.csv"),
  row.names = FALSE
)

write.csv(
  register,
  file.path(tables_dir, "r_structural_review_queue.csv"),
  row.names = FALSE
)

png(file.path(figures_dir, "r_model_form_comparison.png"), width = 1100, height = 750)

barplot(
  comparison$projected_stock,
  names.arg = comparison$key,
  las = 2,
  ylab = "Projected stock",
  main = "Projected Stock by Model Form"
)
abline(h = 45, lty = 2)

dev.off()

print(summary_table)
print(comparison)
print(register)
