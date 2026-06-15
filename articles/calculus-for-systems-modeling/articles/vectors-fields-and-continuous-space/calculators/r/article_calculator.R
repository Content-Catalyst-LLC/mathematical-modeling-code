args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <vector-magnitude|scalar-field|vector-field> ...")
cmd <- args[[1]]
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default
write_result <- function(name, df) { write.csv(df, file.path(out_dir, paste0(name, ".csv")), row.names = FALSE); print(df) }

scalar_field <- function(x, y) 20 + 2 * sin(x) + 0.5 * y^2
vector_field <- function(x, y) c(vx = -y, vy = x)
vector_magnitude <- function(vx, vy) sqrt(vx^2 + vy^2)

if (cmd == "vector-magnitude") {
  vx <- as.numeric(get_arg(2, "3")); vy <- as.numeric(get_arg(3, "4"))
  write_result("r_vector_magnitude", data.frame(calculator=cmd, vx=vx, vy=vy, magnitude=vector_magnitude(vx, vy)))
} else if (cmd == "scalar-field") {
  x <- as.numeric(get_arg(2, "1")); y <- as.numeric(get_arg(3, "2"))
  write_result("r_scalar_field", data.frame(calculator=cmd, x=x, y=y, scalar_value=scalar_field(x, y)))
} else if (cmd == "vector-field") {
  x <- as.numeric(get_arg(2, "1")); y <- as.numeric(get_arg(3, "2"))
  v <- vector_field(x, y)
  write_result("r_vector_field", data.frame(calculator=cmd, x=x, y=y, vx=v[["vx"]], vy=v[["vy"]], magnitude=vector_magnitude(v[["vx"]], v[["vy"]])))
} else {
  stop(paste("Unknown command:", cmd))
}
