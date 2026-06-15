.headers on
.mode column

SELECT 'JACOBIAN ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM jacobian_assumption_registry
ORDER BY assumption_key;

SELECT 'JACOBIAN CASES' AS section;
SELECT x, y, dx, dy, j11, j12, j21, j22, determinant, error_norm, warning
FROM jacobian_cases
ORDER BY x, y, dx, dy;
