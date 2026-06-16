args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <continuous-future-value|continuous-present-value> ...")
cmd <- args[[1]]
out_dir <- "outputs"
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default

if (cmd == "continuous-future-value") {
  v0 <- as.numeric(get_arg(2, "1000"))
  r <- as.numeric(get_arg(3, "0.05"))
  t <- as.numeric(get_arg(4, "30"))
  value <- v0 * exp(r * t)
  out <- data.frame(
    calculator = cmd,
    v0 = v0,
    r = r,
    t = t,
    future_value = value,
    warning = "Long horizons amplify small rate differences."
  )
} else if (cmd == "continuous-present-value") {
  fv <- as.numeric(get_arg(2, "5000"))
  r <- as.numeric(get_arg(3, "0.05"))
  t <- as.numeric(get_arg(4, "30"))
  value <- fv * exp(-r * t)
  out <- data.frame(
    calculator = cmd,
    fv = fv,
    r = r,
    t = t,
    present_value = value,
    warning = "Discount-rate choices can dominate long-horizon conclusions."
  )
} else {
  stop(paste("Unknown command:", cmd))
}

write.csv(out, file.path(out_dir, paste0("r_", cmd, ".csv")), row.names = FALSE)
print(out)
