args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <evaluate|partial-x|partial-y|cross-partial|interaction|grid> ...")
cmd <- args[[1]]
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default
write_result <- function(name, df) { write.csv(df, file.path(out_dir, paste0(name, ".csv")), row.names = FALSE); print(df) }
f <- function(x, y) 3.0 * x + 2.0 * y + 0.5 * x * y
partial_x <- function(x, y) 3.0 + 0.5 * y
partial_y <- function(x, y) 2.0 + 0.5 * x
cross_partial <- function(x, y) 0.5
is_feasible <- function(x, y, budget = 10) x >= 0 & y >= 0 & x + y <= budget

if (cmd %in% c("evaluate","partial-x","partial-y","cross-partial","interaction")) {
  x <- as.numeric(get_arg(2, "4")); y <- as.numeric(get_arg(3, "3"))
  df <- data.frame(calculator=cmd, x=x, y=y, output=f(x,y), partial_x=partial_x(x,y), partial_y=partial_y(x,y), cross_partial_xy=cross_partial(x,y), interaction_component=0.5*x*y)
  write_result(paste0("r_", gsub("-", "_", cmd)), df)
} else if (cmd == "grid") {
  max_x <- as.numeric(get_arg(2, "10")); max_y <- as.numeric(get_arg(3, "10")); step <- as.numeric(get_arg(4, "2"))
  grid <- expand.grid(x=seq(0,max_x,by=step), y=seq(0,max_y,by=step))
  grid$output <- f(grid$x, grid$y)
  grid$partial_x <- partial_x(grid$x, grid$y)
  grid$partial_y <- partial_y(grid$x, grid$y)
  grid$cross_partial_xy <- cross_partial(grid$x, grid$y)
  grid$feasible <- is_feasible(grid$x, grid$y)
  grid$warning <- ifelse(grid$feasible, "", "Input combination is outside the feasible region.")
  write_result("r_partial_derivative_grid", grid)
} else {
  stop(paste("Unknown command:", cmd))
}
