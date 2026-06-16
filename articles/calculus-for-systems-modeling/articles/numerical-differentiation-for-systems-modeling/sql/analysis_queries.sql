.headers on
.mode column

SELECT 'NUMERICAL DIFFERENTIATION ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM numerical_differentiation_assumption_registry
ORDER BY assumption_key;

SELECT 'NUMERICAL DIFFERENTIATION AUDIT CASES' AS section;
SELECT scenario, start_value, stop_value, step_size, formula_family, warning
FROM numerical_differentiation_audit_cases
ORDER BY scenario;
