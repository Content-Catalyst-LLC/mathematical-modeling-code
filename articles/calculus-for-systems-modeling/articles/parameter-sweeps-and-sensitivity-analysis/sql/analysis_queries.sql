.headers on
.mode column

SELECT 'PARAMETER SENSITIVITY REGISTRY' AS section;
SELECT sensitivity_name, analytical_role, systems_modeling_role, review_warning
FROM parameter_sensitivity_registry
ORDER BY sensitivity_key;

SELECT 'PARAMETER SWEEP DESIGN' AS section;
SELECT parameter_name, baseline_value, minimum_value, maximum_value, unit_note, review_warning
FROM parameter_sweep_design
ORDER BY parameter_name;
