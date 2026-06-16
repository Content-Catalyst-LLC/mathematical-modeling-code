args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <forward-difference|backward-difference|central-difference|second-central-difference|benchmark-audit> ...")
cmd <- args[[1]]
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default
write_result <- function(name, df) { write.csv(df, file.path(out_dir, paste0(name, ".csv")), row.names = FALSE); print(df) }
signal_function <- function(x) sin(x) + 0.1 * x^2
true_derivative <- function(x) cos(x) + 0.2 * x

if (cmd == "forward-difference") {
  f_current <- as.numeric(get_arg(2, "1"))
  f_next <- as.numeric(get_arg(3, "1.12"))
  h <- as.numeric(get_arg(4, "0.1"))
  write_result("r_forward_difference", data.frame(calculator=cmd, f_current=f_current, f_next=f_next, h=h, derivative_estimate=(f_next-f_current)/h))
} else if (cmd == "backward-difference") {
  f_previous <- as.numeric(get_arg(2, "0.89"))
  f_current <- as.numeric(get_arg(3, "1"))
  h <- as.numeric(get_arg(4, "0.1"))
  write_result("r_backward_difference", data.frame(calculator=cmd, f_previous=f_previous, f_current=f_current, h=h, derivative_estimate=(f_current-f_previous)/h))
} else if (cmd == "central-difference") {
  f_previous <- as.numeric(get_arg(2, "0.89"))
  f_next <- as.numeric(get_arg(3, "1.12"))
  h <- as.numeric(get_arg(4, "0.1"))
  write_result("r_central_difference", data.frame(calculator=cmd, f_previous=f_previous, f_next=f_next, h=h, derivative_estimate=(f_next-f_previous)/(2*h)))
} else if (cmd == "second-central-difference") {
  f_previous <- as.numeric(get_arg(2, "0.89"))
  f_current <- as.numeric(get_arg(3, "1"))
  f_next <- as.numeric(get_arg(4, "1.12"))
  h <- as.numeric(get_arg(5, "0.1"))
  write_result("r_second_central_difference", data.frame(calculator=cmd, f_previous=f_previous, f_current=f_current, f_next=f_next, h=h, second_derivative_estimate=(f_next - 2*f_current + f_previous)/(h^2)))
} else if (cmd == "benchmark-audit") {
  start <- as.numeric(get_arg(2, "0"))
  stop <- as.numeric(get_arg(3, "10"))
  h <- as.numeric(get_arg(4, "0.1"))
  xs <- seq(start, stop, by=h)
  values <- signal_function(xs)
  rows <- list()
  for (i in seq_along(xs)) {
    central <- NA
    err <- NA
    if (i > 1 && i < length(xs)) {
      central <- (values[[i+1]] - values[[i-1]])/(2*h)
      err <- abs(central - true_derivative(xs[[i]]))
    }
    rows[[length(rows)+1]] <- data.frame(index=i-1, x=xs[[i]], value=values[[i]], true_derivative=true_derivative(xs[[i]]), central_difference=central, central_absolute_error=err, h=h)
  }
  write_result("r_benchmark_audit", do.call(rbind, rows))
} else {
  stop(paste("Unknown command:", cmd))
}
