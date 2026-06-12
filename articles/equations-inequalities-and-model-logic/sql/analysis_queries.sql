.headers on
.mode column

SELECT 'STATEMENT TYPES' AS section;
SELECT statement_type, description, typical_failure
FROM statement_type
ORDER BY statement_type;

SELECT 'FORMAL STATEMENTS REQUIRING REVIEW' AS section;
SELECT statement_key, statement_type, expression, domain_or_condition, review_question
FROM formal_statement_register
WHERE status IN ('review', 'revise');

SELECT 'LOGIC SCENARIOS' AS section;
SELECT scenario, initial_stock, capacity, inflow, demand, loss_rate, low_storage_threshold, periods
FROM logic_scenario
ORDER BY scenario;

SELECT 'TRANSFORMATION AUDIT' AS section;
SELECT transformation, requirement, risk, review_question
FROM transformation_audit
ORDER BY transformation;
