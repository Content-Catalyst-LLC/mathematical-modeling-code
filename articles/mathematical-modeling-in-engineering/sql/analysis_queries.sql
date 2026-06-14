.headers on
.mode column

SELECT 'ENGINEERING MODEL ROLE TYPES' AS section;
SELECT model_role, description, typical_failure
FROM engineering_model_role_type
ORDER BY model_role;

SELECT 'ENGINEERING MODEL RECORDS REQUIRING REVIEW' AS section;
SELECT record_key, engineering_domain, model_role, model_family, design_question
FROM engineering_model_register
WHERE status IN ('review', 'revise');

SELECT 'BEAM DESIGN SAFETY REVIEW' AS section;
SELECT
  design_key,
  width_m,
  height_m,
  load_n,
  ROUND((load_n * span_m / 4.0) * (height_m / 2.0) / (width_m * height_m * height_m * height_m / 12.0), 3) AS max_stress_pa,
  ROUND(allowable_stress_pa - ((load_n * span_m / 4.0) * (height_m / 2.0) / (width_m * height_m * height_m * height_m / 12.0)), 3) AS stress_margin_pa,
  ROUND(allowable_stress_pa / ((load_n * span_m / 4.0) * (height_m / 2.0) / (width_m * height_m * height_m * height_m / 12.0)), 3) AS safety_factor,
  CASE
    WHEN ((load_n * span_m / 4.0) * (height_m / 2.0) / (width_m * height_m * height_m * height_m / 12.0)) <= allowable_stress_pa THEN 'acceptable'
    ELSE 'fails_constraint'
  END AS review_class
FROM beam_design
ORDER BY safety_factor DESC;

SELECT 'DISCIPLINARY ENGINEERING GUIDE' AS section;
SELECT engineering_field, modeling_use, typical_model_forms
FROM engineering_domain_guide
ORDER BY engineering_field;

SELECT 'HIGH-ATTENTION ENGINEERING REVIEW TARGETS' AS section;
SELECT record_key, engineering_domain, model_role, design_question
FROM engineering_model_register
WHERE model_role IN ('safety_review', 'tradeoff_analysis', 'uncertainty_review', 'validation');
