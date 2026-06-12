# Base R scenario diagnostics for "What Is Mathematical Modeling?"

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

scenario_path <- file.path(tables_dir, "scenario_timeseries.csv")
if (!file.exists(scenario_path)) {
  stop("Missing scenario_timeseries.csv. Run make python first.")
}

data <- read.csv(scenario_path, stringsAsFactors = FALSE)

summary_stats <- aggregate(
  state ~ scenario + method,
  data = data,
  FUN = function(x) c(final = tail(x, 1), mean = mean(x), min = min(x), max = max(x), sd = sd(x))
)

summary_stats <- do.call(data.frame, summary_stats)
names(summary_stats) <- c("scenario", "method", "final_state", "mean_state", "min_state", "max_state", "sd_state")
summary_stats$review_status <- ifelse(summary_stats$final_state < 0, "invalid", "reviewed")
write.csv(summary_stats, file.path(tables_dir, "r_scenario_diagnostics.csv"), row.names = FALSE)

png(file.path(figures_dir, "r_scenario_trajectories.png"), width = 1200, height = 720)

plot(
  NA,
  xlim = range(data$time),
  ylim = range(data$state),
  xlab = "Time",
  ylab = "State",
  main = "Mathematical Modeling Scenario Trajectories"
)

keys <- unique(paste(data$scenario, data$method, sep = " / "))
for (key in keys) {
  parts <- strsplit(key, " / ", fixed = TRUE)[[1]]
  subset_data <- data[data$scenario == parts[1] & data$method == parts[2], ]
  lines(subset_data$time, subset_data$state, lwd = 2)
}

legend("bottomright", legend = keys, lwd = 2, cex = 0.65, bty = "n")
grid()
dev.off()

print(summary_stats)
