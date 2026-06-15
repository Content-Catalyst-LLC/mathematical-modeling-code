args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <linear-rate|equilibrium|analytical-solution> ...")
cmd <- args[[1]]
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default
write_result <- function(name, df) { write.csv(df, file.path(out_dir, paste0(name, ".csv")), row.names = FALSE); print(df) }

if (cmd == "linear-rate") {
  state <- as.numeric(get_arg(2, "20")); input <- as.numeric(get_arg(3, "12")); loss <- as.numeric(get_arg(4, "0.4"))
  write_result("r_linear_rate", data.frame(calculator=cmd, state=state, input_rate=input, loss_rate=loss, rate=input - loss*state))
} else if (cmd == "equilibrium") {
  input <- as.numeric(get_arg(2, "12")); loss <- as.numeric(get_arg(3, "0.4"))
  write_result("r_equilibrium", data.frame(calculator=cmd, input_rate=input, loss_rate=loss, equilibrium=input/loss))
} else if (cmd == "analytical-solution") {
  t <- as.numeric(get_arg(2, "2")); initial <- as.numeric(get_arg(3, "20")); input <- as.numeric(get_arg(4, "12")); loss <- as.numeric(get_arg(5, "0.4"))
  eq <- input/loss
  state <- eq + (initial - eq) * exp(-loss*t)
  write_result("r_analytical_solution", data.frame(calculator=cmd, time=t, initial=initial, input_rate=input, loss_rate=loss, equilibrium=eq, state=state))
} else {
  stop(paste("Unknown command:", cmd))
}
