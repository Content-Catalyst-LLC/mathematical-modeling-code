.headers on
.mode column

SELECT 'REPRESENTATION GOVERNANCE REGISTRY' AS section;
SELECT assumption_name, modeling_role, representation_role, review_warning
FROM representation_governance_registry
ORDER BY assumption_key;

SELECT 'REPRESENTATION ASSUMPTION AUDIT CASES' AS section;
SELECT workflow_name, matrix_shape, row_meaning, column_meaning, value_meaning, zero_meaning, missing_value_rule, raw_column_norm_1, raw_column_norm_2, standardized_column_norm_1, standardized_column_norm_2, warning
FROM representation_assumption_audit_cases
ORDER BY workflow_name;
