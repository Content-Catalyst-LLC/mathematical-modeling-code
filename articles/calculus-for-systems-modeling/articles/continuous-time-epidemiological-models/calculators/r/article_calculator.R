args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <r0|doubling-time> ...")
cmd <- args[[1]]
out_dir <- "outputs"
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default

if (cmd == "r0") {
  beta <- as.numeric(get_arg(2, "0.32"))
  gamma <- as.numeric(get_arg(3, "0.10"))
  value <- beta / gamma
  out <- data.frame(
    calculator = cmd,
    beta = beta,
    gamma = gamma,
    r0 = value,
    warning = "R0 depends on model structure population and context."
  )
} else if (cmd == "doubling-time") {
  growth_rate <- as.numeric(get_arg(2, "0.22"))
  value <- ifelse(growth_rate <= 0, Inf, log(2) / growth_rate)
  out <- data.frame(
    calculator = cmd,
    growth_rate = growth_rate,
    doubling_time = value,
    warning = "Doubling time is only valid under the assumed growth-rate window."
  )
} else {
  stop(paste("Unknown command:", cmd))
}

write.csv(out, file.path(out_dir, paste0("r_", cmd, ".csv")), row.names = FALSE)
print(out)
