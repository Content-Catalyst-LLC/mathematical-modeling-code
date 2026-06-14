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

direction_path <- file.path(tables_dir, "future_modeling_direction_register.csv")
if (!file.exists(direction_path)) stop("Missing future modeling outputs. Run make python first.")

directions <- read.csv(direction_path, stringsAsFactors = FALSE)
num_cols <- c("future_priority_score","complexity_relevance","technical_maturity","governance_need","uncertainty_pressure","human_judgment_need")
for (col in num_cols) directions[[col]] <- as.numeric(directions[[col]])
as_bool <- function(x) { x == TRUE | x == "True" | x == "true" | x == "1" }

directions <- directions[order(-directions$future_priority_score), ]
summary_table <- data.frame(
  highest_priority_direction = directions$direction_name[1],
  mean_future_priority_score = mean(directions$future_priority_score),
  max_future_priority_score = max(directions$future_priority_score),
  governance_plan_count = sum(as_bool(directions$requires_governance_plan)),
  uncertainty_brief_count = sum(as_bool(directions$requires_uncertainty_brief)),
  human_judgment_protocol_count = sum(as_bool(directions$requires_human_judgment_protocol)),
  direction_count = nrow(directions)
)

write.csv(directions, file.path(tables_dir, "r_future_modeling_priority_ranking.csv"), row.names = FALSE)
write.csv(summary_table, file.path(tables_dir, "r_future_modeling_summary.csv"), row.names = FALSE)

png(file.path(figures_dir, "r_future_modeling_priority_scores.png"), width = 1100, height = 750)
barplot(directions$future_priority_score, names.arg = directions$key, las = 2, ylab = "Future priority score", main = "Future Modeling Direction Priority Scores")
dev.off()

print(summary_table)
print(directions)
