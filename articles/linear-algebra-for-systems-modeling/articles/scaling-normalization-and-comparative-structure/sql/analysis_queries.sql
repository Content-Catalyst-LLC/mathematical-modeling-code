.headers on
.mode column

SELECT 'SCALING GOVERNANCE REGISTRY' AS section;
SELECT assumption_name, modeling_role, transformation_role, review_warning
FROM scaling_governance_registry
ORDER BY assumption_key;

SELECT 'SCALING NORMALIZATION AUDIT CASES' AS section;
SELECT workflow_name, matrix_shape, row_meaning, column_meaning, raw_column_norm_1, raw_column_norm_2, standardized_column_norm_1, standardized_column_norm_2, first_row_sum_after_row_normalization, first_row_norm_after_unit_normalization, raw_condition_proxy, standardized_condition_proxy, warning
FROM scaling_normalization_audit_cases
ORDER BY workflow_name;
