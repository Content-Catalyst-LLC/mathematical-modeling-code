# Base R workflow for scale and unit diagnostics.

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

summary_path <- file.path(tables_dir, "unit_scale_summary.csv")
unit_path <- file.path(tables_dir, "unit_register.csv")

if (!file.exists(summary_path)) {
  stop("Missing unit_scale_summary.csv. Run make python first.")
}

summary_data <- read.csv(summary_path, stringsAsFactors = FALSE)

summary_data$scale_review <- ifelse(
  summary_data$domain_violations > 0,
  "domain violation detected",
  ifelse(
    summary_data$shortage_periods > 0 | summary_data$overflow_periods > 0,
    "constraint or scale limit active",
    "unit and scale behavior stable"
  )
)

write.csv(
  summary_data,
  file.path(tables_dir, "r_unit_scale_review_summary.csv"),
  row.names = FALSE
)

if (file.exists(unit_path)) {
  units <- read.csv(unit_path, stringsAsFactors = FALSE)

  units$priority <- ifelse(
    units$unit_risk_score >= 8,
    "high",
    ifelse(units$unit_risk_score >= 6, "medium", "low")
  )

  write.csv(
    units,
    file.path(tables_dir, "r_unit_review_queue.csv"),
    row.names = FALSE
  )
}

png(file.path(figures_dir, "r_storage_fraction_range.png"), width = 1100, height = 720)

barplot(
  height = rbind(summary_data$min_storage_fraction, summary_data$max_storage_fraction),
  beside = TRUE,
  names.arg = summary_data$scenario,
  las = 2,
  ylab = "Storage fraction",
  main = "Storage Fraction Ranges Across Unit and Scale Scenarios"
)

legend(
  "topright",
  legend = c("Minimum storage fraction", "Maximum storage fraction"),
  fill = gray.colors(2)
)

grid()
dev.off()

print(summary_data)
