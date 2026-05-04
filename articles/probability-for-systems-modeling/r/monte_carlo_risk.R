# Probability for Systems Modeling:
# Monte Carlo risk simulation in R.
# Educational example only.

library(tidyverse)

set.seed(42)

parameters <- read_csv("../data/monte_carlo_risk_parameters.csv", show_col_types = FALSE)

simulate_system_loss <- function(exposure_min, exposure_max, vulnerability_alpha, vulnerability_beta, shock_meanlog, shock_sdlog, iterations) {
  tibble(
    exposure = runif(iterations, min = exposure_min, max = exposure_max),
    vulnerability = rbeta(iterations, shape1 = vulnerability_alpha, shape2 = vulnerability_beta),
    shock_intensity = rlnorm(iterations, meanlog = shock_meanlog, sdlog = shock_sdlog)
  ) |>
    mutate(
      system_loss = exposure * vulnerability * shock_intensity
    )
}

simulation_results <- parameters |>
  mutate(
    simulation = pmap(
      list(exposure_min, exposure_max, vulnerability_alpha, vulnerability_beta, shock_meanlog, shock_sdlog, iterations),
      simulate_system_loss
    )
  ) |>
  select(scenario_id, simulation) |>
  unnest(simulation)

summary_results <- simulation_results |>
  group_by(scenario_id) |>
  summarise(
    expected_loss = mean(system_loss),
    median_loss = median(system_loss),
    loss_sd = sd(system_loss),
    p90_loss = quantile(system_loss, 0.90),
    p95_loss = quantile(system_loss, 0.95),
    p99_loss = quantile(system_loss, 0.99),
    probability_loss_gt_0_50 = mean(system_loss > 0.50),
    .groups = "drop"
  )

dir.create("../outputs", showWarnings = FALSE, recursive = TRUE)

write_csv(simulation_results, "../outputs/r_monte_carlo_risk_results.csv")
write_csv(summary_results, "../outputs/r_monte_carlo_risk_summary.csv")

print(summary_results)
