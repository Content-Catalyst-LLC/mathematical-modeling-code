# Base R workflow for spatial review and distance diagnostics.

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

access_path <- file.path(tables_dir, "spatial_accessibility_diagnostics.csv")
register_path <- file.path(tables_dir, "spatial_model_register.csv")

if (!file.exists(access_path)) {
  stop("Missing spatial accessibility outputs. Run make python first.")
}

access <- read.csv(access_path, stringsAsFactors = FALSE)
access$accessibility_score <- as.numeric(access$accessibility_score)
access$nearest_distance <- as.numeric(access$nearest_distance)
access$low_access_exposure_score <- as.numeric(access$low_access_exposure_score)

access$review_class <- ifelse(
  access$accessibility_score < median(access$accessibility_score, na.rm = TRUE),
  "lower access review",
  "routine review"
)

write.csv(
  access,
  file.path(tables_dir, "r_spatial_accessibility_review_summary.csv"),
  row.names = FALSE
)

if (file.exists(register_path)) {
  register <- read.csv(register_path, stringsAsFactors = FALSE)

  register$priority <- ifelse(
    register$spatial_risk_score >= 8,
    "high",
    ifelse(register$spatial_risk_score >= 6, "medium", "low")
  )

  write.csv(
    register,
    file.path(tables_dir, "r_spatial_model_review_queue.csv"),
    row.names = FALSE
  )
}

png(file.path(figures_dir, "r_spatial_accessibility_scores.png"), width = 1100, height = 720)

scores <- access$accessibility_score
names(scores) <- access$demand_location

if (length(scores) > 0 && any(is.finite(scores))) {
  barplot(
    sort(scores, decreasing = TRUE),
    las = 2,
    ylab = "Accessibility score",
    main = "Spatial Accessibility Diagnostics"
  )
  grid()
} else {
  plot.new()
  title(main = "Spatial Accessibility Diagnostics")
  text(0.5, 0.5, "No finite accessibility values available.")
}

dev.off()

print(access)
