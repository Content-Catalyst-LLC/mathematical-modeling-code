args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <logistic-derivative|logistic-equilibria|capacity-limit>")
cmd <- args[[1]]
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)
write_result <- function(name, df) { write.csv(df, file.path(out_dir, paste0(name, ".csv")), row.names = FALSE); print(df) }

if (cmd == "logistic-derivative") {
  write_result("r_logistic_derivative", data.frame(calculator=cmd, rate_expression="r*x*(1 - x/K)", first_derivative="r - 2*r*x/K", second_derivative="-2*r/K", warning="Derivative signs depend on parameter regimes and domains."))
} else if (cmd == "logistic-equilibria") {
  write_result("r_logistic_equilibria", data.frame(calculator=cmd, equilibria="x = 0 or x = K", warning="Equilibria require domain and stability review."))
} else if (cmd == "capacity-limit") {
  write_result("r_capacity_limit", data.frame(calculator=cmd, limit_as_x_approaches_K="0", warning="Boundary behavior should be checked against modeled assumptions."))
} else {
  stop(paste("Unknown command:", cmd))
}
