args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <position|speed|distance> ...")
cmd <- args[[1]]
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default
write_result <- function(name, df) { write.csv(df, file.path(out_dir, paste0(name, ".csv")), row.names = FALSE); print(df) }

position <- function(t) c(x=t, y=sin(t))
velocity <- function(t) c(vx=1, vy=cos(t))
distance_between <- function(x1,y1,x2,y2) sqrt((x2-x1)^2 + (y2-y1)^2)

if (cmd == "position") {
  t <- as.numeric(get_arg(2, "1"))
  p <- position(t)
  write_result("r_position", data.frame(calculator=cmd, t=t, x=p[["x"]], y=p[["y"]]))
} else if (cmd == "speed") {
  t <- as.numeric(get_arg(2, "1"))
  v <- velocity(t)
  write_result("r_speed", data.frame(calculator=cmd, t=t, speed=sqrt(v[["vx"]]^2 + v[["vy"]]^2)))
} else if (cmd == "distance") {
  x1 <- as.numeric(get_arg(2, "0")); y1 <- as.numeric(get_arg(3, "0")); x2 <- as.numeric(get_arg(4, "3")); y2 <- as.numeric(get_arg(5, "4"))
  write_result("r_distance", data.frame(calculator=cmd, x1=x1, y1=y1, x2=x2, y2=y2, distance=distance_between(x1,y1,x2,y2)))
} else {
  stop(paste("Unknown command:", cmd))
}
