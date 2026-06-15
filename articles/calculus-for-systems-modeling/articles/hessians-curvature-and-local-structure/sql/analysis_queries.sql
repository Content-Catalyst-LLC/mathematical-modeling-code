.headers on
.mode column

SELECT 'HESSIAN ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM hessian_assumption_registry
ORDER BY assumption_key;

SELECT 'HESSIAN CASES' AS section;
SELECT x, y, dx, dy, h11, h12, h21, h22, determinant, classification, second_order_error, warning
FROM hessian_cases
ORDER BY x, y, dx, dy;
