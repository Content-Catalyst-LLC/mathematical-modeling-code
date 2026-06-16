args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <logistic-regeneration|msy> ...")
cmd <- args[[1]]
out_dir <- "outputs"
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default

if (cmd == "logistic-regeneration") {
  stock <- as.numeric(get_arg(2, "500"))
  r <- as.numeric(get_arg(3, "0.18"))
  k <- as.numeric(get_arg(4, "1000"))
  value <- max(0, r * stock * (1 - stock / k))
  out <- data.frame(
    calculator = cmd,
    stock = stock,
    r = r,
    k = k,
    regeneration = value,
    warning = "Logistic regeneration is a simplifying assumption and should be validated for the resource."
  )
} else if (cmd == "msy") {
  r <- as.numeric(get_arg(2, "0.18"))
  k <- as.numeric(get_arg(3, "1000"))
  value <- r * k / 4
  out <- data.frame(
    calculator = cmd,
    r = r,
    k = k,
    maximum_sustainable_yield = value,
    precautionary_yield = 0.7 * value,
    warning = "MSY is not a safe target under uncertainty by default."
  )
} else {
  stop(paste("Unknown command:", cmd))
}

write.csv(out, file.path(out_dir, paste0("r_", cmd, ".csv")), row.names = FALSE)
print(out)
