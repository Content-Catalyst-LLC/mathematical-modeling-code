# Base R workflow for assumption review and scenario diagnostics.

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

summary_path <- file.path(tables_dir, "resource_scenario_summary.csv")
assumption_path <- file.path(tables_dir, "assumption_register.csv")

if (!file.exists(summary_path)) {
  stop("Missing resource_scenario_summary.csv. Run make python first.")
}

summary_data <- read.csv(summary_path, stringsAsFactors = FALSE)

summary_data$scenario_review <- ifelse(
  summary_data$shortage_periods > 0,
  "requires review",
  "acceptable under stated assumptions"
)

write.csv(
  summary_data,
  file.path(tables_dir, "r_scenario_design_review.csv"),
  row.names = FALSE
)

if (file.exists(assumption_path)) {
  assumptions <- read.csv(assumption_path, stringsAsFactors = FALSE)

  assumptions$priority <- ifelse(
    assumptions$assumption_risk_score >= 8,
    "high",
    ifelse(assumptions$assumption_risk_score >= 6, "medium", "low")
  )

  write.csv(
    assumptions,
    file.path(tables_dir, "r_assumption_review_queue.csv"),
    row.names = FALSE
  )
}

png(file.path(figures_dir, "r_shortage_risk_by_scenario.png"), width = 1100, height = 720)

barplot(
  height = summary_data$shortage_risk,
  names.arg = summary_data$scenario,
  las = 2,
  ylab = "Shortage risk",
  main = "Shortage Risk Under Simplified Model Assumptions"
)

grid()
dev.off()

print(summary_data)
