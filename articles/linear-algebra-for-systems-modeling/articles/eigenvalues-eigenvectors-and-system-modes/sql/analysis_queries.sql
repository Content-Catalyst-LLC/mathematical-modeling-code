.headers on
.mode column

SELECT 'EIGENSTRUCTURE ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM eigenstructure_assumption_registry
ORDER BY assumption_key;

SELECT 'EIGENSTRUCTURE AUDIT CASES' AS section;
SELECT system_name, eigenvalue_1, eigenvalue_2, spectral_radius, dominant_eigenvalue, stability_classification, warning
FROM eigenstructure_audit_cases
ORDER BY system_name;
