#!/usr/bin/env Rscript
# Self-contained model calculator for article companion repositories.
# Uses base R only.
#
# Examples:
#   Rscript model_calculator.R derivative --expr "sin(x)*exp(-x)" --x 1.5
#   Rscript model_calculator.R integral --expr "x^2 + sin(x)" --a 0 --b 10 --method simpson --n 1000
#   Rscript model_calculator.R euler --ode "0.2*y*(1-y/100)" --y0 10 --dt 0.1 --steps 50
#   Rscript model_calculator.R logistic --r 0.2 --k 100 --y0 10 --dt 0.1 --steps 50
#   Rscript model_calculator.R finite-difference --values "1,1.4,2.1,3.2" --h 0.5

args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) {
  stop("Usage: Rscript model_calculator.R <command> [--key value ...]", call. = FALSE)
}
command <- args[[1]]
rest <- args[-1]

get_arg <- function(key, default = NULL, required = FALSE) {
  idx <- which(rest == paste0("--", key))
  if (length(idx) == 0) {
    if (required) stop(paste("Missing required argument --", key, sep = ""), call. = FALSE)
    return(default)
  }
  if (idx[[1]] == length(rest)) stop(paste("Missing value for --", key, sep = ""), call. = FALSE)
  rest[[idx[[1]] + 1]]
}

parse_params <- function(raw) {
  env <- new.env(parent = baseenv())
  if (!is.null(raw) && nchar(raw) > 0) {
    chunks <- strsplit(raw, ",", fixed = TRUE)[[1]]
    for (chunk in chunks) {
      if (nchar(trimws(chunk)) == 0) next
      kv <- strsplit(chunk, "=", fixed = TRUE)[[1]]
      if (length(kv) != 2) stop(paste("Invalid parameter:", chunk), call. = FALSE)
      assign(trimws(kv[[1]]), as.numeric(trimws(kv[[2]])), envir = env)
    }
  }
  env
}

eval_expr <- function(expr, env) {
  eval(parse(text = expr), envir = env)
}

write_rows <- function(df, out = NULL) {
  if (is.null(out) || nchar(out) == 0) {
    write.csv(df, stdout(), row.names = FALSE)
  } else {
    write.csv(df, out, row.names = FALSE)
  }
}

if (command == "derivative") {
  expr <- get_arg("expr", required = TRUE)
  x0 <- as.numeric(get_arg("x", required = TRUE))
  h <- as.numeric(get_arg("h", "1e-5"))
  method <- get_arg("method", "central")
  env <- parse_params(get_arg("params", ""))
  f <- function(x) { assign("x", x, envir = env); eval_expr(expr, env) }
  value <- switch(method,
                  central = (f(x0 + h) - f(x0 - h)) / (2 * h),
                  forward = (f(x0 + h) - f(x0)) / h,
                  backward = (f(x0) - f(x0 - h)) / h,
                  stop("Unknown method", call. = FALSE))
  cat(sprintf("derivative,%.12g\n", value))

} else if (command == "integral") {
  expr <- get_arg("expr", required = TRUE)
  a <- as.numeric(get_arg("a", required = TRUE))
  b <- as.numeric(get_arg("b", required = TRUE))
  n <- as.integer(get_arg("n", "1000"))
  method <- get_arg("method", "simpson")
  env <- parse_params(get_arg("params", ""))
  f <- function(x) { assign("x", x, envir = env); eval_expr(expr, env) }
  h <- (b - a) / n
  if (method == "midpoint") {
    xs <- a + (seq_len(n) - 0.5) * h
    value <- h * sum(vapply(xs, f, numeric(1)))
  } else if (method == "trapezoid") {
    xs <- seq(a, b, length.out = n + 1)
    ys <- vapply(xs, f, numeric(1))
    value <- h * (0.5 * ys[[1]] + sum(ys[2:n]) + 0.5 * ys[[n + 1]])
  } else if (method == "simpson") {
    if (n %% 2 == 1) n <- n + 1
    h <- (b - a) / n
    xs <- seq(a, b, length.out = n + 1)
    ys <- vapply(xs, f, numeric(1))
    value <- h / 3 * (ys[[1]] + ys[[n + 1]] + 4 * sum(ys[seq(2, n, by = 2)]) + 2 * sum(ys[seq(3, n - 1, by = 2)]))
  } else {
    stop("Unknown method", call. = FALSE)
  }
  cat(sprintf("integral,%.12g\n", value))

} else if (command == "euler" || command == "rk4") {
  ode <- get_arg("ode", required = TRUE)
  y <- as.numeric(get_arg("y0", required = TRUE))
  t <- as.numeric(get_arg("t0", "0"))
  dt <- as.numeric(get_arg("dt", "0.1"))
  steps <- as.integer(get_arg("steps", "50"))
  out <- get_arg("out", "")
  env <- parse_params(get_arg("params", ""))
  f <- function(t, y) { assign("t", t, envir = env); assign("x", t, envir = env); assign("y", y, envir = env); eval_expr(ode, env) }
  rows <- data.frame(step = integer(), t = numeric(), y = numeric())
  for (step in 0:steps) {
    rows <- rbind(rows, data.frame(step = step, t = t, y = y))
    if (step < steps) {
      if (command == "euler") {
        y <- y + dt * f(t, y)
      } else {
        k1 <- f(t, y)
        k2 <- f(t + dt / 2, y + dt * k1 / 2)
        k3 <- f(t + dt / 2, y + dt * k2 / 2)
        k4 <- f(t + dt, y + dt * k3)
        y <- y + dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6
      }
      t <- t + dt
    }
  }
  write_rows(rows, out)

} else if (command == "logistic") {
  r <- as.numeric(get_arg("r", required = TRUE))
  k <- as.numeric(get_arg("k", required = TRUE))
  y <- as.numeric(get_arg("y0", required = TRUE))
  t <- as.numeric(get_arg("t0", "0"))
  dt <- as.numeric(get_arg("dt", "0.1"))
  steps <- as.integer(get_arg("steps", "50"))
  out <- get_arg("out", "")
  rows <- data.frame(step = integer(), t = numeric(), y = numeric())
  f <- function(y) r * y * (1 - y / k)
  for (step in 0:steps) {
    rows <- rbind(rows, data.frame(step = step, t = t, y = y))
    if (step < steps) {
      k1 <- f(y)
      k2 <- f(y + dt * k1 / 2)
      k3 <- f(y + dt * k2 / 2)
      k4 <- f(y + dt * k3)
      y <- y + dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6
      t <- t + dt
    }
  }
  write_rows(rows, out)

} else if (command == "finite-difference") {
  values <- as.numeric(strsplit(get_arg("values", required = TRUE), ",", fixed = TRUE)[[1]])
  h <- as.numeric(get_arg("h", "1"))
  out <- get_arg("out", "")
  n <- length(values)
  rows <- data.frame(index = seq_len(n) - 1, value = values, forward_difference = NA_real_, central_difference = NA_real_)
  if (n >= 2) rows$forward_difference[1:(n - 1)] <- diff(values) / h
  if (n >= 3) rows$central_difference[2:(n - 1)] <- (values[3:n] - values[1:(n - 2)]) / (2 * h)
  write_rows(rows, out)

} else {
  stop(paste("Unknown command:", command), call. = FALSE)
}
