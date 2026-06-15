args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <total-differential|local-linear|approximation-error> ...")
cmd <- args[[1]]
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default
write_result <- function(name, df) { write.csv(df, file.path(out_dir, paste0(name, ".csv")), row.names = FALSE); print(df) }
f <- function(x, y) 3.0 * x + 2.0 * y + 0.5 * x * y
fx <- function(x, y) 3.0 + 0.5 * y
fy <- function(x, y) 2.0 + 0.5 * x
total_differential <- function(x, y, dx, dy) fx(x,y) * dx + fy(x,y) * dy

if (cmd %in% c("total-differential","local-linear","approximation-error")) {
  x <- as.numeric(get_arg(2, "4"))
  y <- as.numeric(get_arg(3, "3"))
  dx <- as.numeric(get_arg(4, "0.2"))
  dy <- as.numeric(get_arg(5, "-0.1"))
  baseline <- f(x,y)
  actual <- f(x+dx, y+dy)
  actual_change <- actual - baseline
  estimate <- total_differential(x,y,dx,dy)
  df <- data.frame(
    calculator = cmd,
    x = x, y = y, dx = dx, dy = dy,
    baseline_output = baseline,
    actual_output = actual,
    actual_change = actual_change,
    differential_estimate = estimate,
    local_linear_output = baseline + estimate,
    absolute_error = abs(actual_change - estimate)
  )
  write_result(paste0("r_", gsub("-", "_", cmd)), df)
} else {
  stop(paste("Unknown command:", cmd))
}
