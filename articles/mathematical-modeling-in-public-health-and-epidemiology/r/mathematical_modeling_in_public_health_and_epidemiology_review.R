# Base R workflow for epidemic scenario and capacity review.

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

register_path <- file.path(tables_dir, "public_health_model_register.csv")
scenario_path <- file.path(tables_dir, "epidemic_scenario_review.csv")
trajectory_path <- file.path(tables_dir, "baseline_sir_trajectory.csv")

if (!file.exists(register_path) || !file.exists(scenario_path) || !file.exists(trajectory_path)) {
  stop("Missing public health modeling outputs. Run make python first.")
}

register <- read.csv(register_path, stringsAsFactors = FALSE)
scenarios <- read.csv(scenario_path, stringsAsFactors = FALSE)
trajectory <- read.csv(trajectory_path, stringsAsFactors = FALSE)

register$public_health_priority <- as.numeric(register$public_health_priority)
scenarios$peak_hospital_demand <- as.numeric(scenarios$peak_hospital_demand)
scenarios$peak_infectious <- as.numeric(scenarios$peak_infectious)
scenarios$capacity_margin <- as.numeric(scenarios$capacity_margin)
trajectory$day <- as.numeric(trajectory$day)
trajectory$infectious <- as.numeric(trajectory$infectious)

register <- register[order(-register$public_health_priority), ]
scenarios <- scenarios[order(scenarios$peak_hospital_demand), ]

breach_values <- tolower(as.character(scenarios$capacity_breach))
capacity_breach_count <- sum(breach_values %in% c("true", "1", "yes"))

summary_table <- data.frame(
  lowest_peak_hospital_demand_scenario = scenarios$scenario_name[1],
  mean_peak_infectious = mean(scenarios$peak_infectious),
  max_peak_infectious = max(scenarios$peak_infectious),
  min_peak_infectious = min(scenarios$peak_infectious),
  capacity_breach_count = capacity_breach_count,
  scenario_count = nrow(scenarios)
)

write.csv(
  register,
  file.path(tables_dir, "r_public_health_model_review_queue.csv"),
  row.names = FALSE
)

write.csv(
  scenarios,
  file.path(tables_dir, "r_epidemic_scenario_ranking.csv"),
  row.names = FALSE
)

write.csv(
  summary_table,
  file.path(tables_dir, "r_epidemic_summary.csv"),
  row.names = FALSE
)

png(file.path(figures_dir, "r_baseline_infectious_curve.png"), width = 1000, height = 700)

plot(
  trajectory$day,
  trajectory$infectious,
  type = "l",
  xlab = "Day",
  ylab = "Infectious population",
  main = "Baseline SIR Infectious Curve"
)

dev.off()

print(register)
print(summary_table)
print(scenarios)
