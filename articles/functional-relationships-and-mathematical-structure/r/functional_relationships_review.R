# Base R workflow for comparing functional forms and structural diagnostics.

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

summary_path <- file.path(tables_dir, "structure_scenario_summary.csv")
relationship_path <- file.path(tables_dir, "relationship_register.csv")

if (!file.exists(summary_path)) {
  stop("Missing structure_scenario_summary.csv. Run make python first.")
}

summary_data <- read.csv(summary_path, stringsAsFactors = FALSE)

summary_data$structure_review <- ifelse(
  summary_data$shortage_periods > 0 | summary_data$overflow_periods > 0,
  "structure activates constraint or failure mode",
  "structure stable under scenario"
)

write.csv(
  summary_data,
  file.path(tables_dir, "r_structure_review_summary.csv"),
  row.names = FALSE
)

if (file.exists(relationship_path)) {
  relationships <- read.csv(relationship_path, stringsAsFactors = FALSE)

  relationships$priority <- ifelse(
    relationships$structure_risk_score >= 8,
    "high",
    ifelse(relationships$structure_risk_score >= 6, "medium", "low")
  )

  write.csv(
    relationships,
    file.path(tables_dir, "r_relationship_review_queue.csv"),
    row.names = FALSE
  )
}

png(file.path(figures_dir, "r_total_shortage_by_structure.png"), width = 1100, height = 720)

barplot(
  height = summary_data$total_shortage,
  names.arg = summary_data$structure,
  las = 2,
  ylab = "Total shortage",
  main = "Structural Diagnostics Across Functional Forms"
)

grid()
dev.off()

print(summary_data)
