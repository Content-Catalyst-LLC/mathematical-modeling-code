.headers on
.mode column

SELECT 'MACHINE LEARNING GOVERNANCE REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM machine_learning_governance_registry
ORDER BY assumption_key;

SELECT 'ML LINEAR ALGEBRA AUDIT CASES' AS section;
SELECT model_name, observations, features, method, preprocessing, regularization_strength, feature_matrix_condition_number, gram_matrix_condition_number, numerical_rank, ridge_weight_norm, training_rmse, maximum_absolute_residual, first_two_component_energy, warning
FROM ml_linear_algebra_audit_cases
ORDER BY model_name;
