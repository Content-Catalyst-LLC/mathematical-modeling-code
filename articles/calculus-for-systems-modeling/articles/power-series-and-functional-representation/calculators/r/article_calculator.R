args <- commandArgs(trailingOnly = TRUE)

if (length(args) < 1) {
  stop("Usage: Rscript article_calculator.R <power-series|taylor-exp|logistic> ...")
}

cmd <- args[[1]]
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)

get_arg <- function(i, default) {
  if (length(args) >= i && nzchar(args[[i]])) {
    return(args[[i]])
  }
  default
}

write_result <- function(name, df) {
  write.csv(df, file.path(out_dir, paste0(name, ".csv")), row.names = FALSE)
  print(df)
}

if (cmd == "power-series") {
  x <- as.numeric(get_arg(2, "0.75"))
  n_terms <- as.integer(get_arg(3, "20"))
  n <- 0:(n_terms - 1)
  terms <- x^n
  partial <- sum(terms)
  converges <- abs(x) < 1
  reference <- ifelse(converges, 1 / (1 - x), NA)
  df <- data.frame(
    calculator = "power-series",
    x = x,
    terms = n_terms,
    partial_sum = partial,
    last_term = tail(terms, 1),
    inside_radius = converges,
    reference_value = reference,
    absolute_error = ifelse(is.na(reference), NA, abs(reference - partial))
  )
  write_result("r_power_series", df)
} else if (cmd == "taylor-exp") {
  x <- as.numeric(get_arg(2, "1"))
  n_terms <- as.integer(get_arg(3, "12"))
  n <- 0:(n_terms - 1)
  partial <- sum((x^n) / factorial(n))
  df <- data.frame(
    calculator = "taylor-exp",
    x = x,
    terms = n_terms,
    partial_sum = partial,
    reference_value = exp(x),
    absolute_error = abs(exp(x) - partial)
  )
  write_result("r_taylor_exp", df)
} else if (cmd == "logistic") {
  initial <- as.numeric(get_arg(2, "10"))
  carrying_capacity <- as.numeric(get_arg(3, "100"))
  rate <- as.numeric(get_arg(4, "0.25"))
  steps <- as.integer(get_arg(5, "20"))
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
