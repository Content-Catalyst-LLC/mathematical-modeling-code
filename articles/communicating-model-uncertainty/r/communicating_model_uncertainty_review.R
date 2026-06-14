# Base R workflow for uncertainty communication review.

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

queue_path <- file.path(tables_dir, "communication_review_queue.csv")
messages_path <- file.path(tables_dir, "uncertainty_messages.csv")

if (!file.exists(queue_path) || !file.exists(messages_path)) {
  stop("Missing communication outputs. Run make python first.")
}

queue <- read.csv(queue_path, stringsAsFactors = FALSE)
messages <- read.csv(messages_path, stringsAsFactors = FALSE)

queue$communication_priority <- as.numeric(queue$communication_priority)
queue <- queue[order(-queue$communication_priority), ]

audience_summary <- aggregate(
  communication_priority ~ audience,
  data = queue,
  FUN = mean
)

names(audience_summary)[2] <- "mean_communication_priority"

write.csv(
  queue,
  file.path(tables_dir, "r_communication_review_queue.csv"),
  row.names = FALSE
)

write.csv(
  messages,
  file.path(tables_dir, "r_uncertainty_message_review.csv"),
  row.names = FALSE
)

write.csv(
  audience_summary,
  file.path(tables_dir, "r_audience_summary.csv"),
  row.names = FALSE
)

png(file.path(figures_dir, "r_communication_priority_by_audience.png"), width = 1000, height = 700)

barplot(
  audience_summary$mean_communication_priority,
  names.arg = audience_summary$audience,
  las = 2,
  ylab = "Mean communication priority",
  main = "Uncertainty Communication Priority by Audience"
)

dev.off()

print(queue)
print(messages)
print(audience_summary)
