.headers on
.mode column

SELECT 'REPRODUCIBILITY GOVERNANCE REGISTRY' AS section;
SELECT workflow_name, computational_role, systems_modeling_role, review_warning
FROM reproducibility_governance_registry
ORDER BY workflow_key;

SELECT 'WORKFLOW OUTPUT REGISTER' AS section;
SELECT artifact_name, artifact_type, artifact_path, source_or_generated, review_role, warning
FROM workflow_output_register
ORDER BY artifact_name;
