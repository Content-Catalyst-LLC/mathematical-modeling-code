.headers on
.mode column

SELECT 'CONDITION SCOPE GOVERNANCE REGISTRY' AS section;
SELECT registry_name, analytical_role, systems_modeling_role, review_warning
FROM condition_scope_governance_registry
ORDER BY registry_key;

SELECT 'CONDITION SCOPE RECORDS' AS section;
SELECT record_type, record_name, value_or_domain, source_or_interpretation, warning
FROM condition_scope_records
ORDER BY record_type, record_name;
