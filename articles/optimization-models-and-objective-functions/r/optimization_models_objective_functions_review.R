# Base R workflow for objective review and scenario diagnostics.
# Patched to handle Python CSV boolean values robustly: TRUE/FALSE, True/False, 1/0.

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

choice_path <- file.path(tables_dir, "optimization_feasible_choice_audit.csv")
summary_path <- file.path(tables_dir, "optimization_solution_summary.csv")
register_path <- file.path(tables_dir, "optimization_model_register.csv")

if (!file.exists(choice_path) || !file.exists(summary_path)) {
  stop("Missing optimization outputs. Run make python first.")
}

choices <- read.csv(choice_path, stringsAsFactors = FALSE)
summary_data <- read.csv(summary_path, stringsAsFactors = FALSE)

summary_data$feasibility_review <- ifelse(
  summary_data$feasible_choices == 0,
  "infeasible scenario",
  ifelse(
    summary_data$feasible_choices < 10,
    "narrow feasible region",
    "feasible alternatives available"
  )
)

write.csv(
  summary_data,
  file.path(tables_dir, "r_optimization_solution_review_summary.csv"),
  row.names = FALSE
)

if (file.exists(register_path)) {
  register <- read.csv(register_path, stringsAsFactors = FALSE)

  register$priority <- ifelse(
    register$optimization_risk_score >= 8,
    "high",
    ifelse(register$optimization_risk_score >= 6, "medium", "low")
  )

  write.csv(
    register,
    file.path(tables_dir, "r_optimization_model_review_queue.csv"),
    row.names = FALSE
  )
}

# Robust boolean parsing for feasible flag written from Python CSV.
if (!("feasible" %in% names(choices))) {
  stop("Expected column 'feasible' not found in optimization_feasible_choice_audit.csv.")
}

if (is.logical(choices$feasible)) {
  feasible_flag <- choices$feasible
} else {
  feasible_flag <- tolower(trimws(as.character(choices$feasible))) %in% c("true", "t", "1", "yes", "y")
}

choices$total_cost <- as.numeric(choices$total_cost)
choices$total_benefit <- as.numeric(choices$total_benefit)

feasible <- choices[feasible_flag & is.finite(choices$total_cost) & is.finite(choices$total_benefit), , drop = FALSE]

png(file.path(figures_dir, "r_optimization_feasible_benefit_by_cost.png"), width = 1100, height = 720)

if (nrow(feasible) > 0) {
  plot(
    feasible$total_cost,
    feasible$total_benefit,
    xlab = "Total Cost",
    ylab = "Total Benefit",
    main = "Feasible Optimization Choices: Benefit by Cost"
  )
  grid()
} else {
  plot.new()
  title(main = "Feasible Optimization Choices: Benefit by Cost")
  text(0.5, 0.5, "No feasible choices available for plotting.")
}

dev.off()

print(summary_data)
