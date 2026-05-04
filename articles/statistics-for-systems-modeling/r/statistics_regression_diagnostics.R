# Statistics for Systems Modeling:
# Estimation, uncertainty, and diagnostics in R.
# Educational example only.

library(tidyverse)

set.seed(42)

n <- 250

systems_data <- tibble(
  exposure = runif(n, 0, 100),
  capacity = runif(n, 20, 120),
  governance_quality = runif(n, 0, 1),
  noise = rnorm(n, mean = 0, sd = 8)
) |>
  mutate(
    system_burden =
      35 +
      0.42 * exposure -
      0.28 * capacity -
      14 * governance_quality +
      noise
  )

model <- lm(system_burden ~ exposure + capacity + governance_quality, data = systems_data)

intervals <- confint(model) |>
  as.data.frame() |>
  rownames_to_column("term") |>
  rename(
    lower_95 = `2.5 %`,
    upper_95 = `97.5 %`
  )

diagnostics <- tibble(
  fitted = fitted(model),
  residual = resid(model)
)

diagnostic_summary <- diagnostics |>
  summarise(
    residual_mean = mean(residual),
    residual_sd = sd(residual),
    rmse = sqrt(mean(residual^2))
  )

dir.create("../outputs", showWarnings = FALSE, recursive = TRUE)

write_csv(systems_data, "../outputs/r_statistics_systems_data.csv")
write_csv(intervals, "../outputs/r_regression_confidence_intervals.csv")
write_csv(diagnostics, "../outputs/r_regression_residuals.csv")
write_csv(diagnostic_summary, "../outputs/r_regression_diagnostic_summary.csv")

print(summary(model))
print(intervals)
print(diagnostic_summary)
