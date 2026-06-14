.headers on
.mode column

SELECT 'AI ROLE TYPES' AS section;
SELECT ai_role, appropriate_use, role_boundary
FROM ai_role_type
ORDER BY ai_role;

SELECT 'AI ASSISTANCE RECORDS REQUIRING REVIEW' AS section;
SELECT record_key, modeling_stage, ai_role, artifact_type, provenance_required, human_review_required, status
FROM ai_assistance_register
WHERE human_review_required = 1 OR status IN ('review', 'revise');

SELECT 'HUMAN JUDGMENT RISK REVIEW' AS section;
SELECT
  case_key,
  judgment_point,
  decision_context,
  ROUND(
    0.25 * (1.0 - evidence_strength) +
    0.25 * uncertainty_level +
    0.25 * consequence_level +
    0.15 * automation_bias_risk +
    0.10 * (1.0 - accountability_clarity),
    3
  ) AS judgment_risk_score,
  CASE
    WHEN 0.25 * (1.0 - evidence_strength) + 0.25 * uncertainty_level + 0.25 * consequence_level + 0.15 * automation_bias_risk + 0.10 * (1.0 - accountability_clarity) >= 0.65 THEN 'escalation_required'
    WHEN 0.25 * (1.0 - evidence_strength) + 0.25 * uncertainty_level + 0.25 * consequence_level + 0.15 * automation_bias_risk + 0.10 * (1.0 - accountability_clarity) >= 0.50 THEN 'human_review_required'
    ELSE 'standard_review'
  END AS review_class,
  CASE WHEN consequence_level >= 0.70 THEN 'yes' ELSE 'no' END AS requires_use_limit_statement,
  CASE WHEN uncertainty_level >= 0.60 THEN 'yes' ELSE 'no' END AS requires_uncertainty_brief,
  CASE WHEN accountability_clarity < 0.70 THEN 'yes' ELSE 'no' END AS requires_accountability_owner
FROM human_judgment_case
ORDER BY judgment_risk_score DESC;

SELECT 'AI-ASSISTED MODELING DOMAIN GUIDE' AS section;
SELECT area, review_use, typical_artifacts
FROM ai_assisted_modeling_domain_guide
ORDER BY area;

SELECT 'HIGH-ATTENTION AI-ASSISTED MODELING TARGETS' AS section;
SELECT case_key, judgment_point, decision_context
FROM human_judgment_case
WHERE uncertainty_level >= 0.60 OR consequence_level >= 0.80 OR automation_bias_risk >= 0.60 OR accountability_clarity < 0.70;
