.headers on
.mode column

SELECT 'SVD GOVERNANCE REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM svd_governance_registry
ORDER BY assumption_key;

SELECT 'SVD DIAGNOSTIC AUDIT CASES' AS section;
SELECT model_name, rows, columns, singular_values, numerical_rank, rank_tolerance, condition_number, retained_rank, explained_energy_retained, relative_reconstruction_error, warning
FROM svd_diagnostic_audit_cases
ORDER BY model_name;
