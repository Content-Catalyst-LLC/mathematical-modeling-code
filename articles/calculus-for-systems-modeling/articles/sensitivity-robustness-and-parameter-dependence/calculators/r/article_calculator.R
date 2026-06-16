args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <finite-difference|robustness-classification> ...")
cmd <- args[[1]]
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default
write_result <- function(name, df) { write.csv(df, file.path(out_dir, paste0(name, ".csv")), row.names = FALSE); print(df) }

if (cmd == "finite-difference") {
  low_output <- as.numeric(get_arg(2, "85.8"))
  high_output <- as.numeric(get_arg(3, "99.7"))
  lower <- as.numeric(get_arg(4, "0.2"))
  upper <- as.numeric(get_arg(5, "0.5"))
  sensitivity <- (high_output - low_output) / (upper - lower)
  write_result("r_finite_difference", data.frame(calculator=cmd, sensitivity=sensitivity, warning="Finite differences depend on the tested range."))
} else if (cmd == "robustness-classification") {
  low_output <- as.numeric(get_arg(2, "85.8"))
  high_output <- as.numeric(get_arg(3, "99.7"))
  threshold <- as.numeric(get_arg(4, "10"))
  output_range <- abs(high_output - low_output)
  status <- ifelse(output_range < threshold, "stable", "sensitive")
  write_result("r_robustness_classification", data.frame(calculator=cmd, output_range=output_range, status=status, warning="Robustness depends on the tested parameter domain."))
} else {
  stop(paste("Unknown command:", cmd))
}
