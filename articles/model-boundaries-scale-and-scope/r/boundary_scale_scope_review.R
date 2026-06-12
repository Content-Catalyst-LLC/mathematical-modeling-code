# Base R workflow for boundary, scale, and scope diagnostics.

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

summary_path <- file.path(tables_dir, "boundary_scenario_summary.csv")
boundary_path <- file.path(tables_dir, "boundary_register.csv")

if (!file.exists(summary_path)) {
  stop("Missing boundary_scenario_summary.csv. Run make python first.")
}

summary_data <- read.csv(summary_path, stringsAsFactors = FALSE)

summary_data$scope_review <- ifelse(
  summary_data$shortage_periods > 0,
  "scope requires qualification",
  "acceptable under stated boundary"
)

write.csv(
  summary_data,
  file.path(tables_dir, "r_boundary_scope_review.csv"),
  row.names = FALSE
)

if (file.exists(boundary_path)) {
  boundaries <- read.csv(boundary_path, stringsAsFactors = FALSE)

  boundaries$priority <- ifelse(
    boundaries$boundary_risk_score >= 8,
    "high",
    ifelse(boundaries$boundary_risk_score >= 6, "medium", "low")
  )

  write.csv(
    boundaries,
    file.path(tables_dir, "r_boundary_review_queue.csv"),
    row.names = FALSE
  )
}

png(file.path(figures_dir, "r_shortage_risk_by_boundary_version.png"), width = 1100, height = 720)

barplot(
  height = summary_data$shortage_risk,
  names.arg = summary_data$scenario,
  las = 2,
  ylab = "Shortage risk",
  main = "Shortage Risk Across Boundary Versions"
)

grid()
dev.off()

print(summary_data)
