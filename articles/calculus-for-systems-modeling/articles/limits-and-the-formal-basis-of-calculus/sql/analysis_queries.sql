.headers on
.mode column

SELECT 'LIMIT ASSUMPTION REGISTRY' AS section;
SELECT concept_name, formal_role, systems_modeling_role, review_warning
FROM limit_assumption_registry
ORDER BY assumption_key;

SELECT 'EPSILON BANDS' AS section;
SELECT * FROM epsilon_band
ORDER BY epsilon_value DESC;

SELECT 'CONVERGENCE MODES' AS section;
SELECT mode_name, mathematical_strength, modeling_warning
FROM convergence_mode
ORDER BY mode_key;
