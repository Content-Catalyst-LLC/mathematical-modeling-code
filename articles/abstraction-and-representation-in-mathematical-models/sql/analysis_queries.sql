.headers on
.mode column

SELECT 'TARGET SYSTEM' AS section;
SELECT target_name, target_description, intended_use FROM target_system;

SELECT 'REPRESENTATION FORMS' AS section;
SELECT representation_form, emphasizes, useful_for, limitation
FROM representation_form
ORDER BY representation_form;

SELECT 'REPRESENTATION CHOICES REQUIRING REVIEW' AS section;
SELECT target_feature, formal_representation, omitted_detail, review_question
FROM representation_choice
WHERE status IN ('review', 'revise');

SELECT 'SCENARIOS' AS section;
SELECT scenario, initial_stock, capacity, inflow, demand, loss_rate, periods
FROM scenario_parameter
ORDER BY scenario;
