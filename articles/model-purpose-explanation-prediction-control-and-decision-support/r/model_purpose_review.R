# Base R workflow for model-purpose and decision-support diagnostics.

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

summary_path <- file.path(tables_dir, "purpose_scenario_summary.csv")
purpose_path <- file.path(tables_dir, "purpose_register.csv")

if (!file.exists(summary_path)) {
  stop("Missing purpose_scenario_summary.csv. Run make python first.")
}

summary_data <- read.csv(summary_path, stringsAsFactors = FALSE)

summary_data$review_note <- ifelse(
  summary_data$purpose == "explanation",
  "interpret as mechanism demonstration",
  ifelse(
    summary_data$purpose == "prediction",
    "requires forecast validation and uncertainty",
    ifelse(
      summary_data$purpose == "control",
      "requires feedback, robustness, and monitoring",
      ifelse(
        summary_data$purpose == "optimization",
        "requires objective and constraint sensitivity",
        "requires decision context, trade-offs, and governance"
      )
    )
  )
)

write.csv(
  summary_data,
  file.path(tables_dir, "r_purpose_scenario_review.csv"),
  row.names = FALSE
)

if (file.exists(purpose_path)) {
  purpose_data <- read.csv(purpose_path, stringsAsFactors = FALSE)

  purpose_data$priority <- ifelse(
    purpose_data$purpose_risk_score >= 8,
    "high",
    ifelse(purpose_data$purpose_risk_score >= 6, "medium", "low")
  )

  write.csv(
    purpose_data,
    file.path(tables_dir, "r_purpose_review_queue.csv"),
    row.names = FALSE
  )
}

png(file.path(figures_dir, "r_shortage_risk_by_model_purpose.png"), width = 1100, height = 720)

barplot(
  height = summary_data$shortage_risk,
  names.arg = summary_data$purpose,
  las = 2,
  ylab = "Shortage risk",
  main = "Shortage Risk Across Model Purposes"
)

grid()
dev.off()

print(summary_data)
