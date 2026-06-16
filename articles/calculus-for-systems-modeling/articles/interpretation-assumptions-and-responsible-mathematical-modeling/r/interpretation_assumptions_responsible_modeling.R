assumption_records <- data.frame(
  assumption_name = c(
    "continuous_growth",
    "fixed_parameter_values",
    "solver_configuration",
    "objective_function_weights"
  ),
  assumption_type = c(
    "mathematical",
    "empirical",
    "computational",
    "normative"
  ),
  description = c(
    "state changes continuously over modeled time",
    "parameters remain fixed across the scenario",
    "numerical method and tolerance are adequate for the model",
    "optimization weights reflect a chosen priority structure"
  ),
  risk_if_hidden = c(
    "smooth model may hide shocks, thresholds, or discrete events",
    "output appears more certain than parameter evidence supports",
    "numerical artifact may appear as model insight",
    "value judgments are hidden inside mathematics"
  )
)

claim_records <- data.frame(
  claim_type = c("descriptive", "mechanistic", "predictive", "decision_support"),
  permitted_claim = c(
    "summarizes a specified structure or dataset",
    "represents a plausible process under stated assumptions",
    "forecasts within validated domain and time horizon",
    "frames tradeoffs under documented assumptions"
  ),
  prohibited_claim = c(
    "proves a mechanism",
    "proves causality solely by formal structure",
    "predicts outside validation scope",
    "replaces judgment or accountability"
  ),
  governance_status = c("active", "review", "review", "review")
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(assumption_records, "outputs/tables/r_assumption_records.csv", row.names = FALSE)
write.csv(claim_records, "outputs/tables/r_claim_boundary_records.csv", row.names = FALSE)

print(assumption_records)
print(claim_records)
