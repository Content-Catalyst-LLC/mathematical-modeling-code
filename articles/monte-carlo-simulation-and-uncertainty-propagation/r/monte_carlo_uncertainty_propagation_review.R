# Base R workflow for Monte Carlo uncertainty review.

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

replication_path <- file.path(tables_dir, "monte_carlo_replications.csv")
summary_path <- file.path(tables_dir, "monte_carlo_output_summary.csv")
register_path <- file.path(tables_dir, "monte_carlo_model_register.csv")

if (!file.exists(replication_path) || !file.exists(summary_path)) {
  stop("Missing Monte Carlo outputs. Run make python first.")
}

replications <- read.csv(replication_path, stringsAsFactors = FALSE)
summary_data <- read.csv(summary_path, stringsAsFactors = FALSE)

replications$final_stock <- as.numeric(replications$final_stock)
replications$depleted <- as.integer(replications$depleted)

quantile_review <- aggregate(
  final_stock ~ scenario,
  data = replications,
  FUN = function(x) {
    paste(
      round(quantile(x, probs = c(0.05, 0.5, 0.95), na.rm = TRUE), 4),
      collapse = "|"
    )
  }
)

names(quantile_review)[2] <- "p05_median_p95"

summary_data$review_class <- ifelse(
  summary_data$depletion_probability > 0.25,
  "high depletion risk",
  ifelse(summary_data$p05_final_stock < 15, "lower-tail risk review", "routine uncertainty review")
)

write.csv(
  summary_data,
  file.path(tables_dir, "r_monte_carlo_uncertainty_review_summary.csv"),
  row.names = FALSE
)

write.csv(
  quantile_review,
  file.path(tables_dir, "r_monte_carlo_quantile_review.csv"),
  row.names = FALSE
)

if (file.exists(register_path)) {
  register <- read.csv(register_path, stringsAsFactors = FALSE)

  register$priority <- ifelse(
    register$monte_carlo_risk_score >= 8,
    "high",
    ifelse(register$monte_carlo_risk_score >= 6, "medium", "low")
  )

  write.csv(
    register,
    file.path(tables_dir, "r_monte_carlo_model_review_queue.csv"),
    row.names = FALSE
  )
}

png(file.path(figures_dir, "r_monte_carlo_final_stock_boxplot.png"), width = 1100, height = 720)

if (nrow(replications) > 0 && all(is.finite(replications$final_stock))) {
  boxplot(
    final_stock ~ scenario,
    data = replications,
    las = 2,
    ylab = "Final resource stock",
    main = "Monte Carlo Final Stock Distribution"
  )
  abline(h = 10, lty = 2)
  grid()
} else {
  plot.new()
  title(main = "Monte Carlo Final Stock Distribution")
  text(0.5, 0.5, "No finite Monte Carlo values available.")
}

dev.off()

print(summary_data)
