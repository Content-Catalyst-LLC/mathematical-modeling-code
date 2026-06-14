# Base R workflow for AI model evaluation and governance review.

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

register_path <- file.path(tables_dir, "ai_model_register.csv")
candidate_path <- file.path(tables_dir, "ai_model_candidate_review.csv")

if (!file.exists(register_path) || !file.exists(candidate_path)) {
  stop("Missing AI model outputs. Run make python first.")
}

register <- read.csv(register_path, stringsAsFactors = FALSE)
candidates <- read.csv(candidate_path, stringsAsFactors = FALSE)

register$model_priority <- as.numeric(register$model_priority)
candidates$governance_score <- as.numeric(candidates$governance_score)
candidates$validation_score <- as.numeric(candidates$validation_score)
candidates$calibration_error <- as.numeric(candidates$calibration_error)
candidates$subgroup_error_gap <- as.numeric(candidates$subgroup_error_gap)
candidates$drift_score <- as.numeric(candidates$drift_score)
candidates$privacy_risk <- as.numeric(candidates$privacy_risk)

register <- register[order(-register$model_priority), ]
candidates <- candidates[order(-candidates$governance_score), ]

review_values <- tolower(as.character(candidates$requires_review))
review_required_count <- sum(review_values %in% c("true", "1", "yes"))

summary_table <- data.frame(
  best_governed_candidate = candidates$model_name[1],
  mean_governance_score = mean(candidates$governance_score),
  max_governance_score = max(candidates$governance_score),
  min_governance_score = min(candidates$governance_score),
  review_required_count = review_required_count,
  candidate_count = nrow(candidates)
)

write.csv(
  register,
  file.path(tables_dir, "r_ai_model_review_queue.csv"),
  row.names = FALSE
)

write.csv(
  candidates,
  file.path(tables_dir, "r_ai_candidate_ranking.csv"),
  row.names = FALSE
)

write.csv(
  summary_table,
  file.path(tables_dir, "r_ai_governance_summary.csv"),
  row.names = FALSE
)

png(file.path(figures_dir, "r_ai_governance_scores.png"), width = 1000, height = 700)

barplot(
  candidates$governance_score,
  names.arg = candidates$key,
  las = 2,
  ylab = "Governance score",
  main = "AI Model Candidate Governance Scores"
)

dev.off()

print(register)
print(summary_table)
print(candidates)
