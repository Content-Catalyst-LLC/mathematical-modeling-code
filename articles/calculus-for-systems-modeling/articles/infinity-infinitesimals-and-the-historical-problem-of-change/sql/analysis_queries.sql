.headers on
.mode column

SELECT 'CALCULUS CONCEPT REGISTRY' AS section;
SELECT concept_name, historical_role, systems_modeling_role, review_note
FROM calculus_concept_registry
ORDER BY concept_key;

SELECT 'APPROXIMATION STEPS' AS section;
SELECT step_key, h, interpretation
FROM approximation_step
ORDER BY h DESC;
