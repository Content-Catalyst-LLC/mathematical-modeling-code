# Continuity, Discontinuity, and Structural Breaks
# Base R piecewise structural-break diagnostic workflow.

piecewise_system <- function(x) {
  ifelse(x < 5, 2.0 + 0.5 * x, 6.0 + 1.4 * (x - 5.0))
}

x <- seq(0, 10, by = 0.25)
y <- piecewise_system(x)

left_slope <- rep(NA, length(x))
right_slope <- rep(NA, length(x))
slope_change <- rep(NA, length(x))
level_jump <- rep(NA, length(x))
flag <- rep("ok", length(x))

for (i in 2:(length(x) - 1)) {
  left_slope[i] <- (y[i] - y[i - 1]) / (x[i] - x[i - 1])
  right_slope[i] <- (y[i + 1] - y[i]) / (x[i + 1] - x[i])
  slope_change[i] <- abs(right_slope[i] - left_slope[i])
  level_jump[i] <- abs(y[i] - y[i - 1])

  if (level_jump[i] > 1.0 && slope_change[i] > 0.5) {
    flag[i] <- "level_and_slope_break"
  } else if (level_jump[i] > 1.0) {
    flag[i] <- "possible_jump"
  } else if (slope_change[i] > 0.5) {
    flag[i] <- "possible_slope_break"
  }
}

results <- data.frame(
  x = x,
  y = y,
  left_slope = left_slope,
  right_slope = right_slope,
  slope_change = slope_change,
  level_jump = level_jump,
  flag = flag
)

summary <- aggregate(x ~ flag, data = results, FUN = length)
names(summary) <- c("flag", "count")

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(results, "outputs/tables/r_continuity_break_diagnostics.csv", row.names = FALSE)
write.csv(summary, "outputs/tables/r_continuity_break_summary.csv", row.names = FALSE)

print(results[results$flag != "ok", ])
