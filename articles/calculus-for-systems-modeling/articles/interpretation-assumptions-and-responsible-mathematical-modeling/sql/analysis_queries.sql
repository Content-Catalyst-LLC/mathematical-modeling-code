.headers on
.mode column

SELECT 'RESPONSIBLE MODELING GOVERNANCE REGISTRY' AS section;
SELECT registry_name, analytical_role, systems_modeling_role, review_warning
FROM responsible_modeling_governance_registry
ORDER BY registry_key;

SELECT 'RESPONSIBLE MODELING RECORDS' AS section;
SELECT record_type, record_name, category, permitted_use, prohibited_use, warning
FROM responsible_modeling_records
ORDER BY record_type, record_name;
