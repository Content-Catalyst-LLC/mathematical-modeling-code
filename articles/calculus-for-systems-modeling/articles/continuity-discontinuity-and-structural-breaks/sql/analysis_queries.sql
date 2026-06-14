.headers on
.mode column

SELECT 'CONTINUITY CONCEPT REGISTRY' AS section;
SELECT concept_name, formal_role, systems_modeling_role, review_warning
FROM continuity_concept_registry
ORDER BY concept_key;

SELECT 'DIAGNOSTIC THRESHOLDS' AS section;
SELECT * FROM continuity_diagnostic_threshold
ORDER BY threshold_key;

SELECT 'STRUCTURAL BREAK TYPES' AS section;
SELECT break_name, diagnostic_signal, modeling_warning
FROM structural_break_type
ORDER BY break_key;
