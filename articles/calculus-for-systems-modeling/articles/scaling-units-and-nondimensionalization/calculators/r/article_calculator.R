args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <scale-value|logistic-nondimensional> ...")
cmd <- args[[1]]
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default
write_result <- function(name, df) { write.csv(df, file.path(out_dir, paste0(name, ".csv")), row.names = FALSE); print(df) }

if (cmd == "scale-value") {
  value <- as.numeric(get_arg(2, "40"))
  scale <- as.numeric(get_arg(3, "100"))
  dimensionless <- value / scale
  write_result("r_scale_value", data.frame(calculator=cmd, value=value, scale=scale, dimensionless_value=dimensionless, warning="Changing the reference scale changes dimensionless interpretation."))
} else if (cmd == "logistic-nondimensional") {
  stock <- as.numeric(get_arg(2, "40"))
  capacity <- as.numeric(get_arg(3, "100"))
  time <- as.numeric(get_arg(4, "20"))
  growth_rate <- as.numeric(get_arg(5, "0.35"))
  write_result("r_logistic_nondimensional", data.frame(calculator=cmd, scaled_stock=stock/capacity, scaled_time=growth_rate*time, warning="Dimensionless form still depends on documented scale choices."))
} else {
  stop(paste("Unknown command:", cmd))
}
