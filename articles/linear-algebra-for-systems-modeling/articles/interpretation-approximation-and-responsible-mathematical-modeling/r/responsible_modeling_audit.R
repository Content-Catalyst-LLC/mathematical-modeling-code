audit_record <- data.frame(
  workflow_name = "responsible_modeling_audit",
  model_purpose = "interpret_linear_algebra_output_for_systems_modeling",
  claim_type = "exploratory_decision_support_not_causal_proof",
  approximation_form = "linear_or_low_rank_approximation_with_explicit_assumptions",
  representation_status = "rows_columns_units_zeros_scaling_and_boundaries_documented",
  numerical_status = "residuals_conditioning_solver_tolerance_and_reproducibility_checked",
  diagnostic_status = "residuals_sensitivity_and_alternative_representations_reviewed",
  validation_status = "validated_only_for_stated_data_range_operating_context_and_model_purpose",
  uncertainty_sources = paste(
    "data_uncertainty",
    "model_uncertainty",
    "numerical_uncertainty",
    "interpretive_uncertainty",
    sep = ";"
  ),
  sensitivity_status = paste(
    "conclusions_compared_across_reasonable_representation_scaling",
    "and_model_form_variants"
  ),
  interpretation_boundary = paste(
    "Outputs support structured interpretation within the stated assumptions,",
    "not universal claims, causal proof, or unreviewed decision authority."
  ),
  governance_warning = paste(
    "Model use requires documented assumptions, validation evidence, review status,",
    "uncertainty communication, and stop-use conditions."
  ),
  responsible_use_statement = paste(
    "Use the model as an interpretive and diagnostic aid.",
    "Do not use it as the sole basis for high-stakes decisions without domain review,",
    "uncertainty disclosure, and accountability."
  )
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(audit_record, "outputs/tables/r_responsible_modeling_audit.csv", row.names = FALSE)
print(audit_record)
