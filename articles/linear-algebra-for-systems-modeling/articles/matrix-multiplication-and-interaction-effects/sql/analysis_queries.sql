.headers on
.mode column
SELECT 'MATRIX PRODUCT ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning FROM matrix_product_assumption_registry ORDER BY assumption_key;
SELECT 'MATRIX PRODUCT INTERACTION AUDIT CASES' AS section;
SELECT system_name, left_shape, right_shape, product_shape, product_matrix, reverse_product_available, warning FROM matrix_product_interaction_audit_cases ORDER BY system_name;
