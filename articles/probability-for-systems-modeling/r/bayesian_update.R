# Probability for Systems Modeling:
# Beta-binomial Bayesian updating in R.
# Educational example only.

library(tidyverse)

cases <- read_csv("../data/bayesian_update_cases.csv", show_col_types = FALSE)

updates <- cases |>
  mutate(
    posterior_alpha = prior_alpha + successes,
    posterior_beta = prior_beta + failures,
    prior_mean = prior_alpha / (prior_alpha + prior_beta),
    posterior_mean = posterior_alpha / (posterior_alpha + posterior_beta)
  )

dir.create("../outputs", showWarnings = FALSE, recursive = TRUE)

write_csv(updates, "../outputs/r_bayesian_update_results.csv")

print(updates)
