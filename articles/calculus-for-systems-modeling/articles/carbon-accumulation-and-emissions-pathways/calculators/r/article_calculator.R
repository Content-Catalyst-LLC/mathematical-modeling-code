args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <cumulative-linear|budget-check> ...")
cmd <- args[[1]]
out_dir <- "outputs"
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default

if (cmd == "cumulative-linear") {
  e0 <- as.numeric(get_arg(2, "40"))
  years <- as.integer(get_arg(3, "30"))
  pathway <- pmax(0, e0 * (1 - seq(0, years) / years))
  out <- data.frame(
    calculator = cmd,
    e0 = e0,
    years = years,
    cumulative_emissions = sum(pathway),
    final_emissions = tail(pathway, 1),
    warning = "Linear decline still accumulates emissions until net zero."
  )
} else if (cmd == "budget-check") {
  cumulative <- as.numeric(get_arg(2, "600"))
  budget <- as.numeric(get_arg(3, "500"))
  out <- data.frame(
    calculator = cmd,
    cumulative = cumulative,
    budget = budget,
    exceeds_budget = cumulative > budget,
    overshoot_amount = max(0, cumulative - budget),
    warning = "Carbon budgets are conditional estimates, not exact guarantees."
  )
} else {
  stop(paste("Unknown command:", cmd))
}

write.csv(out, file.path(out_dir, paste0("r_", cmd, ".csv")), row.names = FALSE)
print(out)
