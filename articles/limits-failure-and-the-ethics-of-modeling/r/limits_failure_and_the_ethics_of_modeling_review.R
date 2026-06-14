# Base R workflow for model failure and ethics review.

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

failure_path <- file.path(tables_dir, "model_failure_register.csv")
risk_path <- file.path(tables_dir, "model_ethics_risk_review.csv")

if (!file.exists(failure_path) || !file.exists(risk_path)) {
  stop("Missing model ethics outputs. Run make python first.")
}

failures <- read.csv(failure_path, stringsAsFactors = FALSE)
risks <- read.csv(risk_path, stringsAsFactors = FALSE)

failures$failure_priority <- as.numeric(failures$failure_priority)
risks$ethical_risk_score <- as.numeric(risks$ethical_risk_score)

failures <- failures[order(-failures$failure_priority), ]
risks <- risks[order(-risks$ethical_risk_score), ]

high_review_count <- sum(risks$review_class == "high_ethics_review_required")

summary_table <- data.frame(
  highest_risk_model = risks$model_name[1],
  mean_ethical_risk_score = mean(risks$ethical_risk_score),
  max_ethical_risk_score = max(risks$ethical_risk_score),
  min_ethical_risk_score = min(risks$ethical_risk_score),
  high_ethics_review_count = high_review_count,
  case_count = nrow(risks)
)

write.csv(
  failures,
  file.path(tables_dir, "r_model_failure_governance_queue.csv"),
  row.names = FALSE
)

write.csv(
  risks,
  file.path(tables_dir, "r_model_ethics_risk_ranking.csv"),
  row.names = FALSE
)

write.csv(
  summary_table,
  file.path(tables_dir, "r_model_ethics_summary.csv"),
  row.names = FALSE
)

png(file.path(figures_dir, "r_model_ethics_risk_scores.png"), width = 1000, height = 700)

barplot(
  risks$ethical_risk_score,
  names.arg = risks$key,
  las = 2,
  ylab = "Ethical risk score",
  main = "Model Ethics Risk Scores"
)

dev.off()

print(failures)
print(summary_table)
print(risks)
