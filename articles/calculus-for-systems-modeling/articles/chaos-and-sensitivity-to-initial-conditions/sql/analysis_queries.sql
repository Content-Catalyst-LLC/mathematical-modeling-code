.headers on
.mode column

SELECT 'CHAOS ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM chaos_assumption_registry
ORDER BY assumption_key;

SELECT 'CHAOS AUDIT CASES' AS section;
SELECT model, r, x0, perturbation, steps, burn_in, sample_steps, warning
FROM chaos_audit_cases
ORDER BY model;
