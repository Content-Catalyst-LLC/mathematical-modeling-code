# Base R workflow for distribution review and uncertainty diagnostics.

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

runs_path <- file.path(tables_dir, "probabilistic_simulation_runs.csv")
summary_path <- file.path(tables_dir, "probabilistic_risk_summary.csv")
register_path <- file.path(tables_dir, "probability_model_register.csv")

if (!file.exists(runs_path) || !file.exists(summary_path)) {
  stop("Missing probabilistic outputs. Run make python first.")
}

runs <- read.csv(runs_path, stringsAsFactors = FALSE)
summary_data <- read.csv(summary_path, stringsAsFactors = FALSE)

summary_data$risk_review <- ifelse(
  summary_data$shortage_probability >= 0.25 | summary_data$shortage_q95 > 20,
  "high review priority",
  ifelse(
    summary_data$shortage_probability >= 0.10 | summary_data$shortage_q90 > 10,
    "moderate review priority",
    "routine monitoring"
  )
)

write.csv(
  summary_data,
  file.path(tables_dir, "r_probabilistic_risk_review_summary.csv"),
  row.names = FALSE
)

if (file.exists(register_path)) {
  register <- read.csv(register_path, stringsAsFactors = FALSE)

  register$priority <- ifelse(
    register$probability_risk_score >= 8,
    "high",
    ifelse(register$probability_risk_score >= 6, "medium", "low")
  )

  write.csv(
    register,
    file.path(tables_dir, "r_probability_model_review_queue.csv"),
    row.names = FALSE
  )
}

png(file.path(figures_dir, "r_shortage_distribution_histogram.png"), width = 1100, height = 720)

hist(
  runs$shortage,
  breaks = 40,
  xlab = "Shortage",
  main = "Distribution of Simulated Shortage Outcomes"
)

grid()
dev.off()

print(summary_data)
