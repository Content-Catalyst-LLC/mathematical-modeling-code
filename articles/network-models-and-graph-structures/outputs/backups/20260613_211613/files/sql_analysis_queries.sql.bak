.headers on
.mode column

SELECT 'NETWORK COMPONENT TYPES' AS section;
SELECT component_type, description, typical_failure
FROM network_component_type
ORDER BY component_type;

SELECT 'NETWORK RECORDS REQUIRING REVIEW' AS section;
SELECT record_key, component_type, expression_or_structure, review_question
FROM network_model_register
WHERE status IN ('review', 'revise');

SELECT 'OUT-DEGREE DIAGNOSTICS' AS section;
SELECT source AS node, COUNT(*) AS out_degree, ROUND(SUM(weight), 3) AS weighted_out_degree
FROM infrastructure_edge
GROUP BY source
ORDER BY weighted_out_degree DESC;

SELECT 'IN-DEGREE DIAGNOSTICS' AS section;
SELECT target AS node, COUNT(*) AS in_degree, ROUND(SUM(weight), 3) AS weighted_in_degree
FROM infrastructure_edge
GROUP BY target
ORDER BY weighted_in_degree DESC;

SELECT 'EDGE EVIDENCE SUMMARY' AS section;
SELECT evidence_quality, COUNT(*) AS edge_count, ROUND(AVG(weight), 3) AS average_weight
FROM infrastructure_edge
GROUP BY evidence_quality
ORDER BY edge_count DESC;
