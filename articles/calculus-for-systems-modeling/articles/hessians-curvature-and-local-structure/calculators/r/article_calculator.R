args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <hessian|classify|second-order> ...")
cmd <- args[[1]]
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default
write_result <- function(name, df) { write.csv(df, file.path(out_dir, paste0(name, ".csv")), row.names = FALSE); print(df) }

f_model <- function(x, y) x^2 + x*y + 3*y^2 + 0.2*x^2*y
gradient <- function(x, y) c(2*x + y + 0.4*x*y, x + 6*y + 0.2*x^2)
hessian <- function(x, y) matrix(c(2 + 0.4*y, 1 + 0.4*x, 1 + 0.4*x, 6), nrow=2, byrow=TRUE)
classify_hessian <- function(H) {
  d <- det(H)
  if (d > 0 && H[1,1] > 0) return("positive definite")
  if (d > 0 && H[1,1] < 0) return("negative definite")
  if (d < 0) return("indefinite")
  "semidefinite or inconclusive"
}

if (cmd == "hessian") {
  x <- as.numeric(get_arg(2, "2")); y <- as.numeric(get_arg(3, "1"))
  H <- hessian(x,y)
  write_result("r_hessian", data.frame(calculator=cmd, x=x, y=y, h11=H[1,1], h12=H[1,2], h21=H[2,1], h22=H[2,2]))
} else if (cmd == "classify") {
  x <- as.numeric(get_arg(2, "2")); y <- as.numeric(get_arg(3, "1"))
  H <- hessian(x,y)
  write_result("r_classify", data.frame(calculator=cmd, x=x, y=y, determinant=det(H), trace=sum(diag(H)), classification=classify_hessian(H)))
} else if (cmd == "second-order") {
  x <- as.numeric(get_arg(2, "2")); y <- as.numeric(get_arg(3, "1"))
  dx <- as.numeric(get_arg(4, "0.1")); dy <- as.numeric(get_arg(5, "-0.05"))
  g <- gradient(x,y); H <- hessian(x,y)
  first <- sum(g * c(dx,dy))
  second <- first + 0.5 * as.numeric(t(c(dx,dy)) %*% H %*% c(dx,dy))
  actual <- f_model(x+dx,y+dy) - f_model(x,y)
  write_result("r_second_order", data.frame(calculator=cmd, x=x, y=y, dx=dx, dy=dy, first_order_change=first, second_order_change=second, actual_change=actual, second_order_error=abs(actual-second)))
} else {
  stop(paste("Unknown command:", cmd))
}
