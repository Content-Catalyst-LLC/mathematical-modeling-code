args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <absolute-error|convergence-ratio> ...")
cmd <- args[[1]]
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default
write_result <- function(name, df) { write.csv(df, file.path(out_dir, paste0(name, ".csv")), row.names = FALSE); print(df) }

if (cmd == "absolute-error") {
  numeric <- as.numeric(get_arg(2, "0.912"))
  exact <- as.numeric(get_arg(3, "0.9119"))
  write_result("r_absolute_error", data.frame(calculator=cmd, numeric=numeric, exact=exact, absolute_error=abs(numeric - exact), warning="Small numerical error does not imply empirical validity."))
} else if (cmd == "convergence-ratio") {
  previous_error <- as.numeric(get_arg(2, "0.01"))
  current_error <- as.numeric(get_arg(3, "0.000625"))
  write_result("r_convergence_ratio", data.frame(calculator=cmd, previous_error=previous_error, current_error=current_error, error_ratio=previous_error/current_error, warning="Convergence evidence supports numerical reliability not empirical validity."))
} else {
  stop(paste("Unknown command:", cmd))
}
