.headers on
.mode column

SELECT 'RELATIONSHIP TYPES' AS section;
SELECT relationship_type, description, typical_failure
FROM relationship_type
ORDER BY relationship_type;

SELECT 'RELATIONSHIPS REQUIRING REVIEW' AS section;
SELECT relationship_key, relationship_type, expression, review_question
FROM relationship_register
WHERE status IN ('review', 'revise');

SELECT 'SCENARIOS BY STRUCTURE' AS section;
SELECT structure, COUNT(*) AS scenario_count
FROM structure_scenario
GROUP BY structure
ORDER BY structure;

SELECT 'STRUCTURE REVIEW MATRIX' AS section;
SELECT structure, appropriate_use, main_risk, diagnostic
FROM structure_review_matrix
ORDER BY structure;
