.headers on
.mode column

SELECT 'CONVERGENCE ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM convergence_assumption_registry
ORDER BY assumption_key;

SELECT 'SERIES AUDIT RECORDS' AS section;
SELECT series_name, n_terms, last_term, partial_sum, convergence_classification, stopping_rule, warning
FROM series_audit_records
ORDER BY series_name;
