.headers on
.mode column

SELECT 'IMPLICIT RELATIONSHIP REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM implicit_relationship_registry
ORDER BY assumption_key;
