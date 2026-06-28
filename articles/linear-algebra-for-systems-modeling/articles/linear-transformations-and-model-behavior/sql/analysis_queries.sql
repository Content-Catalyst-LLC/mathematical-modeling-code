.headers on
.mode column

SELECT 'LINEAR TRANSFORMATION ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM linear_transformation_assumption_registry
ORDER BY assumption_key;

SELECT 'LINEAR TRANSFORMATION BEHAVIOR AUDIT CASES' AS section;
SELECT system_name, row_count, column_count, rank, nullity, amplification_ratio, warning
FROM linear_transformation_behavior_audit_cases
ORDER BY system_name;
