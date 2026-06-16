risk_records <- data.frame(
  risk_name = c(
    "false_smoothness",
    "hidden_threshold",
    "equilibrium_bias",
    "aggregation_risk",
    "solver_confidence"
  ),
  risk_pattern = c(
    "smooth curve hides structural break",
    "critical transition is omitted or smoothed",
    "steady state is overinterpreted",
    "average hides heterogeneity",
    "successful computation is mistaken for validation"
  ),
  possible_consequence = c(
    "failure or shock dynamics are missed",
    "fragility is understated",
    "transition costs and delays are hidden",
    "local stress or inequality is hidden",
    "numerical artifact appears as insight"
  ),
  governance_response = c(
    "test for breaks and document discontinuities",
    "run threshold and scenario checks",
    "analyze trajectories and stability",
    "inspect distributions and subgroups",
    "record solver method, tolerance, convergence, and warnings"
  )
)

risk_records$review_status <- c("review", "review", "review", "review", "review")

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(risk_records, "outputs/tables/r_continuous_model_risk_records.csv", row.names = FALSE)

print(risk_records)
