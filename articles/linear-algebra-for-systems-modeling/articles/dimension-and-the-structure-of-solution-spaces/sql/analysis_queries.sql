.headers on
.mode column

SELECT 'SOLUTION SPACE ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM solution_space_assumption_registry
ORDER BY assumption_key;

SELECT 'SOLUTION SPACE AUDIT CASES' AS section;
SELECT system_name, variable_count, equation_count, rank_value, nullity_value, likely_solution_structure, warning
FROM solution_space_audit_cases
ORDER BY system_name;
