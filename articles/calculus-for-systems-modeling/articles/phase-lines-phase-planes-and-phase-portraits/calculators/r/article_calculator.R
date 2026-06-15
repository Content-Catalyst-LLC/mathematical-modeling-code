args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <predator-prey-vector|phase-speed|coexistence-equilibrium> ...")
cmd <- args[[1]]
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default
write_result <- function(name, df) { write.csv(df, file.path(out_dir, paste0(name, ".csv")), row.names = FALSE); print(df) }

if (cmd == "predator-prey-vector") {
  x <- as.numeric(get_arg(2, "40")); y <- as.numeric(get_arg(3, "9"))
  alpha <- as.numeric(get_arg(4, "0.7")); beta <- as.numeric(get_arg(5, "0.05")); delta <- as.numeric(get_arg(6, "0.02")); gamma <- as.numeric(get_arg(7, "0.5"))
  dxdt <- alpha*x - beta*x*y
  dydt <- delta*x*y - gamma*y
  write_result("r_predator_prey_vector", data.frame(calculator=cmd, x=x, y=y, dxdt=dxdt, dydt=dydt, speed=sqrt(dxdt^2 + dydt^2)))
} else if (cmd == "phase-speed") {
  dxdt <- as.numeric(get_arg(2, "3")); dydt <- as.numeric(get_arg(3, "4"))
  write_result("r_phase_speed", data.frame(calculator=cmd, dxdt=dxdt, dydt=dydt, speed=sqrt(dxdt^2 + dydt^2)))
} else if (cmd == "coexistence-equilibrium") {
  alpha <- as.numeric(get_arg(2, "0.7")); beta <- as.numeric(get_arg(3, "0.05")); delta <- as.numeric(get_arg(4, "0.02")); gamma <- as.numeric(get_arg(5, "0.5"))
  write_result("r_coexistence_equilibrium", data.frame(calculator=cmd, coexistence_x=gamma/delta, coexistence_y=alpha/beta))
} else {
  stop(paste("Unknown command:", cmd))
}
