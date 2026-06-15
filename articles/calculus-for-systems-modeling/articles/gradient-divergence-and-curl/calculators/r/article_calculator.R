args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <scalar-field|gradient|curl-2d> ...")
cmd <- args[[1]]
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default
write_result <- function(name, df) { write.csv(df, file.path(out_dir, paste0(name, ".csv")), row.names = FALSE); print(df) }

scalar_field <- function(x, y) x^2 + y^2
gradient_field <- function(x, y) c(2*x, 2*y)
curl_2d <- function(x, y) 2

if (cmd == "scalar-field") {
  x <- as.numeric(get_arg(2, "1")); y <- as.numeric(get_arg(3, "1"))
  write_result("r_scalar_field", data.frame(calculator=cmd, x=x, y=y, value=scalar_field(x,y)))
} else if (cmd == "gradient") {
  x <- as.numeric(get_arg(2, "1")); y <- as.numeric(get_arg(3, "1"))
  g <- gradient_field(x,y)
  write_result("r_gradient", data.frame(calculator=cmd, x=x, y=y, df_dx=g[1], df_dy=g[2]))
} else if (cmd == "curl-2d") {
  x <- as.numeric(get_arg(2, "1")); y <- as.numeric(get_arg(3, "1"))
  write_result("r_curl_2d", data.frame(calculator=cmd, x=x, y=y, curl_2d=curl_2d(x,y)))
} else {
  stop(paste("Unknown command:", cmd))
}
