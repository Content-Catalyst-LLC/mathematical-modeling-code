# Base R workflow for dynamic model review and time-series diagnostics.

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

timeseries_path <- file.path(tables_dir, "dynamic_model_timeseries.csv")
summary_path <- file.path(tables_dir, "dynamic_model_summary.csv")
register_path <- file.path(tables_dir, "dynamic_model_register.csv")

if (!file.exists(timeseries_path) || !file.exists(summary_path)) {
  stop("Missing dynamic model outputs. Run make python first.")
}

timeseries <- read.csv(timeseries_path, stringsAsFactors = FALSE)
summary_data <- read.csv(summary_path, stringsAsFactors = FALSE)

summary_data$dynamic_review <- ifelse(
  summary_data$domain_violations > 0,
  "domain violation detected",
  ifelse(
    summary_data$shortage_periods > 0 | summary_data$overflow_periods > 0,
    "boundary or stress behavior active",
    "trajectory stable under scenario"
  )
)

write.csv(
  summary_data,
  file.path(tables_dir, "r_dynamic_model_review_summary.csv"),
  row.names = FALSE
)

if (file.exists(register_path)) {
  register <- read.csv(register_path, stringsAsFactors = FALSE)

  register$priority <- ifelse(
    register$dynamic_risk_score >= 8,
    "high",
    ifelse(register$dynamic_risk_score >= 6, "medium", "low")
  )

  write.csv(
    register,
    file.path(tables_dir, "r_dynamic_model_review_queue.csv"),
    row.names = FALSE
  )
}

png(file.path(figures_dir, "r_dynamic_storage_trajectories.png"), width = 1100, height = 720)

scenario_names <- unique(timeseries$scenario)
plot(
  NULL,
  xlim = range(timeseries$time),
  ylim = range(timeseries$storage),
  xlab = "Time",
  ylab = "Storage",
  main = "Dynamic Storage Trajectories"
)

for (scenario in scenario_names) {
  rows <- timeseries[timeseries$scenario == scenario, ]
  lines(rows$time, rows$storage, lwd = 2)
}

legend("bottomright", legend = scenario_names, lwd = 2, cex = 0.85)
grid()
dev.off()

print(summary_data)
