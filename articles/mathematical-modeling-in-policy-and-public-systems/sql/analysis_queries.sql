.headers on
.mode column

SELECT 'POLICY MODEL ROLE TYPES' AS section;
SELECT model_role, description, typical_failure
FROM policy_model_role_type
ORDER BY model_role;

SELECT 'POLICY MODEL RECORDS REQUIRING REVIEW' AS section;
SELECT record_key, policy_domain, model_role, model_family, public_question
FROM policy_model_register
WHERE status IN ('review', 'revise');

SELECT 'POLICY OPTION PUBLIC REVIEW' AS section;
SELECT
  option_key,
  option_name,
  projected_benefit,
  total_cost,
  ROUND(40.0 - total_cost, 3) AS budget_margin,
  equity_score,
  public_risk,
  uncertainty_width,
  ROUND(projected_benefit + 18.0 * implementation_feasibility + 24.0 * equity_score - total_cost - 0.22 * uncertainty_width - 30.0 * public_risk - CASE WHEN total_cost > 40.0 THEN 14.0 ELSE 0.0 END, 3) AS public_value_score,
  CASE
    WHEN public_risk > 0.38 THEN 'requires_risk_review'
    WHEN equity_score < 0.65 THEN 'requires_equity_review'
    WHEN total_cost > 40.0 THEN 'requires_budget_review'
    ELSE 'within_budget'
  END AS review_class
FROM policy_option
ORDER BY public_value_score DESC;

SELECT 'POLICY DOMAIN GUIDE' AS section;
SELECT policy_area, modeling_use, typical_model_forms
FROM policy_domain_guide
ORDER BY policy_area;

SELECT 'HIGH-ATTENTION PUBLIC REVIEW TARGETS' AS section;
SELECT record_key, policy_domain, model_role, public_question
FROM policy_model_register
WHERE model_role IN ('option_comparison', 'distributional_review', 'model_governance', 'forecasting');
