args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <regeneration|extraction> ...")
cmd <- args[[1]]
out_dir <- "outputs"
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default

if (cmd == "regeneration") {
  stock <- as.numeric(get_arg(2, "80"))
  growth_rate <- as.numeric(get_arg(3, "0.08"))
  carrying_capacity <- as.numeric(get_arg(4, "100"))
  value <- growth_rate * stock * (1 - stock / carrying_capacity)
  out <- data.frame(calculator = cmd, stock = stock, growth_rate = growth_rate, carrying_capacity = carrying_capacity, regeneration = value, warning = "Regeneration may vary with habitat climate age structure and system state.")
} else if (cmd == "extraction") {
  efficiency <- as.numeric(get_arg(2, "0.003"))
  effort <- as.numeric(get_arg(3, "12"))
  stock <- as.numeric(get_arg(4, "80"))
  value <- efficiency * effort * stock
  out <- data.frame(calculator = cmd, efficiency = efficiency, effort = effort, stock = stock, extraction = value, warning = "Extraction assumptions should include technology livelihoods markets and constraints.")
} else {
  stop(paste("Unknown command:", cmd))
}

write.csv(out, file.path(out_dir, paste0("r_", cmd, ".csv")), row.names = FALSE)
print(out)
