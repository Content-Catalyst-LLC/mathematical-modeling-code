.headers on
.mode column

SELECT 'LINEAR MODEL GOVERNANCE REGISTRY' AS section;
SELECT assumption_name, modeling_role, distortion_risk, review_warning
FROM linear_model_governance_registry
ORDER BY assumption_key;

SELECT 'LINEARITY DISTORTION AUDIT CASES' AS section;
SELECT workflow_name, model_purpose, fitted_intercept, fitted_slope, residual_sum_squares, max_absolute_residual, residual_sign_pattern, curvature_warning, extrapolation_warning, interpretation_warning
FROM linearity_distortion_audit_cases
ORDER BY workflow_name;
