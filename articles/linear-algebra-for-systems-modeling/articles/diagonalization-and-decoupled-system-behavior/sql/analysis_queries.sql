.headers on
.mode column

SELECT 'DIAGONALIZATION ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM diagonalization_assumption_registry
ORDER BY assumption_key;

SELECT 'DIAGONALIZATION AUDIT CASES' AS section;
SELECT system_name, reconstruction_error_frobenius, spectral_radius, dominant_eigenvalue, stability_classification, warning
FROM diagonalization_audit_cases
ORDER BY system_name;
