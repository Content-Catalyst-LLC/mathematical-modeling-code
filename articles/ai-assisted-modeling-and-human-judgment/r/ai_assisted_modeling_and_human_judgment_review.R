# Base R workflow for AI-assisted modeling oversight.

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

assistance_path <- file.path(tables_dir, "ai_assistance_register.csv")
judgment_path <- file.path(tables_dir, "human_judgment_review.csv")

if (!file.exists(assistance_path) || !file.exists(judgment_path)) {
  stop("Missing AI-assisted modeling outputs. Run make python first.")
}

assistance <- read.csv(assistance_path, stringsAsFactors = FALSE)
judgment <- read.csv(judgment_path, stringsAsFactors = FALSE)

assistance$review_priority <- as.numeric(assistance$review_priority)
judgment$judgment_risk_score <- as.numeric(judgment$judgment_risk_score)

assistance <- assistance[order(-assistance$review_priority), ]
judgment <- judgment[order(-judgment$judgment_risk_score), ]

summary_table <- data.frame(
  highest_risk_judgment_point = judgment$judgment_point[1],
  mean_judgment_risk_score = mean(judgment$judgment_risk_score),
  max_judgment_risk_score = max(judgment$judgment_risk_score),
  escalation_count = sum(judgment$review_class == "escalation_required"),
  case_count = nrow(judgment)
)

write.csv(assistance, file.path(tables_dir, "r_ai_assistance_review_queue.csv"), row.names = FALSE)
write.csv(judgment, file.path(tables_dir, "r_human_judgment_risk_ranking.csv"), row.names = FALSE)
write.csv(summary_table, file.path(tables_dir, "r_ai_assisted_modeling_summary.csv"), row.names = FALSE)

png(file.path(figures_dir, "r_human_judgment_risk_scores.png"), width = 1000, height = 700)

barplot(
  judgment$judgment_risk_score,
  names.arg = judgment$key,
  las = 2,
  ylab = "Judgment risk score",
  main = "AI-Assisted Modeling Human Judgment Risk Scores"
)

dev.off()

print(assistance)
print(summary_table)
print(judgment)
