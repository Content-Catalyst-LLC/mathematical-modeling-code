# Base R workflow for simulation review and ensemble diagnostics.

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

trajectory_path <- file.path(tables_dir, "simulation_trajectories.csv")
summary_path <- file.path(tables_dir, "simulation_scenario_summary.csv")
register_path <- file.path(tables_dir, "simulation_model_register.csv")

if (!file.exists(trajectory_path) || !file.exists(summary_path)) {
  stop("Missing simulation outputs. Run make python first.")
}

trajectories <- read.csv(trajectory_path, stringsAsFactors = FALSE)
summary_data <- read.csv(summary_path, stringsAsFactors = FALSE)

trajectories$step <- as.integer(trajectories$step)
trajectories$resource_stock <- as.numeric(trajectories$resource_stock)

mean_trajectories <- aggregate(
  resource_stock ~ scenario + step,
  data = trajectories,
  FUN = mean
)

write.csv(
  mean_trajectories,
  file.path(tables_dir, "r_mean_simulation_trajectories.csv"),
  row.names = FALSE
)

summary_data$review_class <- ifelse(
  summary_data$depletion_probability > 0.25,
  "high depletion risk",
  ifelse(summary_data$stdev_final_stock > 15, "high variability", "routine review")
)

write.csv(
  summary_data,
  file.path(tables_dir, "r_simulation_scenario_review_summary.csv"),
  row.names = FALSE
)

if (file.exists(register_path)) {
  register <- read.csv(register_path, stringsAsFactors = FALSE)
  register$priority <- ifelse(
    register$simulation_risk_score >= 8,
    "high",
    ifelse(register$simulation_risk_score >= 6, "medium", "low")
  )

  write.csv(
    register,
    file.path(tables_dir, "r_simulation_model_review_queue.csv"),
    row.names = FALSE
  )
}

png(file.path(figures_dir, "r_mean_simulation_trajectories.png"), width = 1100, height = 720)

scenarios <- unique(mean_trajectories$scenario)

if (nrow(mean_trajectories) > 0 && all(is.finite(range(mean_trajectories$step))) && all(is.finite(range(mean_trajectories$resource_stock)))) {
  plot(
    range(mean_trajectories$step),
    range(mean_trajectories$resource_stock),
    type = "n",
    xlab = "Simulation step",
    ylab = "Mean resource stock",
    main = "Simulation Scenario Mean Trajectories"
  )

  for (scenario in scenarios) {
    subset_data <- mean_trajectories[mean_trajectories$scenario == scenario, ]
    lines(subset_data$step, subset_data$resource_stock)
  }

  legend("topright", legend = scenarios, lty = 1, bty = "n")
  grid()
} else {
  plot.new()
  title(main = "Simulation Scenario Mean Trajectories")
  text(0.5, 0.5, "No finite simulation values available.")
}

dev.off()

print(summary_data)
