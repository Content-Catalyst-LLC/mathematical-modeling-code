.headers on
.mode column

SELECT 'DIVERGENCE THEOREM ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM divergence_theorem_assumption_registry
ORDER BY assumption_key;

SELECT 'DIVERGENCE THEOREM AUDIT CASES' AS section;
SELECT scenario, grid_steps, boundary_flux, volume_divergence_integral, absolute_gap, normal_note, warning
FROM divergence_theorem_audit_cases
ORDER BY grid_steps;
