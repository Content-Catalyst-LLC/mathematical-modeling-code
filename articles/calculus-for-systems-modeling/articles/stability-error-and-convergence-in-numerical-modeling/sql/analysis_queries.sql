.headers on
.mode column

SELECT 'NUMERICAL RELIABILITY REGISTRY' AS section;
SELECT reliability_name, numerical_role, systems_modeling_role, review_warning
FROM numerical_reliability_registry
ORDER BY reliability_key;

SELECT 'CONVERGENCE AUDIT CASES' AS section;
SELECT case_id, solver_method, step_size, diagnostic_type, interpretation_warning
FROM convergence_audit_cases
ORDER BY step_size DESC;
