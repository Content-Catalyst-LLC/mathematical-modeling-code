# Base R workflow for scenario comparison and modeling-process review.

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

timeseries_path <- file.path(tables_dir, "reservoir_scenario_timeseries.csv")
assumption_path <- file.path(tables_dir, "assumption_log.csv")

if (!file.exists(timeseries_path)) {
  stop("Missing reservoir_scenario_timeseries.csv. Run make python first.")
}

data <- read.csv(timeseries_path, stringsAsFactors = FALSE)

scenario_review <- aggregate(
  cbind(storage, shortage) ~ scenario,
  data = data,
  FUN = function(x) c(mean = mean(x), min = min(x), max = max(x), final = tail(x, 1))
)

scenario_review <- do.call(data.frame, scenario_review)
names(scenario_review) <- c(
  "scenario",
  "mean_storage",
  "min_storage",
  "max_storage",
  "final_storage",
  "mean_shortage",
  "min_shortage",
  "max_shortage",
  "final_shortage"
)

shortage_periods <- aggregate(shortage ~ scenario, data = data, FUN = function(x) sum(x > 0))
names(shortage_periods) <- c("scenario", "shortage_periods")

scenario_review <- merge(scenario_review, shortage_periods, by = "scenario")
scenario_review$review_status <- ifelse(
  scenario_review$shortage_periods > 0,
  "requires review",
  "acceptable under stated assumptions"
)

write.csv(
  scenario_review,
  file.path(tables_dir, "r_modeling_process_review.csv"),
  row.names = FALSE
)

if (file.exists(assumption_path)) {
  assumptions <- read.csv(assumption_path, stringsAsFactors = FALSE)
  write.csv(
    assumptions[, c("key", "statement", "risk_if_false", "sensitivity_test", "review_status")],
    file.path(tables_dir, "r_assumption_review.csv"),
    row.names = FALSE
  )
}

png(file.path(figures_dir, "r_reservoir_storage_scenarios.png"), width = 1200, height = 720)
plot(
  NA,
  xlim = range(data$period),
  ylim = range(data$storage),
  xlab = "Period",
  ylab = "Storage",
  main = "Reservoir Storage Across Modeling Scenarios"
)

for (scenario_name in unique(data$scenario)) {
  subset_data <- data[data$scenario == scenario_name, ]
  lines(subset_data$period, subset_data$storage, lwd = 2)
}

legend("bottomright", legend = unique(data$scenario), lwd = 2, cex = 0.75, bty = "n")
grid()
dev.off()

print(scenario_review)
