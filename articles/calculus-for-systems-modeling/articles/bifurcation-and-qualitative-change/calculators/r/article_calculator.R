args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <saddle-node-equilibria|transcritical-equilibria|pitchfork-equilibria|classify-derivative> ...")
cmd <- args[[1]]
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default
write_result <- function(name, df) { write.csv(df, file.path(out_dir, paste0(name, ".csv")), row.names = FALSE); print(df) }

classify <- function(d, tolerance = 1e-8) {
  if (d < -tolerance) return("locally_stable")
  if (d > tolerance) return("locally_unstable")
  "inconclusive_at_critical_value"
}

if (cmd == "saddle-node-equilibria") {
  mu <- as.numeric(get_arg(2, "4"))
  eqs <- if (mu < 0) numeric(0) else if (abs(mu) < 1e-12) c(0) else c(-sqrt(mu), sqrt(mu))
  write_result("r_saddle_node_equilibria", data.frame(calculator=cmd, mu=mu, equilibrium=if(length(eqs)==0) NA else eqs))
} else if (cmd == "transcritical-equilibria") {
  mu <- as.numeric(get_arg(2, "2"))
  write_result("r_transcritical_equilibria", data.frame(calculator=cmd, mu=mu, equilibrium=c(0, mu)))
} else if (cmd == "pitchfork-equilibria") {
  mu <- as.numeric(get_arg(2, "4"))
  eqs <- if (mu < 0) c(0) else if (abs(mu) < 1e-12) c(0) else c(0, -sqrt(mu), sqrt(mu))
  write_result("r_pitchfork_equilibria", data.frame(calculator=cmd, mu=mu, equilibrium=eqs))
} else if (cmd == "classify-derivative") {
  d <- as.numeric(get_arg(2, "-2"))
  write_result("r_classify_derivative", data.frame(calculator=cmd, derivative_value=d, stability=classify(d)))
} else {
  stop(paste("Unknown command:", cmd))
}
