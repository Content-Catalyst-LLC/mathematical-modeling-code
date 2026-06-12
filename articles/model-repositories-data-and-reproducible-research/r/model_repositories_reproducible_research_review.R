# Base R workflow for repository audit review.

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

inventory_path <- file.path(tables_dir, "repository_artifact_inventory.csv")
register_path <- file.path(tables_dir, "repository_audit_register.csv")

if (!file.exists(inventory_path) || !file.exists(register_path)) {
  stop("Missing repository audit outputs. Run make python first.")
}

inventory <- read.csv(inventory_path, stringsAsFactors = FALSE)
register <- read.csv(register_path, stringsAsFactors = FALSE)

inventory$exists_logical <- inventory$exists == "True" | inventory$exists == TRUE
inventory$required_logical <- inventory$required == "True" | inventory$required == TRUE

inventory$review_class <- ifelse(
  inventory$required_logical & !inventory$exists_logical,
  "missing required artifact",
  ifelse(inventory$exists_logical, "present", "missing optional artifact")
)

register$priority <- ifelse(
  register$repository_risk_score >= 8,
  "high",
  ifelse(register$repository_risk_score >= 6, "medium", "low")
)

completeness_summary <- aggregate(
  exists_logical ~ required_logical,
  data = inventory,
  FUN = function(x) round(mean(x), 4)
)

names(completeness_summary) <- c("required_artifact", "presence_rate")

write.csv(
  inventory,
  file.path(tables_dir, "r_repository_artifact_review.csv"),
  row.names = FALSE
)

write.csv(
  register,
  file.path(tables_dir, "r_repository_review_queue.csv"),
  row.names = FALSE
)

write.csv(
  completeness_summary,
  file.path(tables_dir, "r_repository_completeness_summary.csv"),
  row.names = FALSE
)

png(file.path(figures_dir, "r_repository_artifact_completeness.png"), width = 1000, height = 700)

counts <- table(inventory$review_class)

barplot(
  counts,
  las = 2,
  ylab = "Artifact count",
  main = "Repository Artifact Review"
)

grid()

dev.off()

print(completeness_summary)
print(register)
