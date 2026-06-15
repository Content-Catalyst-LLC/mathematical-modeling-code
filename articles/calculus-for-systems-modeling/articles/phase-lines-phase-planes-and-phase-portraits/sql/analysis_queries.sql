.headers on
.mode column

SELECT 'PHASE SPACE ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM phase_space_assumption_registry
ORDER BY assumption_key;

SELECT 'PHASE PORTRAIT AUDIT CASES' AS section;
SELECT scenario, alpha, beta, delta, gamma, x_min, x_max, y_min, y_max, grid_step_x, grid_step_y, warning
FROM phase_portrait_audit_cases
ORDER BY scenario;
