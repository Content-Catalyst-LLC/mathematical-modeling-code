# Base R workflow for scientific model evidence review.

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

register_path <- file.path(tables_dir, "scientific_model_register.csv")
scenario_path <- file.path(tables_dir, "population_scenario_summary.csv")
trajectory_path <- file.path(tables_dir, "baseline_population_trajectory.csv")

if (!file.exists(register_path) || !file.exists(scenario_path) || !file.exists(trajectory_path)) {
  stop("Missing scientific modeling outputs. Run make python first.")
}

register <- read.csv(register_path, stringsAsFactors = FALSE)
scenarios <- read.csv(scenario_path, stringsAsFactors = FALSE)
trajectory <- read.csv(trajectory_path, stringsAsFactors = FALSE)

register$scientific_priority <- as.numeric(register$scientific_priority)
scenarios$final_population <- as.numeric(scenarios$final_population)
trajectory$year <- as.numeric(trajectory$year)
trajectory$population <- as.numeric(trajectory$population)

register <- register[order(-register$scientific_priority), ]

scenario_summary <- data.frame(
  mean_final_population = mean(scenarios$final_population),
  min_final_population = min(scenarios$final_population),
  max_final_population = max(scenarios$final_population),
  scenario_spread = max(scenarios$final_population) - min(scenarios$final_population),
  scenario_count = nrow(scenarios)
)

write.csv(
  register,
  file.path(tables_dir, "r_scientific_model_review_queue.csv"),
  row.names = FALSE
)

write.csv(
  scenario_summary,
  file.path(tables_dir, "r_population_scenario_summary.csv"),
  row.names = FALSE
)

png(file.path(figures_dir, "r_baseline_population_trajectory.png"), width = 1000, height = 700)

plot(
  trajectory$year,
  trajectory$population,
  type = "l",
  xlab = "Year",
  ylab = "Population",
  main = "Baseline Logistic Population Trajectory"
)

dev.off()

print(register)
print(scenario_summary)
