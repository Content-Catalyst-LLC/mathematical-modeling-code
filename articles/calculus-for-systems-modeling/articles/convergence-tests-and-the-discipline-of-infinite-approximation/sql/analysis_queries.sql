.headers on
.mode column

SELECT 'CONVERGENCE TEST ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM convergence_test_assumption_registry
ORDER BY assumption_key;

SELECT 'CONVERGENCE TEST AUDIT RECORDS' AS section;
SELECT series_name, test_used, n_terms, partial_sum, last_term, test_result, estimated_error, stopping_rule, warning
FROM convergence_test_audit_records
ORDER BY series_name;
