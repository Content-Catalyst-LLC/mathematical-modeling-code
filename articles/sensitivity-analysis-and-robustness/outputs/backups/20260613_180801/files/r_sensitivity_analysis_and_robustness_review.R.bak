# Base R workflow for sensitivity ranking and robustness review.

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

summary_path <- file.path(tables_dir, "sensitivity_summary.csv")
register_path <- file.path(tables_dir, "sensitivity_register.csv")

if (!file.exists(summary_path) || !file.exists(register_path)) {
  stop("Missing sensitivity outputs. Run make python first.")
}

summary_data <- read.csv(summary_path, stringsAsFactors = FALSE)
register <- read.csv(register_path, stringsAsFactors = FALSE)

summary_data$range_width <- as.numeric(summary_data$range_width)
summary_data$max_abs_relative_change <- as.numeric(summary_data$max_abs_relative_change)

summary_data <- summary_data[order(-summary_data$range_width), ]

summary_data$review_priority <- ifelse(
  summary_data$threshold_crossed == "True" | summary_data$threshold_crossed == TRUE,
  "high",
  ifelse(summary_data$range_width > median(summary_data$range_width), "medium", "low")
)

register$priority <- ifelse(
  register$sensitivity_risk_score >= 8,
  "high",
  ifelse(register$sensitivity_risk_score >= 6, "medium", "low")
)

write.csv(
  summary_data,
  file.path(tables_dir, "r_sensitivity_ranking_review.csv"),
  row.names = FALSE
)

write.csv(
  register,
  file.path(tables_dir, "r_sensitivity_review_queue.csv"),
  row.names = FALSE
)

png(file.path(figures_dir, "r_sensitivity_tornado_plot.png"), width = 1100, height = 750)

barplot(
  rev(summary_data$range_width),
  names.arg = rev(summary_data$parameter),
  horiz = TRUE,
  las = 1,
  xlab = "Output range width",
  main = "Sensitivity Ranking by Output Range"
)

dev.off()

print(summary_data)
print(register)
