.headers on
.mode column

SELECT 'INPUT OUTPUT GOVERNANCE REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM input_output_governance_registry
ORDER BY assumption_key;

SELECT 'INPUT OUTPUT AUDIT CASES' AS section;
SELECT model_name, sectors, method, coefficient_basis, condition_number, maximum_output_multiplier, highest_multiplier_sector, total_baseline_output, total_shock_output_change, total_emissions_for_final_demand, warning
FROM input_output_audit_cases
ORDER BY model_name;
