.headers on
.mode column

SELECT 'SPATIAL COMPONENT TYPES' AS section;
SELECT component_type, description, typical_failure
FROM spatial_component_type
ORDER BY component_type;

SELECT 'SPATIAL RECORDS REQUIRING REVIEW' AS section;
SELECT record_key, component_type, geometry_or_structure, review_question
FROM spatial_model_register
WHERE status IN ('review', 'revise');

SELECT 'SPATIAL LOCATIONS' AS section;
SELECT location_key, kind, x, y, value
FROM spatial_location
ORDER BY kind, location_key;

SELECT 'DEMAND AND SERVICE COUNTS' AS section;
SELECT kind, COUNT(*) AS location_count, ROUND(SUM(value), 3) AS total_value
FROM spatial_location
GROUP BY kind;

SELECT 'DISTANCE FROM DEMAND TO SERVICE LOCATIONS' AS section;
SELECT
  d.location_key AS demand_location,
  s.location_key AS service_location,
  ROUND(SQRT((d.x-s.x)*(d.x-s.x) + (d.y-s.y)*(d.y-s.y)), 4) AS euclidean_distance
FROM spatial_location d
JOIN spatial_location s ON d.kind='demand' AND s.kind='service'
ORDER BY d.location_key, euclidean_distance;

SELECT 'SPATIAL COMPONENT GUIDE' AS section;
SELECT component_type, meaning, example, review_question
FROM spatial_component_guide
ORDER BY component_type;
