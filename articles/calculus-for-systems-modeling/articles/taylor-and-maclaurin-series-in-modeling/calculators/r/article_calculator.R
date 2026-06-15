args <- commandArgs(trailingOnly = TRUE)

if (length(args) < 1) {
  stop("Usage: Rscript article_calculator.R <taylor-exp|taylor-sin|logistic> ...")
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

taylor_exp <- function(x, order) {
  n <- 0:order
  sum((x^n) / factorial(n))
}

taylor_sin <- function(x, order) {
  n <- 0:order
  sum(((-1)^n) * (x^(2*n + 1)) / factorial(2*n + 1))
}

if (cmd == "taylor-exp") {
  x <- as.numeric(get_arg(2, "1"))
  order <- as.integer(get_arg(3, "10"))
  approx <- taylor_exp(x, order)
  df <- data.frame(
    calculator = "taylor-exp",
    x = x,
    order = order,
    approximation = approx,
    reference_value = exp(x),
    absolute_error = abs(exp(x) - approx)
  )
  write_result("r_taylor_exp", df)
} else if (cmd == "taylor-sin") {
  x <- as.numeric(get_arg(2, "1"))
  order <- as.integer(get_arg(3, "10"))
  approx <- taylor_sin(x, order)
  df <- data.frame(
    calculator = "taylor-sin",
    x = x,
    order = order,
    approximation = approx,
    reference_value = sin(x),
    absolute_error = abs(sin(x) - approx)
  )
  write_result("r_taylor_sin", df)
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
