.headers on
.mode column

SELECT 'STATE VECTOR ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM state_vector_assumption_registry
ORDER BY assumption_key;

SELECT 'STATE VECTOR COMPONENTS' AS section;
SELECT position, component_name, value, unit, scale_type, warning
FROM state_vector_components
ORDER BY position;
