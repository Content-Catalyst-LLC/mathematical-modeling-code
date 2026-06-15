args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) {
  stop("Usage: Rscript article_calculator.R <geometric|pseries|logistic> ...")
}

out_dir <- file.path(dirname(dirname(normalizePath(sys.frame(1)$ofile %||% "r/article_calculator.R"))), "outputs")
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)

`%||%` <- function(x, y) if (is.null(x)) y else x

write_result <- function(name, df) {
  write.csv(df, file.path(out_dir, paste0(name, ".csv")), row.names = FALSE)
  cat(paste(capture.output(print(df)), collapse = "\n"), "\n")
}

cmd <- args[[1]]

if (cmd == "geometric") {
  a <- as.numeric(args[[2]] %||% "10")
  r <- as.numeric(args[[3]] %||% "0.6")
  n_terms <- as.integer(args[[4]] %||% "25")
  n <- 0:(n_terms - 1)
  terms <- a * r^n
  partial <- sum(terms)
  reference <- ifelse(abs(r) < 1, a / (1 - r), NA)
  df <- data.frame(
    calculator = "geometric",
    a = a,
    r = r,
    terms = n_terms,
    partial_sum = partial,
    last_term = tail(terms, 1),
    converges = abs(r) < 1,
    reference_value = reference,
    estimated_tail_error = ifelse(is.na(reference), NA, reference - partial)
  )
  write_result("r_geometric", df)
} else if (cmd == "pseries") {
  p <- as.numeric(args[[2]] %||% "1.25")
  n_terms <- as.integer(args[[3]] %||% "10000")
  terms <- 1 / (seq_len(n_terms)^p)
  df <- data.frame(
    calculator = "pseries",
    p = p,
    terms = n_terms,
    partial_sum = sum(terms),
    last_term = tail(terms, 1),
    converges = p > 1
  )
  write_result("r_pseries", df)
} else if (cmd == "logistic") {
  initial <- as.numeric(args[[2]] %||% "10")
  carrying_capacity <- as.numeric(args[[3]] %||% "100")
  rate <- as.numeric(args[[4]] %||% "0.25")
  steps <- as.integer(args[[5]] %||% "20")
  x <- initial
  rows <- data.frame(step = 0, x = x)
  for (step in seq_len(steps)) {
    x <- x + rate * x * (1 - x / carrying_capacity)
    rows <- rbind(rows, data.frame(step = step, x = x))
  }
  write_result("r_logistic_trajectory", rows)
} else {
  stop(paste("Unknown command:", cmd))
}
