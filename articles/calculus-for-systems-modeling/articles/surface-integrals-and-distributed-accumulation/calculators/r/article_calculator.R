args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <height|patch-area|scalar-field> ...")
cmd <- args[[1]]
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default
write_result <- function(name, df) { write.csv(df, file.path(out_dir, paste0(name, ".csv")), row.names = FALSE); print(df) }

height <- function(x, y) 0.1*x^2 + 0.05*y^2
scalar_field <- function(x, y, z) 1 + 0.2*z
normal_area_vector <- function(x, y, step) c(-0.2*x*step*step, -0.1*y*step*step, step*step)
vector_norm <- function(v) sqrt(sum(v^2))

if (cmd == "height") {
  x <- as.numeric(get_arg(2, "1")); y <- as.numeric(get_arg(3, "1"))
  write_result("r_height", data.frame(calculator=cmd, x=x, y=y, z=height(x,y)))
} else if (cmd == "patch-area") {
  x <- as.numeric(get_arg(2, "1")); y <- as.numeric(get_arg(3, "1")); step <- as.numeric(get_arg(4, "0.25"))
  write_result("r_patch_area", data.frame(calculator=cmd, x=x, y=y, step=step, patch_area=vector_norm(normal_area_vector(x,y,step))))
} else if (cmd == "scalar-field") {
  x <- as.numeric(get_arg(2, "1")); y <- as.numeric(get_arg(3, "1"))
  z <- height(x,y)
  write_result("r_scalar_field", data.frame(calculator=cmd, x=x, y=y, z=z, scalar_value=scalar_field(x,y,z)))
} else {
  stop(paste("Unknown command:", cmd))
}
