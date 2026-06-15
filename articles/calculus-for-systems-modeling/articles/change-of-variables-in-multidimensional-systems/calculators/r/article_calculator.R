args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <polar-jacobian|circular-area|linear-det> ...")
cmd <- args[[1]]
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default
write_result <- function(name, df) { write.csv(df, file.path(out_dir, paste0(name, ".csv")), row.names = FALSE); print(df) }

if (cmd == "polar-jacobian") {
  r <- as.numeric(get_arg(2, "3"))
  write_result("r_polar_jacobian", data.frame(calculator=cmd, radius=r, jacobian_factor=r))
} else if (cmd == "circular-area") {
  r <- as.numeric(get_arg(2, "3"))
  write_result("r_circular_area", data.frame(calculator=cmd, radius=r, area=pi*r^2))
} else if (cmd == "linear-det") {
  a <- as.numeric(get_arg(2, "2")); b <- as.numeric(get_arg(3, "1")); c <- as.numeric(get_arg(4, "0")); d <- as.numeric(get_arg(5, "3"))
  detv <- a*d - b*c
  write_result("r_linear_det", data.frame(calculator=cmd, a=a, b=b, c=c, d=d, determinant=detv, absolute_measure_factor=abs(detv)))
} else {
  stop(paste("Unknown command:", cmd))
}
