args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <solve|multiplier|stationarity> ...")
cmd <- args[[1]]
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default
write_result <- function(name, df) { write.csv(df, file.path(out_dir, paste0(name, ".csv")), row.names = FALSE); print(df) }

objective <- function(x, y) x^2 + 2*y^2
solve_budget <- function(target) {
  y <- target / 3
  x <- 2 * target / 3
  lambda_value <- 2*x
  c(x=x, y=y, lambda_value=lambda_value)
}

if (cmd == "solve" || cmd == "multiplier") {
  target <- as.numeric(get_arg(2, "12"))
  s <- solve_budget(target)
  write_result(paste0("r_", cmd), data.frame(calculator=cmd, target=target, x=s[["x"]], y=s[["y"]], lambda_value=s[["lambda_value"]], objective_value=objective(s[["x"]], s[["y"]])))
} else if (cmd == "stationarity") {
  target <- as.numeric(get_arg(2, "12"))
  s <- solve_budget(target)
  x <- s[["x"]]; y <- s[["y"]]; lambda_value <- s[["lambda_value"]]
  gf <- c(2*x, 4*y)
  gg <- c(1, 1)
  residual <- gf - lambda_value * gg
  write_result("r_stationarity", data.frame(calculator=cmd, target=target, x=x, y=y, lambda_value=lambda_value, stationarity_residual_norm=sqrt(sum(residual^2))))
} else {
  stop(paste("Unknown command:", cmd))
}
