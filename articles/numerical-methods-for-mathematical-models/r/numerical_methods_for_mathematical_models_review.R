# Base R workflow for numerical review and convergence diagnostics.

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

trajectory_path <- file.path(tables_dir, "euler_resource_trajectories.csv")
convergence_path <- file.path(tables_dir, "step_size_convergence_summary.csv")
register_path <- file.path(tables_dir, "numerical_method_register.csv")

if (!file.exists(trajectory_path) || !file.exists(convergence_path)) {
  stop("Missing numerical method outputs. Run make python first.")
}

trajectories <- read.csv(trajectory_path, stringsAsFactors = FALSE)
convergence <- read.csv(convergence_path, stringsAsFactors = FALSE)

trajectories$time <- as.numeric(trajectories$time)
trajectories$resource_stock <- as.numeric(trajectories$resource_stock)
trajectories$step_size <- as.numeric(trajectories$step_size)

convergence$review_class <- ifelse(
  convergence$absolute_difference_from_finest_step > 0.5,
  "step-size sensitivity review",
  "routine convergence review"
)

write.csv(
  convergence,
  file.path(tables_dir, "r_step_size_convergence_review.csv"),
  row.names = FALSE
)

if (file.exists(register_path)) {
  register <- read.csv(register_path, stringsAsFactors = FALSE)

  register$priority <- ifelse(
    register$numerical_risk_score >= 8,
    "high",
    ifelse(register$numerical_risk_score >= 6, "medium", "low")
  )

  write.csv(
    register,
    file.path(tables_dir, "r_numerical_method_review_queue.csv"),
    row.names = FALSE
  )
}

png(file.path(figures_dir, "r_euler_step_size_comparison.png"), width = 1100, height = 720)

step_sizes <- sort(unique(trajectories$step_size), decreasing = TRUE)

if (nrow(trajectories) > 0 && all(is.finite(range(trajectories$time))) && all(is.finite(range(trajectories$resource_stock)))) {
  plot(
    range(trajectories$time),
    range(trajectories$resource_stock),
    type = "n",
    xlab = "Time",
    ylab = "Resource stock",
    main = "Euler Approximation by Step Size"
  )

  for (h in step_sizes) {
    subset_data <- trajectories[trajectories$step_size == h, ]
    lines(subset_data$time, subset_data$resource_stock)
  }

  legend("topright", legend = paste("h =", step_sizes), lty = 1, bty = "n")
  grid()
} else {
  plot.new()
  title(main = "Euler Approximation by Step Size")
  text(0.5, 0.5, "No finite numerical trajectory values available.")
}

dev.off()

print(convergence)
