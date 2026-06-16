args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <coexistence|type-ii-response> ...")
cmd <- args[[1]]
out_dir <- "outputs"
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default

if (cmd == "coexistence") {
  alpha <- as.numeric(get_arg(2, "0.6"))
  beta <- as.numeric(get_arg(3, "0.02"))
  gamma <- as.numeric(get_arg(4, "0.5"))
  delta <- as.numeric(get_arg(5, "0.01"))
  out <- data.frame(
    calculator = cmd,
    x_star = gamma / delta,
    y_star = alpha / beta,
    warning = "Equilibrium is a mathematical condition, not a full ecological conclusion."
  )
} else if (cmd == "type-ii-response") {
  x <- as.numeric(get_arg(2, "50"))
  a <- as.numeric(get_arg(3, "0.04"))
  h <- as.numeric(get_arg(4, "0.08"))
  out <- data.frame(
    calculator = cmd,
    x = x,
    a = a,
    h = h,
    functional_response = (a * x) / (1 + a * h * x),
    warning = "Functional response choice can change stability and persistence conclusions."
  )
} else {
  stop(paste("Unknown command:", cmd))
}

write.csv(out, file.path(out_dir, paste0("r_", cmd, ".csv")), row.names = FALSE)
print(out)
