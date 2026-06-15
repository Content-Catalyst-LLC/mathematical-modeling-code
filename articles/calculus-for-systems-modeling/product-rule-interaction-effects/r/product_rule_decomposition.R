# Product Rule and Interaction Effects
# Base R workflow for contribution decomposition

dir.create("outputs/tables", showWarnings = FALSE, recursive = TRUE)
dir.create("outputs/figures", showWarnings = FALSE, recursive = TRUE)

central_difference <- function(values, time) {
  n <- length(values)
  if (n < 3) stop("At least three points are required.")
  deriv <- numeric(n)
  deriv[1] <- (values[2] - values[1]) / (time[2] - time[1])
  deriv[n] <- (values[n] - values[n - 1]) / (time[n] - time[n - 1])
  for (i in 2:(n - 1)) {
    deriv[i] <- (values[i + 1] - values[i - 1]) / (time[i + 1] - time[i - 1])
  }
  deriv
}

time <- seq(0, 20, length.out = 401)
factor_a <- 100 + 4 * time + 8 * sin(0.4 * time)
factor_b <- 1.2 + 0.03 * time + 0.15 * cos(0.25 * time)
product_y <- factor_a * factor_b

a_prime <- central_difference(factor_a, time)
b_prime <- central_difference(factor_b, time)
direct_y_prime <- central_difference(product_y, time)

contribution_from_a <- a_prime * factor_b
contribution_from_b <- factor_a * b_prime
product_rule_y_prime <- contribution_from_a + contribution_from_b
residual <- direct_y_prime - product_rule_y_prime

results <- data.frame(
  time = time,
  factor_a = factor_a,
  factor_b = factor_b,
  product_y = product_y,
  a_prime = a_prime,
  b_prime = b_prime,
  direct_y_prime = direct_y_prime,
  contribution_from_a = contribution_from_a,
  contribution_from_b = contribution_from_b,
  product_rule_y_prime = product_rule_y_prime,
  residual = residual
)

summary_table <- data.frame(
  metric = c("max_abs_residual", "mean_abs_residual", "mean_abs_contribution_from_a", "mean_abs_contribution_from_b", "mean_direct_y_prime"),
  value = c(max(abs(residual)), mean(abs(residual)), mean(abs(contribution_from_a)), mean(abs(contribution_from_b)), mean(direct_y_prime))
)

write.csv(results, "outputs/tables/product_rule_decomposition_r.csv", row.names = FALSE)
write.csv(summary_table, "outputs/tables/product_rule_summary_r.csv", row.names = FALSE)

png("outputs/figures/product_rule_contributions_r.png", width = 1200, height = 700)
plot(time, direct_y_prime, type = "l", lwd = 2, xlab = "Time", ylab = "Derivative / contribution", main = "Product-rule decomposition")
lines(time, contribution_from_a, lwd = 2, lty = 2)
lines(time, contribution_from_b, lwd = 2, lty = 3)
legend("topleft", legend = c("direct y prime", "contribution from a", "contribution from b"), lwd = 2, lty = c(1, 2, 3), bty = "n")
grid()
dev.off()

print(head(results))
print(summary_table)
