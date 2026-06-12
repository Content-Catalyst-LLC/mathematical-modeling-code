# Base R workflow for constraint and logic diagnostics.

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

summary_path <- file.path(tables_dir, "logic_scenario_summary.csv")
statement_path <- file.path(tables_dir, "formal_statement_register.csv")

if (!file.exists(summary_path)) {
  stop("Missing logic_scenario_summary.csv. Run make python first.")
}

summary_data <- read.csv(summary_path, stringsAsFactors = FALSE)

summary_data$logic_review <- ifelse(
  summary_data$domain_violations > 0,
  "domain violation detected",
  ifelse(
    summary_data$shortage_periods > 0 | summary_data$logic_activation_periods > 0,
    "constraint or conditional logic active",
    "logic stable under scenario"
  )
)

write.csv(
  summary_data,
  file.path(tables_dir, "r_logic_review_summary.csv"),
  row.names = FALSE
)

if (file.exists(statement_path)) {
  statements <- read.csv(statement_path, stringsAsFactors = FALSE)

  statements$priority <- ifelse(
    statements$statement_risk_score >= 8,
    "high",
    ifelse(statements$statement_risk_score >= 6, "medium", "low")
  )

  write.csv(
    statements,
    file.path(tables_dir, "r_formal_statement_review_queue.csv"),
    row.names = FALSE
  )
}

png(file.path(figures_dir, "r_shortage_and_logic_activation.png"), width = 1100, height = 720)

barplot(
  height = rbind(summary_data$total_shortage, summary_data$logic_activation_periods),
  beside = TRUE,
  names.arg = summary_data$scenario,
  las = 2,
  ylab = "Diagnostic count or magnitude",
  main = "Shortage and Conditional Logic Activation"
)

legend(
  "topright",
  legend = c("Total shortage", "Logic activation periods"),
  fill = gray.colors(2)
)

grid()
dev.off()

print(summary_data)
