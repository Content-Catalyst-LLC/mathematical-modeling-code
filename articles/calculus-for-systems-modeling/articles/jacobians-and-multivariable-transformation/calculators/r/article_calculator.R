args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <jacobian|determinant|local-linear> ...")
cmd <- args[[1]]
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default
write_result <- function(name, df) { write.csv(df, file.path(out_dir, paste0(name, ".csv")), row.names = FALSE); print(df) }

F_model <- function(x, y) c(x^2 + y, x * y + 3 * y)
jacobian <- function(x, y) matrix(c(2*x, y, 1, x+3), nrow=2, byrow=FALSE)

if (cmd == "jacobian") {
  x <- as.numeric(get_arg(2, "2")); y <- as.numeric(get_arg(3, "1"))
  J <- jacobian(x,y)
  write_result("r_jacobian", data.frame(calculator=cmd, x=x, y=y, j11=J[1,1], j12=J[1,2], j21=J[2,1], j22=J[2,2]))
} else if (cmd == "determinant") {
  x <- as.numeric(get_arg(2, "2")); y <- as.numeric(get_arg(3, "1"))
  J <- jacobian(x,y)
  write_result("r_determinant", data.frame(calculator=cmd, x=x, y=y, determinant=det(J), absolute_determinant=abs(det(J))))
} else if (cmd == "local-linear") {
  x <- as.numeric(get_arg(2, "2")); y <- as.numeric(get_arg(3, "1"))
  dx <- as.numeric(get_arg(4, "0.1")); dy <- as.numeric(get_arg(5, "-0.05"))
  J <- jacobian(x,y)
  baseline <- F_model(x,y)
  actual <- F_model(x+dx,y+dy)
  approximate <- J %*% c(dx,dy)
  actual_change <- actual - baseline
  write_result("r_local_linear", data.frame(calculator=cmd, x=x, y=y, dx=dx, dy=dy, approximate_change_1=approximate[1], approximate_change_2=approximate[2], actual_change_1=actual_change[1], actual_change_2=actual_change[2], error_norm=sqrt(sum((actual_change-approximate)^2))))
} else {
  stop(paste("Unknown command:", cmd))
}
