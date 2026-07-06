module Main where

data ResponsibleModelingAudit = ResponsibleModelingAudit
  { workflowName :: String
  , modelPurpose :: String
  , claimType :: String
  , approximationForm :: String
  , representationStatus :: String
  , numericalStatus :: String
  , diagnosticStatus :: String
  , validationStatus :: String
  , uncertaintySources :: String
  , sensitivityStatus :: String
  , interpretationBoundary :: String
  , governanceWarning :: String
  , responsibleUseStatement :: String
  } deriving (Show)

buildAudit :: ResponsibleModelingAudit
buildAudit =
  ResponsibleModelingAudit
    "responsible_modeling_audit"
    "interpret_linear_algebra_output_for_systems_modeling"
    "exploratory_decision_support_not_causal_proof"
    "linear_or_low_rank_approximation_with_explicit_assumptions"
    "rows_columns_units_zeros_scaling_and_boundaries_documented"
    "residuals_conditioning_solver_tolerance_and_reproducibility_checked"
    "residuals_sensitivity_and_alternative_representations_reviewed"
    "validated_only_for_stated_data_range_operating_context_and_model_purpose"
    "data_uncertainty;model_uncertainty;numerical_uncertainty;interpretive_uncertainty"
    "conclusions_compared_across_reasonable_representation_scaling_and_model_form_variants"
    "Outputs support structured interpretation within the stated assumptions, not universal claims, causal proof, or unreviewed decision authority."
    "Model use requires documented assumptions, validation evidence, review status, uncertainty communication, and stop-use conditions."
    "Use the model as an interpretive and diagnostic aid. Do not use it as the sole basis for high-stakes decisions without domain review, uncertainty disclosure, and accountability."

main :: IO ()
main =
  print buildAudit
