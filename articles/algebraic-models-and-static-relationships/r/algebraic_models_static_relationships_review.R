# Base R workflow for static relationship diagnostics.

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

scenario_path <- file.path(tables_dir, "static_allocation_scenarios.csv")
relationship_path <- file.path(tables_dir, "algebraic_relationship_register.csv")

if (!file.exists(scenario_path)) {
  stop("Missing static_allocation_scenarios.csv. Run make python first.")
}

scenario_data <- read.csv(scenario_path, stringsAsFactors = FALSE)

scenario_data$review_priority <- ifelse(
  scenario_data$feasible == "False" | scenario_data$feasible == FALSE,
  "high",
  ifelse(scenario_data$budget_slack <= 10, "medium", "low")
)

write.csv(
  scenario_data,
  file.path(tables_dir, "r_static_relationship_review_summary.csv"),
  row.names = FALSE
)

if (file.exists(relationship_path)) {
  relationships <- read.csv(relationship_path, stringsAsFactors = FALSE)

  relationships$priority <- ifelse(
    relationships$relationship_risk_score >= 8,
    "high",
    ifelse(relationships$relationship_risk_score >= 6, "medium", "low")
  )

  write.csv(
    relationships,
    file.path(tables_dir, "r_algebraic_relationship_review_queue.csv"),
    row.names = FALSE
  )
}

png(file.path(figures_dir, "r_static_scenario_benefit_and_slack.png"), width = 1100, height = 720)

barplot(
  height = rbind(scenario_data$total_benefit, scenario_data$budget_slack),
  beside = TRUE,
  names.arg = scenario_data$scenario,
  las = 2,
  ylab = "Value",
  main = "Static Algebraic Scenario Diagnostics"
)

legend(
  "topright",
  legend = c("Total benefit", "Budget slack"),
  fill = gray.colors(2)
)

grid()
dev.off()

print(scenario_data)
