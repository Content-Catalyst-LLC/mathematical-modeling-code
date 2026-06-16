args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <exponential-growth|doubling-time> ...")
cmd <- args[[1]]
out_dir <- "outputs"
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default

if (cmd == "exponential-growth") {
  y0 <- as.numeric(get_arg(2, "100"))
  g <- as.numeric(get_arg(3, "0.025"))
  years <- as.numeric(get_arg(4, "40"))
  final <- y0 * exp(g * years)
  out <- data.frame(
    calculator = cmd,
    y0 = y0,
    g = g,
    years = years,
    final_output = final,
    warning = "Growth-rate assumptions compound strongly over time."
  )
} else if (cmd == "doubling-time") {
  g <- as.numeric(get_arg(2, "0.025"))
  dt <- ifelse(g <= 0, Inf, log(2) / g)
  out <- data.frame(
    calculator = cmd,
    g = g,
    doubling_time = dt,
    warning = "Doubling time assumes constant proportional growth."
  )
} else {
  stop(paste("Unknown command:", cmd))
}

write.csv(out, file.path(out_dir, paste0("r_", cmd, ".csv")), row.names = FALSE)
print(out)
