# Base R workflow for complexity scenario and robustness review.

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

model_path <- file.path(tables_dir, "complexity_model_register.csv")
scenario_path <- file.path(tables_dir, "complexity_scenario_review.csv")

if (!file.exists(model_path) || !file.exists(scenario_path)) {
  stop("Missing complexity modeling outputs. Run make python first.")
}

models <- read.csv(model_path, stringsAsFactors = FALSE)
scenarios <- read.csv(scenario_path, stringsAsFactors = FALSE)

models$model_priority <- as.numeric(models$model_priority)
scenarios$fragility_score <- as.numeric(scenarios$fragility_score)
scenarios$robust_value <- as.numeric(scenarios$robust_value)
scenarios$stress_level <- as.numeric(scenarios$stress_level)
scenarios$uncertainty_level <- as.numeric(scenarios$uncertainty_level)

models <- models[order(-models$model_priority), ]
risk_ranking <- scenarios[order(-scenarios$fragility_score), ]
robust_ranking <- scenarios[order(-scenarios$robust_value), ]

summary_table <- data.frame(
  highest_fragility_scenario = risk_ranking$scenario_name[1],
  best_robust_value_scenario = robust_ranking$scenario_name[1],
  mean_fragility_score = mean(scenarios$fragility_score),
  mean_robust_value = mean(scenarios$robust_value),
  max_fragility_score = max(scenarios$fragility_score),
  scenario_count = nrow(scenarios)
)

write.csv(models, file.path(tables_dir, "r_complexity_model_review_queue.csv"), row.names = FALSE)
write.csv(risk_ranking, file.path(tables_dir, "r_complexity_fragility_ranking.csv"), row.names = FALSE)
write.csv(robust_ranking, file.path(tables_dir, "r_complexity_robust_value_ranking.csv"), row.names = FALSE)
write.csv(summary_table, file.path(tables_dir, "r_complexity_summary.csv"), row.names = FALSE)

png(file.path(figures_dir, "r_complexity_fragility_scores.png"), width = 1000, height = 700)

barplot(
  risk_ranking$fragility_score,
  names.arg = risk_ranking$key,
  las = 2,
  ylab = "Fragility score",
  main = "Complexity Scenario Fragility Scores"
)

dev.off()

print(models)
print(summary_table)
print(risk_ranking)
print(robust_ranking)
