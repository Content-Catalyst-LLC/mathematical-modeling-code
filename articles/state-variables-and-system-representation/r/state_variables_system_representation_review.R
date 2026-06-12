# Base R workflow for state diagnostics and representation review.

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

summary_path <- file.path(tables_dir, "state_representation_summary.csv")
state_path <- file.path(tables_dir, "state_variable_register.csv")

if (!file.exists(summary_path)) {
  stop("Missing state_representation_summary.csv. Run make python first.")
}

summary_data <- read.csv(summary_path, stringsAsFactors = FALSE)

summary_data$representation_review <- ifelse(
  summary_data$domain_violations > 0,
  "domain violation detected",
  ifelse(
    summary_data$shortage_periods > 0 | summary_data$overflow_periods > 0,
    "state representation activates stress behavior",
    "state representation stable under scenario"
  )
)

write.csv(
  summary_data,
  file.path(tables_dir, "r_state_representation_review_summary.csv"),
  row.names = FALSE
)

if (file.exists(state_path)) {
  states <- read.csv(state_path, stringsAsFactors = FALSE)

  states$priority <- ifelse(
    states$state_risk_score >= 8,
    "high",
    ifelse(states$state_risk_score >= 6, "medium", "low")
  )

  write.csv(
    states,
    file.path(tables_dir, "r_state_review_queue.csv"),
    row.names = FALSE
  )
}

png(file.path(figures_dir, "r_shortage_by_state_representation.png"), width = 1100, height = 720)

barplot(
  height = summary_data$total_shortage,
  names.arg = summary_data$representation,
  las = 2,
  ylab = "Total shortage",
  main = "Shortage Across State Representations"
)

grid()
dev.off()

print(summary_data)
