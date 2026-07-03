.headers on
.mode column

SELECT 'OPTIMIZATION GOVERNANCE REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM optimization_governance_registry
ORDER BY assumption_key;

SELECT 'OPTIMIZATION MATRIX AUDIT CASES' AS section;
SELECT model_name, observations, features, objective, solver, regularization_strength, feature_matrix_condition_number, hessian_condition_number, gradient_norm_final, objective_initial, objective_final, closed_form_gap_norm, training_rmse, warning
FROM optimization_matrix_audit_cases
ORDER BY model_name;
