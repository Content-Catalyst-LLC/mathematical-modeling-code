.headers on
.mode column
SELECT 'COMPONENT TYPES' AS section;
SELECT * FROM component_type;
SELECT 'COMPONENTS REQUIRING REVIEW' AS section;
SELECT symbol,name,component_type,unit_or_domain,review_question FROM component_register WHERE status IN ('review','revise');
SELECT 'SCENARIOS' AS section;
SELECT * FROM scenario_parameter ORDER BY scenario;
SELECT 'PARAMETER STATUS' AS section;
SELECT * FROM parameter_status ORDER BY parameter;
SELECT 'CONSTRAINT CATALOG' AS section;
SELECT * FROM constraint_catalog ORDER BY constraint_name;
