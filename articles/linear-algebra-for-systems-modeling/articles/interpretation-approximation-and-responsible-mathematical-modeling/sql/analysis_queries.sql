.headers on
.mode column

SELECT 'RESPONSIBLE MODELING GOVERNANCE REGISTRY' AS section;
SELECT governance_name, modeling_role, review_requirement, responsible_use_warning
FROM responsible_modeling_governance_registry
ORDER BY governance_key;

SELECT 'RESPONSIBLE MODELING AUDIT CASES' AS section;
SELECT workflow_name, model_purpose, claim_type, approximation_form, validation_status, interpretation_boundary, governance_warning, responsible_use_statement
FROM responsible_modeling_audit_cases
ORDER BY workflow_name;
