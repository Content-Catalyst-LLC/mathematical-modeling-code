# Mathematical Modeling: Model Assumption Risk in R
# Educational example only.

library(tidyverse)

assumptions <- read_csv("../data/model_assumptions.csv", show_col_types = FALSE)

assumptions <- assumptions |>
  mutate(
    assumption_risk_score = (1 - confidence) * impact_if_wrong,
    priority_band = case_when(
      assumption_risk_score >= 0.30 ~ "High priority",
      assumption_risk_score >= 0.18 ~ "Medium priority",
      TRUE ~ "Lower priority"
    )
  ) |>
  arrange(desc(assumption_risk_score))

dir.create("../outputs", showWarnings = FALSE, recursive = TRUE)

write_csv(assumptions, "../outputs/r_model_assumption_risk_scores.csv")

print(assumptions)
