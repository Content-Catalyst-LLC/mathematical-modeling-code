.headers on
.mode column

SELECT 'INFRASTRUCTURE GOVERNANCE REGISTRY' AS section;
SELECT governance_name, modeling_role, review_requirement, responsible_use_warning
FROM infrastructure_interdependence_governance_registry
ORDER BY governance_key;

SELECT 'DEPENDENCY BURDEN BY SUPPORT SECTOR' AS section;
SELECT support_sector, ROUND(SUM(dependency_weight), 3) AS dependency_burden
FROM infrastructure_dependency_matrix
GROUP BY support_sector
ORDER BY dependency_burden DESC;

SELECT 'INFRASTRUCTURE INTERDEPENDENCE AUDIT CASES' AS section;
SELECT workflow_name, scenario_name, sector_count, initial_shock_sector, initial_shock_magnitude, highest_dependency_burden_sector, highest_dependency_burden, largest_downstream_loss_sector, largest_downstream_loss, total_estimated_downstream_loss, sensitivity_warning, interpretation_warning
FROM infrastructure_interdependence_audit_cases
ORDER BY workflow_name;
