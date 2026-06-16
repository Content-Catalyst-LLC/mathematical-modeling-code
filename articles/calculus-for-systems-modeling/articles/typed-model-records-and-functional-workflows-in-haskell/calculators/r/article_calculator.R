args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <validate-parameter|logistic-step> ...")
cmd <- args[[1]]
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default
write_result <- function(name, df) { write.csv(df, file.path(out_dir, paste0(name, ".csv")), row.names = FALSE); print(df) }

if (cmd == "validate-parameter") {
  name <- get_arg(2, "growth_rate")
  value <- as.numeric(get_arg(3, "0.35"))
  minimum <- as.numeric(get_arg(4, "0"))
  valid <- value > minimum
  write_result("r_validate_parameter", data.frame(calculator=cmd, name=name, value=value, minimum=minimum, valid=valid, warning="Validation rules do not prove empirical correctness."))
} else if (cmd == "logistic-step") {
  stock <- as.numeric(get_arg(2, "10"))
  growth_rate <- as.numeric(get_arg(3, "0.35"))
  carrying_capacity <- as.numeric(get_arg(4, "100"))
  time_step <- as.numeric(get_arg(5, "0.25"))
  dx <- growth_rate * stock * (1 - stock / carrying_capacity)
  next_stock <- stock + time_step * dx
  write_result("r_logistic_step", data.frame(calculator=cmd, stock=stock, next_stock=next_stock, warning="Pure transformations can still encode poor assumptions."))
} else {
  stop(paste("Unknown command:", cmd))
}
