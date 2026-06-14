# Base R workflow for decision summary and threshold review.

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

options_path <- file.path(tables_dir, "decision_option_review.csv")
register_path <- file.path(tables_dir, "interpretation_register.csv")

if (!file.exists(options_path) || !file.exists(register_path)) {
  stop("Missing decision outputs. Run make python first.")
}

options <- read.csv(options_path, stringsAsFactors = FALSE)
register <- read.csv(register_path, stringsAsFactors = FALSE)

options$decision_score <- as.numeric(options$decision_score)
options$threshold_margin <- as.numeric(options$threshold_margin)
options$implementation_burden <- as.numeric(options$implementation_burden)
options$consequence_if_wrong <- as.numeric(options$consequence_if_wrong)

options <- options[order(-options$decision_score), ]

summary_table <- data.frame(
  best_scored_option = options$option_name[1],
  max_score = max(options$decision_score),
  min_score = min(options$decision_score),
  fragile_option_count = sum(options$robustness_class == "fragile"),
  option_count = nrow(options)
)

register$priority_class <- ifelse(
  register$interpretation_priority >= 8,
  "high",
  ifelse(register$interpretation_priority >= 6, "medium", "low")
)

write.csv(
  options,
  file.path(tables_dir, "r_decision_option_ranking.csv"),
  row.names = FALSE
)

write.csv(
  summary_table,
  file.path(tables_dir, "r_decision_summary.csv"),
  row.names = FALSE
)

write.csv(
  register,
  file.path(tables_dir, "r_interpretation_review_queue.csv"),
  row.names = FALSE
)

png(file.path(figures_dir, "r_decision_option_scores.png"), width = 1000, height = 700)

barplot(
  options$decision_score,
  names.arg = options$key,
  las = 2,
  ylab = "Decision score",
  main = "Decision Option Scores Under Model Interpretation Review"
)

dev.off()

print(summary_table)
print(options)
print(register)
