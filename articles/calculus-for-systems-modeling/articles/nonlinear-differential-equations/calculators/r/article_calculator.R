args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <logistic-rate|logistic-equilibria|bistable-rate|bistable-equilibria> ...")
cmd <- args[[1]]
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default
write_result <- function(name, df) { write.csv(df, file.path(out_dir, paste0(name, ".csv")), row.names = FALSE); print(df) }

if (cmd == "logistic-rate") {
  x <- as.numeric(get_arg(2, "10")); growth <- as.numeric(get_arg(3, "0.6")); carrying <- as.numeric(get_arg(4, "100"))
  write_result("r_logistic_rate", data.frame(calculator=cmd, state=x, growth_rate=growth, carrying_capacity=carrying, rate=growth*x*(1-x/carrying)))
} else if (cmd == "logistic-equilibria") {
  carrying <- as.numeric(get_arg(2, "100"))
  write_result("r_logistic_equilibria", data.frame(calculator=cmd, equilibrium_zero=0, equilibrium_capacity=carrying))
} else if (cmd == "bistable-rate") {
  x <- as.numeric(get_arg(2, "0.35")); threshold <- as.numeric(get_arg(3, "0.4"))
  write_result("r_bistable_rate", data.frame(calculator=cmd, state=x, threshold=threshold, rate=x*(1-x)*(x-threshold)))
} else if (cmd == "bistable-equilibria") {
  threshold <- as.numeric(get_arg(2, "0.4"))
  write_result("r_bistable_equilibria", data.frame(calculator=cmd, equilibrium_zero=0, equilibrium_threshold=threshold, equilibrium_one=1))
} else {
  stop(paste("Unknown command:", cmd))
}
