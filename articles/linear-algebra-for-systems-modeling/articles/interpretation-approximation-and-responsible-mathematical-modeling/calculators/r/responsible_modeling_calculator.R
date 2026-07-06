result <- data.frame(
  calculator = "interpretation_approximation_and_responsible_mathematical_modeling_calculator",
  workflow_name = "responsible_modeling_audit",
  model_purpose = "interpret_linear_algebra_output_for_systems_modeling",
  claim_type = "exploratory_decision_support_not_causal_proof",
  approximation_form = "linear_or_low_rank_approximation_with_explicit_assumptions",
  validation_status = "validated_only_for_stated_data_range_operating_context_and_model_purpose",
  interpretation_boundary = "Outputs support structured interpretation within the stated assumptions, not universal claims, causal proof, or unreviewed decision authority.",
  warning = "Model use requires documented assumptions, validation evidence, review status, uncertainty communication, and stop-use conditions."
)

dir.create("outputs", recursive = TRUE, showWarnings = FALSE)
write.csv(result, "outputs/r_interpretation_approximation_and_responsible_mathematical_modeling_calculator.csv", row.names = FALSE)
print(result)
