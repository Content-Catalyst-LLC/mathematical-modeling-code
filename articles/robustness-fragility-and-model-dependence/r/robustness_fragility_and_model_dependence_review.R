# Base R workflow for robustness summary and fragility ranking.

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

matrix_path <- file.path(tables_dir, "robustness_matrix.csv")
register_path <- file.path(tables_dir, "robustness_register.csv")

if (!file.exists(matrix_path) || !file.exists(register_path)) {
  stop("Missing robustness outputs. Run make python first.")
}

matrix_data <- read.csv(matrix_path, stringsAsFactors = FALSE)
register <- read.csv(register_path, stringsAsFactors = FALSE)

matrix_data$projected_stock <- as.numeric(matrix_data$projected_stock)
matrix_data$distance_to_threshold <- as.numeric(matrix_data$distance_to_threshold)
matrix_data$absolute_threshold_distance <- abs(matrix_data$distance_to_threshold)

matrix_data <- matrix_data[order(matrix_data$absolute_threshold_distance), ]

summary_table <- data.frame(
  mean_output = mean(matrix_data$projected_stock),
  min_output = min(matrix_data$projected_stock),
  max_output = max(matrix_data$projected_stock),
  robustness_spread = max(matrix_data$projected_stock) - min(matrix_data$projected_stock),
  threshold_disagreement = length(unique(matrix_data$below_threshold)) > 1,
  fragile_case_count = sum(matrix_data$fragility_class == "fragile"),
  scenario_count = nrow(matrix_data)
)

register$priority <- ifelse(
  register$robustness_risk_score >= 8,
  "high",
  ifelse(register$robustness_risk_score >= 6, "medium", "low")
)

write.csv(
  matrix_data,
  file.path(tables_dir, "r_fragility_ranking.csv"),
  row.names = FALSE
)

write.csv(
  summary_table,
  file.path(tables_dir, "r_robustness_summary.csv"),
  row.names = FALSE
)

write.csv(
  register,
  file.path(tables_dir, "r_robustness_review_queue.csv"),
  row.names = FALSE
)

png(file.path(figures_dir, "r_robustness_matrix_plot.png"), width = 1100, height = 750)

barplot(
  matrix_data$projected_stock,
  names.arg = matrix_data$key,
  las = 2,
  ylab = "Projected stock",
  main = "Robustness Matrix: Output by Model and Scenario"
)
abline(h = 45, lty = 2)

dev.off()

print(summary_table)
print(matrix_data)
print(register)
