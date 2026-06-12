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

trajectory_path <- file.path(tables_dir, "abm_adoption_trajectories.csv")
summary_path <- file.path(tables_dir, "abm_ensemble_summary.csv")
register_path <- file.path(tables_dir, "abm_model_register.csv")

if (!file.exists(trajectory_path) || !file.exists(summary_path)) {
  stop("Missing ABM outputs. Run make python first.")
}

trajectories <- read.csv(trajectory_path, stringsAsFactors = FALSE)
summary_data <- read.csv(summary_path, stringsAsFactors = FALSE)

trajectories$step <- as.integer(trajectories$step)
trajectories$adoption_share <- as.numeric(trajectories$adoption_share)

aggregate_means <- aggregate(
  adoption_share ~ scenario + step,
  data = trajectories,
  FUN = mean
)

write.csv(
  aggregate_means,
  file.path(tables_dir, "r_abm_mean_adoption_trajectories.csv"),
  row.names = FALSE
)

summary_data$review_class <- ifelse(
  summary_data$stdev_final_adoption > 0.20,
  "high stochastic variability",
  ifelse(summary_data$mean_final_adoption < 0.25, "low adoption outcome", "routine review")
)

write.csv(
  summary_data,
  file.path(tables_dir, "r_abm_ensemble_review_summary.csv"),
  row.names = FALSE
)

if (file.exists(register_path)) {
  register <- read.csv(register_path, stringsAsFactors = FALSE)

  register$priority <- ifelse(
    register$rule_risk_score >= 8,
    "high",
    ifelse(register$rule_risk_score >= 6, "medium", "low")
  )

  write.csv(
    register,
    file.path(tables_dir, "r_abm_model_review_queue.csv"),
    row.names = FALSE
  )
}

png(file.path(figures_dir, "r_abm_mean_adoption_trajectories.png"), width = 1100, height = 720)

scenarios <- unique(aggregate_means$scenario)

if (nrow(aggregate_means) > 0 && all(is.finite(range(aggregate_means$step))) && all(is.finite(range(aggregate_means$adoption_share)))) {
  plot(
    range(aggregate_means$step),
    range(aggregate_means$adoption_share),
    type = "n",
    xlab = "Simulation step",
    ylab = "Mean adoption share",
    main = "Agent-Based Adoption Model: Mean Ensemble Trajectories"
  )

  for (scenario in scenarios) {
    subset_data <- aggregate_means[aggregate_means$scenario == scenario, ]
    lines(subset_data$step, subset_data$adoption_share)
  }

  legend("bottomright", legend = scenarios, lty = 1, bty = "n")
  grid()
} else {
  plot.new()
  title(main = "Agent-Based Adoption Model: Mean Ensemble Trajectories")
  text(0.5, 0.5, "No finite ensemble trajectory values available.")
}

dev.off()

print(summary_data)
