DROP TABLE IF EXISTS responsible_modeling_governance_registry;
DROP TABLE IF EXISTS responsible_modeling_audit_cases;

CREATE TABLE responsible_modeling_governance_registry (
    governance_key TEXT PRIMARY KEY,
    governance_name TEXT NOT NULL,
    modeling_role TEXT NOT NULL,
    review_requirement TEXT NOT NULL,
    responsible_use_warning TEXT NOT NULL
);

INSERT INTO responsible_modeling_governance_registry VALUES
('model_purpose','Model purpose','Defines why the model exists and what decision or interpretation it supports.','State whether the model is exploratory predictive explanatory diagnostic optimization-oriented or governance-supporting.','A model built for exploration should not be used as final decision authority without further validation.'),
('claim_type','Claim type','Distinguishes descriptive predictive explanatory causal and decision-support claims.','Match claim strength to evidence strength.','Do not communicate stronger claims than the model can support.'),
('approximation_boundary','Approximation boundary','Defines what the model preserves and what it simplifies.','Document linearity low-rank aggregation scaling or state-space approximation choices.','Approximation is useful only when its losses are visible.'),
('uncertainty_sources','Uncertainty sources','Separates data model numerical sampling and interpretive uncertainty.','Report uncertainty sources alongside outputs.','A precise number can still be uncertain if assumptions or data are fragile.'),
('validation_status','Validation status','Records where the model has been checked and where it has not.','Preserve validation evidence reference cases residual diagnostics and operating ranges.','Validation in one context does not automatically transfer to another.'),
('sensitivity_review','Sensitivity review','Tests whether conclusions depend on data assumptions scaling representation or model form.','Compare reasonable alternative workflows when conclusions matter.','Fragile conclusions should be communicated with caution.'),
('interpretation_boundary','Interpretation boundary','Defines what outputs can and cannot responsibly mean.','Attach interpretation limits to generated reports and decision-support artifacts.','Do not let computational output exceed the model evidence.'),
('accountability_path','Accountability path','Defines who reviews maintains challenges updates and retires the model.','Assign ownership review status revision procedures and stop-use conditions.','A model without accountability should not silently guide consequential decisions.');

CREATE TABLE responsible_modeling_audit_cases (
    workflow_name TEXT NOT NULL,
    model_purpose TEXT NOT NULL,
    claim_type TEXT NOT NULL,
    approximation_form TEXT NOT NULL,
    representation_status TEXT NOT NULL,
    numerical_status TEXT NOT NULL,
    diagnostic_status TEXT NOT NULL,
    validation_status TEXT NOT NULL,
    uncertainty_sources TEXT NOT NULL,
    sensitivity_status TEXT NOT NULL,
    interpretation_boundary TEXT NOT NULL,
    governance_warning TEXT NOT NULL,
    responsible_use_statement TEXT NOT NULL
);

INSERT INTO responsible_modeling_audit_cases VALUES
('responsible_modeling_audit','interpret_linear_algebra_output_for_systems_modeling','exploratory_decision_support_not_causal_proof','linear_or_low_rank_approximation_with_explicit_assumptions','rows_columns_units_zeros_scaling_and_boundaries_documented','residuals_conditioning_solver_tolerance_and_reproducibility_checked','residuals_sensitivity_and_alternative_representations_reviewed','validated_only_for_stated_data_range_operating_context_and_model_purpose','data_uncertainty;model_uncertainty;numerical_uncertainty;interpretive_uncertainty','conclusions_compared_across_reasonable_representation_scaling_and_model_form_variants','Outputs support structured interpretation within the stated assumptions not universal claims causal proof or unreviewed decision authority.','Model use requires documented assumptions validation evidence review status uncertainty communication and stop-use conditions.','Use the model as an interpretive and diagnostic aid not as the sole basis for high-stakes decisions without domain review uncertainty disclosure and accountability.');
