rate_function <- function(t) 2 + sin(t) + 0.1 * t
true_integral <- function(t) 2 * t - cos(t) + 1 + 0.05 * t ^ 2
times <- seq(0, 10, by = 0.1)
rates <- rate_function(times)
left_total <- 0
trap_total <- 0
rows <- list()
for (i in seq_along(times)) {
  if (i > 1) {
    left_total <- left_total + rates[[i - 1]] * 0.1
    trap_total <- trap_total + 0.5 * (rates[[i - 1]] + rates[[i]]) * 0.1
  }
  true_total <- true_integral(times[[i]]) - true_integral(0)
  rows[[length(rows) + 1]] <- data.frame(index=i-1,time=times[[i]],rate=rates[[i]],left_cumulative=left_total,trapezoid_cumulative=trap_total,true_cumulative=true_total,trapezoid_absolute_error=abs(trap_total-true_total),step_size=0.1)
}
results <- do.call(rbind, rows)
dir.create("outputs/tables", recursive=TRUE, showWarnings=FALSE)
write.csv(results, "outputs/tables/r_numerical_integration_audit.csv", row.names=FALSE)
print(head(results))
