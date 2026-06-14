.headers on
.mode column

SELECT 'DIFFERENTIABILITY ASSUMPTION REGISTRY' AS section;
SELECT concept_name, formal_role, systems_modeling_role, review_warning
FROM differentiability_assumption_registry
ORDER BY assumption_key;

SELECT 'DIAGNOSTIC THRESHOLDS' AS section;
SELECT * FROM derivative_diagnostic_threshold
ORDER BY threshold_key;

SELECT 'NONSMOOTH CASE TYPES' AS section;
SELECT case_name, diagnostic_signal, modeling_warning
FROM nonsmooth_case_type
ORDER BY case_key;
