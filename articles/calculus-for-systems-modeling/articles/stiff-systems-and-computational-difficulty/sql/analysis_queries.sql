.headers on
.mode column

SELECT 'STIFFNESS REVIEW REGISTRY' AS section;
SELECT stiffness_name, numerical_role, systems_modeling_role, review_warning
FROM stiffness_review_registry
ORDER BY stiffness_key;

SELECT 'STIFFNESS AUDIT CASES' AS section;
SELECT case_id, step_size, eigenvalue, method, diagnostic_type, interpretation_warning
FROM stiffness_audit_cases
ORDER BY method, step_size DESC;
