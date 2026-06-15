args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <path-point|segment-length|scalar-field> ...")
cmd <- args[[1]]
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default
write_result <- function(name, df) { write.csv(df, file.path(out_dir, paste0(name, ".csv")), row.names = FALSE); print(df) }

path_point <- function(t) c(x=t, y=sin(t))
scalar_field <- function(x, y) 1 + y^2
distance_between <- function(x1,y1,x2,y2) sqrt((x2-x1)^2 + (y2-y1)^2)

if (cmd == "path-point") {
  t <- as.numeric(get_arg(2, "1"))
  p <- path_point(t)
  write_result("r_path_point", data.frame(calculator=cmd, t=t, x=p[["x"]], y=p[["y"]]))
} else if (cmd == "segment-length") {
  x1 <- as.numeric(get_arg(2, "0")); y1 <- as.numeric(get_arg(3, "0")); x2 <- as.numeric(get_arg(4, "3")); y2 <- as.numeric(get_arg(5, "4"))
  write_result("r_segment_length", data.frame(calculator=cmd, x1=x1, y1=y1, x2=x2, y2=y2, segment_length=distance_between(x1,y1,x2,y2)))
} else if (cmd == "scalar-field") {
  x <- as.numeric(get_arg(2, "1")); y <- as.numeric(get_arg(3, "2"))
  write_result("r_scalar_field", data.frame(calculator=cmd, x=x, y=y, scalar_value=scalar_field(x,y)))
} else {
  stop(paste("Unknown command:", cmd))
}
