.headers on
.mode column

SELECT 'QUANTITY TYPES' AS section;
SELECT quantity_type, description, typical_failure
FROM quantity_type
ORDER BY quantity_type;

SELECT 'UNIT RECORDS REQUIRING REVIEW' AS section;
SELECT unit_key, quantity_type, unit, dimension, review_question
FROM unit_register
WHERE status IN ('review', 'revise');

SELECT 'SCALE SCENARIOS' AS section;
SELECT scenario, initial_storage_m3, capacity_m3, inflow_m3_per_day, demand_m3_per_day, loss_rate_per_day, delta_t_days, periods
FROM scale_scenario
ORDER BY scenario;

SELECT 'CONVERSION AUDIT' AS section;
SELECT conversion, source_unit, target_unit, factor, review_question
FROM conversion_audit
ORDER BY conversion;
