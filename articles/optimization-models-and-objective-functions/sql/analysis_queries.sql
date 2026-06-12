.headers on
.mode column

SELECT 'OPTIMIZATION COMPONENT TYPES' AS section;
SELECT component_type, description, typical_failure
FROM optimization_component_type
ORDER BY component_type;

SELECT 'OPTIMIZATION RECORDS REQUIRING REVIEW' AS section;
SELECT record_key, component_type, expression, review_question
FROM optimization_model_register
WHERE status IN ('review', 'revise');

SELECT 'PROGRAM DATA' AS section;
SELECT program, benefit_per_unit, cost_per_unit, lower_bound, upper_bound,
       ROUND(benefit_per_unit / cost_per_unit, 3) AS benefit_cost_ratio
FROM program
ORDER BY benefit_cost_ratio DESC;

SELECT 'SCENARIO DATA' AS section;
SELECT scenario, budget, equity_floor, description
FROM optimization_scenario
ORDER BY scenario;

SELECT 'MINIMUM FLOOR COST BY SCENARIO' AS section;
SELECT
  s.scenario,
  s.budget,
  s.equity_floor,
  SUM(p.cost_per_unit * s.equity_floor) AS minimum_floor_cost,
  CASE
    WHEN SUM(p.cost_per_unit * s.equity_floor) <= s.budget THEN 'floor feasible by cost'
    ELSE 'floor infeasible by cost'
  END AS floor_feasibility
FROM optimization_scenario s
CROSS JOIN program p
GROUP BY s.scenario, s.budget, s.equity_floor;

SELECT 'OPTIMIZATION COMPONENT GUIDE' AS section;
SELECT component_type, meaning, example, review_question
FROM optimization_component_guide
ORDER BY component_type;
