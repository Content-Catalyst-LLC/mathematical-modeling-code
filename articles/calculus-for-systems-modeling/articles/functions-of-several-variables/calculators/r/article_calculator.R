args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <evaluate|feasible|grid> ...")
cmd <- args[[1]]
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default
write_result <- function(name, df) { write.csv(df, file.path(out_dir, paste0(name, ".csv")), row.names = FALSE); print(df) }
system_response <- function(x, y) 3.0 * x + 2.0 * y + 0.5 * x * y
is_feasible <- function(x, y, budget = 10) x >= 0 & y >= 0 & x + y <= budget

if (cmd == "evaluate") {
  x <- as.numeric(get_arg(2, "4")); y <- as.numeric(get_arg(3, "3")); budget <- as.numeric(get_arg(4, "10"))
  feasible <- is_feasible(x, y, budget)
  write_result("r_evaluate", data.frame(calculator="evaluate", x=x, y=y, budget=budget, output=system_response(x,y), feasible=feasible, warning=ifelse(feasible,"","Input combination is outside the feasible region.")))
} else if (cmd == "feasible") {
  x <- as.numeric(get_arg(2, "8")); y <- as.numeric(get_arg(3, "4")); budget <- as.numeric(get_arg(4, "10"))
  feasible <- is_feasible(x, y, budget)
  write_result("r_feasible", data.frame(calculator="feasible", x=x, y=y, budget=budget, feasible=feasible, remaining_budget=budget-x-y, warning=ifelse(feasible,"","Input combination violates constraints.")))
} else if (cmd == "grid") {
  max_x <- as.numeric(get_arg(2, "10")); max_y <- as.numeric(get_arg(3, "10")); step <- as.numeric(get_arg(4, "2"))
  grid <- expand.grid(x=seq(0,max_x,by=step), y=seq(0,max_y,by=step))
  grid$output <- system_response(grid$x, grid$y)
  grid$feasible <- is_feasible(grid$x, grid$y)
  grid$warning <- ifelse(grid$feasible, "", "Input combination is outside the feasible region.")
  write_result("r_multivariable_grid", grid)
} else {
  stop(paste("Unknown command:", cmd))
}
