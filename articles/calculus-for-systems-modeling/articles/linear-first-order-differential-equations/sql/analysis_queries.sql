.headers on
.mode column

SELECT 'LINEAR FIRST-ORDER ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM linear_first_order_assumption_registry
ORDER BY assumption_key;

SELECT 'LINEAR FIRST-ORDER AUDIT CASES' AS section;
SELECT scenario, initial_state, input_rate, loss_rate, equilibrium, time_step, steps, method, warning
FROM linear_first_order_audit_cases
ORDER BY scenario;
