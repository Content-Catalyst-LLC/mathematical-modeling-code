# Base R workflow for ecological scenario and sustainability review.

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

register_path <- file.path(tables_dir, "ecology_model_register.csv")
scenario_path <- file.path(tables_dir, "sustainability_scenario_review.csv")
trajectory_path <- file.path(tables_dir, "baseline_resource_trajectory.csv")

if (!file.exists(register_path) || !file.exists(scenario_path) || !file.exists(trajectory_path)) {
  stop("Missing ecology and sustainability outputs. Run make python first.")
}

register <- read.csv(register_path, stringsAsFactors = FALSE)
scenarios <- read.csv(scenario_path, stringsAsFactors = FALSE)
trajectory <- read.csv(trajectory_path, stringsAsFactors = FALSE)

register$ecology_priority <- as.numeric(register$ecology_priority)
scenarios$final_stock <- as.numeric(scenarios$final_stock)
scenarios$minimum_resilience_margin <- as.numeric(scenarios$minimum_resilience_margin)
trajectory$year <- as.numeric(trajectory$year)
trajectory$stock <- as.numeric(trajectory$stock)

register <- register[order(-register$ecology_priority), ]
scenarios <- scenarios[order(-scenarios$minimum_resilience_margin), ]

breach_values <- tolower(as.character(scenarios$threshold_breach))
threshold_breach_count <- sum(breach_values %in% c("true", "1", "yes"))

summary_table <- data.frame(
  best_resilience_scenario = scenarios$scenario_name[1],
  mean_final_stock = mean(scenarios$final_stock),
  min_final_stock = min(scenarios$final_stock),
  max_final_stock = max(scenarios$final_stock),
  scenario_spread = max(scenarios$final_stock) - min(scenarios$final_stock),
  threshold_breach_count = threshold_breach_count,
  scenario_count = nrow(scenarios)
)

write.csv(
  register,
  file.path(tables_dir, "r_ecology_model_review_queue.csv"),
  row.names = FALSE
)

write.csv(
  scenarios,
  file.path(tables_dir, "r_sustainability_scenario_ranking.csv"),
  row.names = FALSE
)

write.csv(
  summary_table,
  file.path(tables_dir, "r_sustainability_summary.csv"),
  row.names = FALSE
)

png(file.path(figures_dir, "r_baseline_resource_trajectory.png"), width = 1000, height = 700)

plot(
  trajectory$year,
  trajectory$stock,
  type = "l",
  xlab = "Year",
  ylab = "Resource stock",
  main = "Baseline Resource Stock Trajectory"
)

abline(h = 250, lty = 2)

dev.off()

print(register)
print(summary_table)
print(scenarios)
