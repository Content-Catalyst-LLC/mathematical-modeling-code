.headers on
.mode column

SELECT 'INPUT-OUTPUT GOVERNANCE REGISTRY' AS section;
SELECT governance_name, modeling_role, review_requirement, responsible_use_warning
FROM economic_input_output_governance_registry
ORDER BY governance_key;

SELECT 'TECHNICAL COEFFICIENTS BY OUTPUT SECTOR' AS section;
SELECT output_sector, ROUND(SUM(coefficient), 3) AS direct_input_requirement_sum
FROM technical_coefficients
GROUP BY output_sector
ORDER BY direct_input_requirement_sum DESC;

SELECT 'FINAL DEMAND' AS section;
SELECT sector, final_demand
FROM final_demand
ORDER BY sector;

SELECT 'ECONOMIC INPUT-OUTPUT AUDIT CASES' AS section;
SELECT workflow_name, economy_name, sector_count, final_demand_total, gross_output_total, highest_multiplier_sector, highest_output_multiplier, shock_sector, shock_amount, gross_output_change_total, leontief_infinity_condition_estimate, solvability_warning, interpretation_warning
FROM economic_input_output_audit_cases
ORDER BY workflow_name;
