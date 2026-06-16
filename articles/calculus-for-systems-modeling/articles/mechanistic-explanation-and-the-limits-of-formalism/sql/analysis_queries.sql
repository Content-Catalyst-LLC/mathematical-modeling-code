.headers on
.mode column

SELECT 'EXPLANATION GOVERNANCE REGISTRY' AS section;
SELECT registry_name, analytical_role, systems_modeling_role, review_warning
FROM explanation_governance_registry
ORDER BY registry_key;

SELECT 'MECHANISM RECORDS' AS section;
SELECT mechanism_name, represented_process, evidence_status, claim_type, warning
FROM mechanism_records
ORDER BY mechanism_name;
