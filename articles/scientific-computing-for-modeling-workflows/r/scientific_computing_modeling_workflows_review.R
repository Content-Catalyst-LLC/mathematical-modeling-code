# Base R workflow review and reproducibility diagnostics.

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

trajectory_path <- file.path(tables_dir, "resource_model_trajectories.csv")
summary_path <- file.path(tables_dir, "resource_model_summary.csv")
register_path <- file.path(tables_dir, "scientific_computing_workflow_register.csv")
output_index_path <- file.path(tables_dir, "workflow_output_index.csv")

if (!file.exists(trajectory_path) || !file.exists(summary_path) || !file.exists(register_path)) {
  stop("Missing workflow outputs. Run make python first.")
}

trajectories <- read.csv(trajectory_path, stringsAsFactors = FALSE)
summary_data <- read.csv(summary_path, stringsAsFactors = FALSE)
register <- read.csv(register_path, stringsAsFactors = FALSE)

trajectories$step <- as.integer(trajectories$step)
trajectories$resource_stock <- as.numeric(trajectories$resource_stock)

register$priority <- ifelse(
  register$workflow_risk_score >= 8,
  "high",
  ifelse(register$workflow_risk_score >= 6, "medium", "low")
)

summary_data$review_class <- ifelse(
  summary_data$minimum_stock < 10,
  "threshold risk review",
  "routine workflow review"
)

write.csv(
  register,
  file.path(tables_dir, "r_workflow_review_queue.csv"),
  row.names = FALSE
)

write.csv(
  summary_data,
  file.path(tables_dir, "r_resource_model_review_summary.csv"),
  row.names = FALSE
)

if (file.exists(output_index_path)) {
  output_index <- read.csv(output_index_path, stringsAsFactors = FALSE)
  output_index$review_flag <- ifelse(output_index$exists == "True" | output_index$exists == TRUE, "present", "missing")
  write.csv(
    output_index,
    file.path(tables_dir, "r_output_index_review.csv"),
    row.names = FALSE
  )
}

png(file.path(figures_dir, "r_resource_model_trajectories.png"), width = 1100, height = 720)

scenarios <- unique(trajectories$scenario)

if (nrow(trajectories) > 0 && all(is.finite(trajectories$resource_stock))) {
  plot(
    range(trajectories$step),
    range(trajectories$resource_stock),
    type = "n",
    xlab = "Step",
    ylab = "Resource stock",
    main = "Workflow-Generated Resource Model Trajectories"
  )

  for (scenario in scenarios) {
    subset_data <- trajectories[trajectories$scenario == scenario, ]
    lines(subset_data$step, subset_data$resource_stock)
  }

  legend("topright", legend = scenarios, lty = 1, bty = "n")
  grid()
} else {
  plot.new()
  title(main = "Workflow-Generated Resource Model Trajectories")
  text(0.5, 0.5, "No finite trajectory values available.")
}

dev.off()

print(summary_data)
print(register)
