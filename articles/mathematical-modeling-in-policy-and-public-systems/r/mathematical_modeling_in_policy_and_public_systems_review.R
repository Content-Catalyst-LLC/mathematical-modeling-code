# Base R workflow for policy option and public-system review.

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

register_path <- file.path(tables_dir, "policy_model_register.csv")
option_path <- file.path(tables_dir, "policy_option_review.csv")

if (!file.exists(register_path) || !file.exists(option_path)) {
  stop("Missing policy modeling outputs. Run make python first.")
}

register <- read.csv(register_path, stringsAsFactors = FALSE)
options <- read.csv(option_path, stringsAsFactors = FALSE)

register$policy_priority <- as.numeric(register$policy_priority)
options$public_value_score <- as.numeric(options$public_value_score)
options$equity_score <- as.numeric(options$equity_score)
options$public_risk <- as.numeric(options$public_risk)
options$total_cost <- as.numeric(options$total_cost)
options$budget_margin <- as.numeric(options$budget_margin)

register <- register[order(-register$policy_priority), ]
options <- options[order(-options$public_value_score), ]

budget_values <- tolower(as.character(options$budget_violation))
budget_violation_count <- sum(budget_values %in% c("true", "1", "yes"))
equity_review_count <- sum(options$equity_score < 0.65)
risk_review_count <- sum(options$public_risk > 0.38)

summary_table <- data.frame(
  best_scored_option = options$option_name[1],
  mean_public_value_score = mean(options$public_value_score),
  max_public_value_score = max(options$public_value_score),
  min_public_value_score = min(options$public_value_score),
  budget_violation_count = budget_violation_count,
  equity_review_count = equity_review_count,
  risk_review_count = risk_review_count,
  option_count = nrow(options)
)

write.csv(
  register,
  file.path(tables_dir, "r_policy_model_review_queue.csv"),
  row.names = FALSE
)

write.csv(
  options,
  file.path(tables_dir, "r_policy_option_ranking.csv"),
  row.names = FALSE
)

write.csv(
  summary_table,
  file.path(tables_dir, "r_policy_option_summary.csv"),
  row.names = FALSE
)

png(file.path(figures_dir, "r_policy_option_scores.png"), width = 1000, height = 700)

barplot(
  options$public_value_score,
  names.arg = options$key,
  las = 2,
  ylab = "Public value score",
  main = "Policy Option Scores Under Public-System Review"
)

dev.off()

print(register)
print(summary_table)
print(options)
