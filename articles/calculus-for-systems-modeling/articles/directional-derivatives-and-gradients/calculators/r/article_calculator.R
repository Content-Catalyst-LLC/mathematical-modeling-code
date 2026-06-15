args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <gradient|directional-derivative|estimated-change> ...")
cmd <- args[[1]]
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default
write_result <- function(name, df) { write.csv(df, file.path(out_dir, paste0(name, ".csv")), row.names = FALSE); print(df) }
f <- function(x, y) 3.0 * x + 2.0 * y + 0.5 * x * y
gradient <- function(x, y) c(3.0 + 0.5 * y, 2.0 + 0.5 * x)
normalize <- function(v) {
  norm_value <- sqrt(sum(v^2))
  if (norm_value == 0) stop("Direction vector must be nonzero.")
  v / norm_value
}

if (cmd == "gradient") {
  x <- as.numeric(get_arg(2, "4")); y <- as.numeric(get_arg(3, "3"))
  grad <- gradient(x,y)
  write_result("r_gradient", data.frame(calculator=cmd, x=x, y=y, gradient_x=grad[1], gradient_y=grad[2]))
} else if (cmd %in% c("directional-derivative","estimated-change")) {
  x <- as.numeric(get_arg(2, "4")); y <- as.numeric(get_arg(3, "3"))
  vx <- as.numeric(get_arg(4, "1")); vy <- as.numeric(get_arg(5, "1"))
  step <- as.numeric(get_arg(6, "0.25"))
  unit <- normalize(c(vx,vy)); grad <- gradient(x,y)
  derivative <- sum(grad * unit)
  actual <- f(x + step * unit[1], y + step * unit[2]) - f(x,y)
  estimated <- step * derivative
  write_result(paste0("r_", gsub("-", "_", cmd)), data.frame(calculator=cmd, x=x, y=y, direction_x=vx, direction_y=vy, unit_x=unit[1], unit_y=unit[2], gradient_x=grad[1], gradient_y=grad[2], directional_derivative=derivative, estimated_change=estimated, actual_change=actual, absolute_error=abs(actual-estimated)))
} else {
  stop(paste("Unknown command:", cmd))
}
