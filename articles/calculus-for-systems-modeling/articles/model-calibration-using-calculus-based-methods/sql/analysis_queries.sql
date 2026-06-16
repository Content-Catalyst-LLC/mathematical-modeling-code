.headers on
.mode column

SELECT 'CALIBRATION GOVERNANCE REGISTRY' AS section;
SELECT calibration_name, analytical_role, systems_modeling_role, review_warning
FROM calibration_governance_registry
ORDER BY calibration_key;

SELECT 'CALIBRATION PARAMETER RECORDS' AS section;
SELECT parameter_name, baseline_value, lower_bound, upper_bound, unit_note, calibration_warning
FROM calibration_parameter_records
ORDER BY parameter_name;
