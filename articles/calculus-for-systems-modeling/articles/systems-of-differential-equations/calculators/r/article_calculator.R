args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <predator-prey-rates|coexistence-equilibrium> ...")
cmd <- args[[1]]
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default
write_result <- function(name, df) { write.csv(df, file.path(out_dir, paste0(name, ".csv")), row.names = FALSE); print(df) }

if (cmd == "predator-prey-rates") {
  prey <- as.numeric(get_arg(2, "40")); predator <- as.numeric(get_arg(3, "9"))
  alpha <- as.numeric(get_arg(4, "0.7")); beta <- as.numeric(get_arg(5, "0.05")); delta <- as.numeric(get_arg(6, "0.02")); gamma <- as.numeric(get_arg(7, "0.5"))
  prey_rate <- alpha*prey - beta*prey*predator
  predator_rate <- delta*prey*predator - gamma*predator
  write_result("r_predator_prey_rates", data.frame(calculator=cmd, prey=prey, predator=predator, prey_rate=prey_rate, predator_rate=predator_rate))
} else if (cmd == "coexistence-equilibrium") {
  alpha <- as.numeric(get_arg(2, "0.7")); beta <- as.numeric(get_arg(3, "0.05")); delta <- as.numeric(get_arg(4, "0.02")); gamma <- as.numeric(get_arg(5, "0.5"))
  write_result("r_coexistence_equilibrium", data.frame(calculator=cmd, coexistence_prey=gamma/delta, coexistence_predator=alpha/beta))
} else {
  stop(paste("Unknown command:", cmd))
}
