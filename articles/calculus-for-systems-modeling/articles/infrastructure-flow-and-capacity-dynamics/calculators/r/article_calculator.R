args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <utilization|delay> ...")
cmd <- args[[1]]
out_dir <- "outputs"
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default

if (cmd == "utilization") {
  arrival <- as.numeric(get_arg(2, "95"))
  capacity <- as.numeric(get_arg(3, "100"))
  u <- arrival / capacity
  out <- data.frame(
    calculator = cmd,
    arrival = arrival,
    capacity = capacity,
    utilization = u,
    over_capacity = u > 1,
    warning = "Peak and average demand should be documented separately."
  )
} else if (cmd == "delay") {
  u <- as.numeric(get_arg(2, "0.95"))
  delay <- ifelse(u >= 1, Inf, 1 * (1 + 0.8 * (u / (1 - u))))
  out <- data.frame(
    calculator = cmd,
    utilization = u,
    delay = delay,
    warning = "Delay functions are model assumptions and should be calibrated."
  )
} else {
  stop(paste("Unknown command:", cmd))
}

write.csv(out, file.path(out_dir, paste0("r_", cmd, ".csv")), row.names = FALSE)
print(out)
