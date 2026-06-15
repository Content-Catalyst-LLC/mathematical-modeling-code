args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <classify-derivative|logistic-stability|bistable-stability> ...")
cmd <- args[[1]]
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default
write_result <- function(name, df) { write.csv(df, file.path(out_dir, paste0(name, ".csv")), row.names = FALSE); print(df) }

classify <- function(d, tolerance = 1e-8) {
  if (d < -tolerance) return("locally_stable")
  if (d > tolerance) return("locally_unstable")
  "inconclusive_by_linearization"
}

bistable_rate <- function(x, threshold) x * (1 - x) * (x - threshold)
num_deriv <- function(x, threshold, h = 1e-5) (bistable_rate(x+h, threshold)-bistable_rate(x-h, threshold))/(2*h)

if (cmd == "classify-derivative") {
  d <- as.numeric(get_arg(2, "-0.6"))
  write_result("r_classify_derivative", data.frame(calculator=cmd, derivative_value=d, stability=classify(d)))
} else if (cmd == "logistic-stability") {
  eq <- as.numeric(get_arg(2, "100")); growth <- as.numeric(get_arg(3, "0.6")); carrying <- as.numeric(get_arg(4, "100"))
  d <- growth * (1 - 2*eq/carrying)
  write_result("r_logistic_stability", data.frame(calculator=cmd, equilibrium=eq, derivative_value=d, stability=classify(d)))
} else if (cmd == "bistable-stability") {
  eq <- as.numeric(get_arg(2, "0.4")); threshold <- as.numeric(get_arg(3, "0.4"))
  d <- num_deriv(eq, threshold)
  write_result("r_bistable_stability", data.frame(calculator=cmd, equilibrium=eq, threshold=threshold, derivative_value=d, stability=classify(d)))
} else {
  stop(paste("Unknown command:", cmd))
}
