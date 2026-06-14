.headers on
.mode column

SELECT 'RISK TIERS' AS section;
SELECT risk_tier, description, review_requirement
FROM risk_tier_type
ORDER BY
  CASE risk_tier
    WHEN 'low' THEN 1
    WHEN 'medium' THEN 2
    WHEN 'high' THEN 3
    WHEN 'critical' THEN 4
    ELSE 99
  END;

SELECT 'MODEL GOVERNANCE REGISTER REVIEW QUEUE' AS section;
SELECT
  record_key,
  model_name,
  risk_tier,
  validation_status,
  use_limit_status,
  monitoring_status,
  model_owner,
  decision_owner
FROM model_governance_register
WHERE validation_status <> 'validated_with_limits'
   OR use_limit_status NOT IN ('approved', 'approved_with_limits')
   OR monitoring_status <> 'active'
   OR risk_tier IN ('high', 'critical');

SELECT 'MODEL GOVERNANCE RISK REVIEW' AS section;
SELECT
  case_key,
  model_name,
  ROUND(
    0.20 * error_risk +
    0.20 * uncertainty_level +
    0.25 * consequence_level +
    0.20 * scope_misuse_risk +
    0.15 * accountability_gap,
    3
  ) AS governance_risk_score,
  CASE
    WHEN 0.20 * error_risk + 0.20 * uncertainty_level + 0.25 * consequence_level + 0.20 * scope_misuse_risk + 0.15 * accountability_gap >= 0.70 THEN 'escalation_required'
    WHEN 0.20 * error_risk + 0.20 * uncertainty_level + 0.25 * consequence_level + 0.20 * scope_misuse_risk + 0.15 * accountability_gap >= 0.55 THEN 'governance_review_required'
    ELSE 'standard_monitoring'
  END AS review_class,
  CASE WHEN uncertainty_level >= 0.60 THEN 'yes' ELSE 'no' END AS requires_uncertainty_brief,
  CASE WHEN scope_misuse_risk >= 0.45 THEN 'yes' ELSE 'no' END AS requires_use_limit_review,
  CASE WHEN accountability_gap >= 0.30 THEN 'yes' ELSE 'no' END AS requires_accountability_review
FROM model_governance_risk_case
ORDER BY governance_risk_score DESC;

SELECT 'MODEL LIFECYCLE CHECKLIST' AS section;
SELECT lifecycle_stage, review_question, artifact
FROM model_lifecycle_checklist;

SELECT 'GOVERNANCE DOMAIN GUIDE' AS section;
SELECT area, governance_use, typical_artifacts
FROM governance_domain_guide
ORDER BY area;
