.headers on
.mode column

SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM convergence_test_assumption_registry
ORDER BY assumption_key;
