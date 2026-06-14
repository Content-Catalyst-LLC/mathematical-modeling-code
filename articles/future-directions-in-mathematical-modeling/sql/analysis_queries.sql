.headers on
.mode column

SELECT 'FUTURE MODELING PRIORITY REVIEW' AS section;
SELECT
  direction_key,
  direction_name,
  modeling_area,
  ROUND(0.25 * complexity_relevance + 0.20 * technical_maturity + 0.20 * governance_need + 0.20 * uncertainty_pressure + 0.15 * human_judgment_need, 3) AS future_priority_score,
  CASE
    WHEN governance_need >= 0.85 OR human_judgment_need >= 0.90 THEN 'governance_priority'
    WHEN uncertainty_pressure >= 0.85 THEN 'uncertainty_priority'
    WHEN 0.25 * complexity_relevance + 0.20 * technical_maturity + 0.20 * governance_need + 0.20 * uncertainty_pressure + 0.15 * human_judgment_need >= 0.78 THEN 'strategic_priority'
    ELSE 'monitor'
  END AS review_class
FROM future_modeling_direction
ORDER BY future_priority_score DESC;

SELECT 'MODEL LIFECYCLE CHECKLIST' AS section;
SELECT lifecycle_stage, review_question, artifact FROM model_lifecycle_checklist;

SELECT 'HIGH-GOVERNANCE FUTURE DIRECTIONS' AS section;
SELECT direction_key, direction_name, governance_need, human_judgment_need
FROM future_modeling_direction
WHERE governance_need >= 0.85 OR human_judgment_need >= 0.90
ORDER BY governance_need DESC, human_judgment_need DESC;
