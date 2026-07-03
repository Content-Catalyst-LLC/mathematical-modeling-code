.headers on
.mode column

SELECT 'LEONTIEF GOVERNANCE REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM leontief_governance_registry
ORDER BY assumption_key;

SELECT 'LEONTIEF SYSTEM AUDIT CASES' AS section;
SELECT model_name, sectors, method, coefficient_basis, spectral_radius, condition_number, productive_system_flag, maximum_output_multiplier, highest_multiplier_sector, total_output_required, total_shock_output_change, emissions_for_final_demand, warning
FROM leontief_system_audit_cases
ORDER BY model_name;
