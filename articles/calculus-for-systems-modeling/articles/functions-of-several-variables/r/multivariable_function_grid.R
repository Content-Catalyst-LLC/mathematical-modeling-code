system_response <- function(x, y) 3.0 * x + 2.0 * y + 0.5 * x * y
is_feasible <- function(x, y, budget = 10) x >= 0 & y >= 0 & x + y <= budget

grid <- expand.grid(x = seq(0, 10, by = 2), y = seq(0, 10, by = 2))
grid$output <- system_response(grid$x, grid$y)
grid$feasible <- is_feasible(grid$x, grid$y)
grid$warning <- ifelse(grid$feasible, "", "Input combination is outside the feasible region.")
dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(grid, "outputs/tables/r_multivariable_function_grid.csv", row.names = FALSE)
print(grid)
