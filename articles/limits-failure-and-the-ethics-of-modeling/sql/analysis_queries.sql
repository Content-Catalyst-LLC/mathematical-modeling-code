.headers on
.mode column

SELECT 'MODEL FAILURE TYPES' AS section;
SELECT failure_mode, description, typical_harm
FROM model_failure_type
ORDER BY failure_mode;

SELECT 'MODEL FAILURE RECORDS REQUIRING REVIEW' AS section;
SELECT record_key, failure_mode, model_stage, ethical_issue, likely_cause, review_status
FROM model_failure_register
WHERE review_status IN ('review', 'revise');

SELECT 'MODEL ETHICS RISK REVIEW' AS section;
SELECT
  case_key,
  model_name,
  intended_use,
  ROUND(
    1.8 * severity +
    1.3 * likelihood +
    1.2 * detectability_gap +
    1.1 * uncertainty_level +
    1.5 * equity_concern +
    1.6 * accountability_gap,
    3
  ) AS ethical_risk_score,
  CASE
    WHEN 1.8 * severity + 1.3 * likelihood + 1.2 * detectability_gap + 1.1 * uncertainty_level + 1.5 * equity_concern + 1.6 * accountability_gap >= 6.0 THEN 'high_ethics_review_required'
    WHEN 1.8 * severity + 1.3 * likelihood + 1.2 * detectability_gap + 1.1 * uncertainty_level + 1.5 * equity_concern + 1.6 * accountability_gap >= 4.0 THEN 'governance_review_required'
    ELSE 'standard_review'
  END AS review_class,
  CASE WHEN equity_concern >= 0.50 THEN 'yes' ELSE 'no' END AS requires_equity_review,
  CASE WHEN accountability_gap >= 0.40 THEN 'yes' ELSE 'no' END AS requires_human_decision_owner
FROM model_ethics_risk_case
ORDER BY ethical_risk_score DESC;

SELECT 'MODEL ETHICS DOMAIN GUIDE' AS section;
SELECT area, review_use, typical_artifacts
FROM model_ethics_domain_guide
ORDER BY area;

SELECT 'HIGH-ATTENTION MODEL ETHICS TARGETS' AS section;
SELECT record_key, model_stage, ethical_issue, likely_cause
FROM model_failure_register
WHERE failure_mode IN ('validation_gap', 'false_precision', 'accountability_gap', 'scope_creep', 'data_bias');
