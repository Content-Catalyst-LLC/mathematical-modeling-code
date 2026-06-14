.headers on
.mode column

SELECT 'COMPLEXITY FEATURE TYPES' AS section;
SELECT complexity_feature, description, modeling_risk
FROM complexity_feature_type
ORDER BY complexity_feature;

SELECT 'COMPLEXITY MODEL RECORDS REQUIRING REVIEW' AS section;
SELECT record_key, model_role, model_family, complexity_feature, decision_context
FROM complexity_model_register
WHERE status IN ('review', 'revise');

SELECT 'COMPLEXITY SCENARIO REVIEW' AS section;
SELECT
  scenario_key,
  scenario_name,
  stress_level,
  interdependence_level,
  uncertainty_level,
  ROUND(0.35 * stress_level + 0.30 * interdependence_level + 0.25 * uncertainty_level + 0.10 * (1.0 - adaptability_score), 3) AS fragility_score,
  ROUND(0.40 * resilience_score + 0.30 * equity_score + 0.30 * adaptability_score - 0.20 * (0.35 * stress_level + 0.30 * interdependence_level + 0.25 * uncertainty_level + 0.10 * (1.0 - adaptability_score)), 3) AS robust_value,
  CASE
    WHEN 0.35 * stress_level + 0.30 * interdependence_level + 0.25 * uncertainty_level + 0.10 * (1.0 - adaptability_score) >= 0.70 THEN 'high_complexity_risk'
    WHEN 0.35 * stress_level + 0.30 * interdependence_level + 0.25 * uncertainty_level + 0.10 * (1.0 - adaptability_score) >= 0.50 THEN 'complexity_review_required'
    ELSE 'standard_monitoring'
  END AS review_class
FROM complexity_scenario
ORDER BY fragility_score DESC;

SELECT 'COMPLEXITY DOMAIN GUIDE' AS section;
SELECT area, modeling_use, typical_model_forms
FROM complexity_domain_guide
ORDER BY area;

SELECT 'HIGH-ATTENTION COMPLEXITY REVIEW TARGETS' AS section;
SELECT record_key, model_family, complexity_feature, decision_context
FROM complexity_model_register
WHERE complexity_feature IN ('cascading_dependency', 'adaptive_behavior', 'uncertain_future_pathways', 'robustness_under_uncertainty');
