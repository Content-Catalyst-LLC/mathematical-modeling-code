# Scientific Computing for Systems Modeling:
# Workflow assumption risk scoring in R.
# Educational example only.

library(tidyverse)

assumptions <- read_csv("../data/workflow_assumptions.csv", show_col_types = FALSE)

scored <- assumptions |>
  mutate(
    risk_score = (1 - confidence) * impact_if_wrong,
    priority = case_when(
      risk_score >= 0.30 ~ "High",
      risk_score >= 0.18 ~ "Medium",
      TRUE ~ "Lower"
    )
  ) |>
  arrange(desc(risk_score))

dir.create("../outputs", showWarnings = FALSE, recursive = TRUE)

write_csv(scored, "../outputs/r_workflow_assumption_risk.csv")

print(scored)
