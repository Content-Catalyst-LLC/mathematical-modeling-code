.headers on
.mode column

SELECT 'SCALING GOVERNANCE REGISTRY' AS section;
SELECT registry_name, analytical_role, systems_modeling_role, review_warning
FROM scaling_governance_registry
ORDER BY registry_key;

SELECT 'SCALING UNIT RECORDS' AS section;
SELECT record_type, quantity_name, value, unit, interpretation, warning
FROM scaling_unit_records
ORDER BY record_type, quantity_name;
