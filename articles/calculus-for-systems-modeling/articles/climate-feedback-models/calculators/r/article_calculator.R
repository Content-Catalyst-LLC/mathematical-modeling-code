args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <co2-forcing|one-box> ...")
cmd <- args[[1]]
out_dir <- "outputs"
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default

if (cmd == "co2-forcing") {
  concentration <- as.numeric(get_arg(2, "560"))
  baseline <- as.numeric(get_arg(3, "280"))
  out <- data.frame(
    calculator = cmd,
    concentration = concentration,
    baseline = baseline,
    forcing = 5.35 * log(concentration / baseline),
    warning = "This compact approximation does not replace detailed radiative-transfer modeling."
  )
} else if (cmd == "one-box") {
  forcing <- as.numeric(get_arg(2, "3.7"))
  feedback <- as.numeric(get_arg(3, "1.2"))
  heat_capacity <- as.numeric(get_arg(4, "8"))
  time <- as.numeric(get_arg(5, "80"))
  equilibrium <- forcing / feedback
  temperature <- equilibrium * (1 - exp(-(feedback / heat_capacity) * time))
  out <- data.frame(
    calculator = cmd,
    forcing = forcing,
    feedback = feedback,
    heat_capacity = heat_capacity,
    time = time,
    temperature = temperature,
    equilibrium_temperature = equilibrium,
    warning = "One-box models clarify structure but are not complete Earth-system models."
  )
} else {
  stop(paste("Unknown command:", cmd))
}

write.csv(out, file.path(out_dir, paste0("r_", cmd, ".csv")), row.names = FALSE)
print(out)
