.headers on
.mode column

SELECT 'STABILITY ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM stability_assumption_registry
ORDER BY assumption_key;

SELECT 'STABILITY AUDIT CASES' AS section;
SELECT scenario, equilibrium, derivative_value, stability, domain_min, domain_max, warning
FROM stability_audit_cases
ORDER BY scenario, equilibrium;
