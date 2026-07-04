.headers on
.mode column

SELECT 'NUMERICAL STABILITY GOVERNANCE REGISTRY' AS section;
SELECT assumption_name, mathematical_role, computational_role, review_warning
FROM numerical_stability_governance_registry
ORDER BY assumption_key;

SELECT 'STABILITY CONDITIONING AUDIT CASES' AS section;
SELECT model_name, matrix_case, matrix_shape, determinant, condition_number_proxy, solution_norm, residual_norm, relative_residual, perturbation_size, perturbed_solution_change, stability_status, warning
FROM stability_conditioning_audit_cases
ORDER BY matrix_case;
