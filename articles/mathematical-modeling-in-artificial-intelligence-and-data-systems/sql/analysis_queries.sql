.headers on
.mode column

SELECT 'AI MODEL ROLE TYPES' AS section;
SELECT model_role, description, typical_failure
FROM ai_model_role_type
ORDER BY model_role;

SELECT 'AI MODEL RECORDS REQUIRING REVIEW' AS section;
SELECT record_key, model_role, model_family, data_domain, decision_context
FROM ai_model_register
WHERE status IN ('review', 'revise');

SELECT 'AI MODEL CANDIDATE GOVERNANCE REVIEW' AS section;
SELECT
  candidate_key,
  model_name,
  validation_score,
  calibration_error,
  subgroup_error_gap,
  drift_score,
  privacy_risk,
  ROUND(validation_score - (
      1.8 * calibration_error +
      1.5 * subgroup_error_gap +
      1.2 * drift_score +
      1.4 * privacy_risk +
      0.7 * deployment_criticality -
      0.5 * interpretability_score
  ), 3) AS governance_score,
  CASE
    WHEN deployment_criticality > 0.75 AND (
      calibration_error > 0.08 OR subgroup_error_gap > 0.12 OR drift_score > 0.20 OR privacy_risk > 0.15 OR interpretability_score < 0.50
    ) THEN 'high_stakes_review_required'
    WHEN calibration_error > 0.08 OR subgroup_error_gap > 0.12 OR drift_score > 0.20 OR privacy_risk > 0.15 OR interpretability_score < 0.50 THEN 'requires_governance_review'
    ELSE 'deployment_candidate'
  END AS review_class
FROM model_candidate
ORDER BY governance_score DESC;

SELECT 'AI DATA SYSTEMS DOMAIN GUIDE' AS section;
SELECT area, modeling_use, typical_model_forms
FROM ai_data_systems_domain_guide
ORDER BY area;

SELECT 'HIGH-ATTENTION AI REVIEW TARGETS' AS section;
SELECT record_key, model_role, model_family, decision_context
FROM ai_model_register
WHERE model_role IN ('ranking', 'generation', 'monitoring', 'governance');
