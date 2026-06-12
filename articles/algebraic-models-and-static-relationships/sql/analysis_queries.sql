.headers on
.mode column

SELECT 'RELATIONSHIP TYPES' AS section;
SELECT relationship_type, description, typical_failure
FROM relationship_type
ORDER BY relationship_type;

SELECT 'RELATIONSHIPS REQUIRING REVIEW' AS section;
SELECT relationship_key, relationship_type, expression, domain_or_constraint, review_question
FROM algebraic_relationship_register
WHERE status IN ('review', 'revise');

SELECT 'STATIC SCENARIOS WITH DERIVED VALUES' AS section;
SELECT
  scenario,
  budget,
  cost_a * allocation_a + cost_b * allocation_b AS total_cost,
  benefit_a * allocation_a + benefit_b * allocation_b AS total_benefit,
  budget - (cost_a * allocation_a + cost_b * allocation_b) AS budget_slack,
  CASE
    WHEN budget - (cost_a * allocation_a + cost_b * allocation_b) >= 0
      AND capacity_a - allocation_a >= 0
      AND capacity_b - allocation_b >= 0
    THEN 'feasible'
    ELSE 'constraint violation'
  END AS constraint_status
FROM static_allocation_scenario
ORDER BY scenario;

SELECT 'STATIC RELATIONSHIP GUIDE' AS section;
SELECT relationship_type, meaning, example, review_question
FROM static_relationship_guide
ORDER BY relationship_type;
