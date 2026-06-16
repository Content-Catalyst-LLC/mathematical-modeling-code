args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <artifact-count|clean-run-status> ...")
cmd <- args[[1]]
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default
write_result <- function(name, df) { write.csv(df, file.path(out_dir, paste0(name, ".csv")), row.names = FALSE); print(df) }

if (cmd == "artifact-count") {
  source <- as.integer(get_arg(2, "2"))
  generated <- as.integer(get_arg(3, "4"))
  total <- source + generated
  write_result("r_artifact_count", data.frame(calculator=cmd, source=source, generated=generated, total=total, warning="Artifact counts do not prove workflow quality."))
} else if (cmd == "clean-run-status") {
  expected <- as.integer(get_arg(2, "6"))
  found <- as.integer(get_arg(3, "6"))
  passed <- expected == found
  write_result("r_clean_run_status", data.frame(calculator=cmd, expected=expected, found=found, passed=passed, warning="A clean run does not prove mathematical validity."))
} else {
  stop(paste("Unknown command:", cmd))
}
