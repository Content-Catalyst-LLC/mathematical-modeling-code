# Base R workflow for reviewing abstraction and representation outputs.

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

summary_path <- file.path(tables_dir, "stock_flow_summary.csv")
audit_path <- file.path(tables_dir, "representation_audit.csv")

if (!file.exists(summary_path)) {
  stop("Missing stock_flow_summary.csv. Run make python first.")
}

summary_data <- read.csv(summary_path, stringsAsFactors = FALSE)
summary_data$shortage_flag <- ifelse(summary_data$shortage_periods > 0, "shortage observed", "no shortage")
summary_data$representation_review <- ifelse(
  summary_data$shortage_periods > 0,
  "review abstraction and scenario assumptions",
  "acceptable under stated abstraction"
)

write.csv(
  summary_data,
  file.path(tables_dir, "r_abstraction_level_review.csv"),
  row.names = FALSE
)

if (file.exists(audit_path)) {
  audit_data <- read.csv(audit_path, stringsAsFactors = FALSE)
  audit_review <- data.frame(
    target_feature = audit_data$target_feature,
    represented_as = audit_data$formal_representation,
    representation_risk_score = audit_data$representation_risk_score,
    review_question = audit_data$review_question,
    omitted_detail = audit_data$omitted_detail
  )
  write.csv(
    audit_review,
    file.path(tables_dir, "r_representation_review_queue.csv"),
    row.names = FALSE
  )
}

png(file.path(figures_dir, "r_final_stock_by_representation_scenario.png"), width = 1100, height = 720)
barplot(
  height = summary_data$final_stock,
  names.arg = summary_data$scenario,
  las = 2,
  ylab = "Final stock",
  main = "Final Stock by Scenario Under Aggregate Stock-Flow Representation"
)
grid()
dev.off()

print(summary_data)
