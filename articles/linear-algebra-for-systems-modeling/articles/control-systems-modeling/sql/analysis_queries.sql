.headers on
.mode column

SELECT 'CONTROL SYSTEM ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM control_system_assumption_registry
ORDER BY assumption_key;

SELECT 'CONTROL SYSTEM AUDIT CASES' AS section;
SELECT system_name, open_loop_max_real_part, closed_loop_max_real_part, controllability_rank, observability_rank, warning
FROM control_system_audit_cases
ORDER BY system_name;
