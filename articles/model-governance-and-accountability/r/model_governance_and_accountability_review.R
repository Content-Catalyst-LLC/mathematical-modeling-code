# Base R workflow for model governance and accountability review.

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

register_path <- file.path(tables_dir, "model_governance_register.csv")
risk_path <- file.path(tables_dir, "model_governance_risk_review.csv")

if (!file.exists(register_path) || !file.exists(risk_path)) {
  stop("Missing model governance outputs. Run make python first.")
}

register <- read.csv(register_path, stringsAsFactors = FALSE)
risk <- read.csv(risk_path, stringsAsFactors = FALSE)

register$governance_priority <- as.numeric(register$governance_priority)
risk$governance_risk_score <- as.numeric(risk$governance_risk_score)

register <- register[order(-register$governance_priority), ]
risk <- risk[order(-risk$governance_risk_score), ]

summary_table <- data.frame(
  highest_risk_model = risk$model_name[1],
  mean_governance_risk_score = mean(risk$governance_risk_score),
  max_governance_risk_score = max(risk$governance_risk_score),
  escalation_count = sum(risk$review_class == "escalation_required"),
  case_count = nrow(risk)
)

write.csv(register, file.path(tables_dir, "r_model_governance_review_queue.csv"), row.names = FALSE)
write.csv(risk, file.path(tables_dir, "r_model_governance_risk_ranking.csv"), row.names = FALSE)
write.csv(summary_table, file.path(tables_dir, "r_model_governance_summary.csv"), row.names = FALSE)

png(file.path(figures_dir, "r_model_governance_risk_scores.png"), width = 1000, height = 700)
barplot(
  risk$governance_risk_score,
  names.arg = risk$key,
  las = 2,
  ylab = "Governance risk score",
  main = "Model Governance Risk Scores"
)
dev.off()

print(register)
print(summary_table)
print(risk)
