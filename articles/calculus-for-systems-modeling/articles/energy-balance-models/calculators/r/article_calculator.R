args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <equilibrium-temperature|adjustment-time> ...")
cmd <- args[[1]]
out_dir <- "outputs"
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default
if (cmd == "equilibrium-temperature") {
  forcing <- as.numeric(get_arg(2, "3.7"))
  feedback <- as.numeric(get_arg(3, "1.2"))
  out <- data.frame(calculator = cmd, forcing = forcing, feedback = feedback, equilibrium_temperature = forcing / feedback, warning = "Feedback terms can hide multiple physical processes.")
} else if (cmd == "adjustment-time") {
  heat_capacity <- as.numeric(get_arg(2, "10"))
  feedback <- as.numeric(get_arg(3, "1.2"))
  out <- data.frame(calculator = cmd, heat_capacity = heat_capacity, feedback = feedback, adjustment_time = heat_capacity / feedback, warning = "Equilibrium should not be confused with immediate response.")
} else { stop(paste("Unknown command:", cmd)) }
write.csv(out, file.path(out_dir, paste0("r_", cmd, ".csv")), row.names = FALSE)
print(out)
