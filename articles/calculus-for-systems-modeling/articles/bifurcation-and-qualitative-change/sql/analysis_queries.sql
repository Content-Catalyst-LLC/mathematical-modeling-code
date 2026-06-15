.headers on
.mode column

SELECT 'BIFURCATION ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM bifurcation_assumption_registry
ORDER BY assumption_key;

SELECT 'BIFURCATION AUDIT CASES' AS section;
SELECT model, parameter_min, parameter_max, parameter_step, normal_form, critical_value, warning
FROM bifurcation_audit_cases
ORDER BY model;
