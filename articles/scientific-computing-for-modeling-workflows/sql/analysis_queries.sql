.headers on
.mode column

SELECT 'WORKFLOW STAGE TYPES' AS section;
SELECT workflow_stage, description, typical_failure
FROM workflow_stage_type
ORDER BY workflow_stage;

SELECT 'WORKFLOW RECORDS REQUIRING REVIEW' AS section;
SELECT record_key, workflow_stage, computational_object, review_question
FROM scientific_computing_workflow_register
WHERE status IN ('review', 'revise');

SELECT 'RESOURCE WORKFLOW SCENARIOS' AS section;
SELECT scenario, initial_stock, growth_rate, carrying_capacity, extraction, shock_probability, shock_fraction, steps, seed
FROM resource_workflow_scenario
ORDER BY scenario;

SELECT 'WORKFLOW GOVERNANCE CHECK' AS section;
SELECT workflow_stage, COUNT(*) AS record_count
FROM scientific_computing_workflow_register
GROUP BY workflow_stage
ORDER BY workflow_stage;

SELECT 'WORKFLOW COMPONENT GUIDE' AS section;
SELECT workflow_stage, meaning, example, review_question
FROM workflow_component_guide
ORDER BY workflow_stage;
