.headers on
.mode column

SELECT 'PCA GOVERNANCE REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM pca_governance_registry
ORDER BY assumption_key;

SELECT 'PCA DIAGNOSTIC AUDIT CASES' AS section;
SELECT model_name, observations, variables, preprocessing, retained_components, explained_variance_ratio, cumulative_explained_variance, relative_reconstruction_error, largest_loading_variable_pc1, largest_loading_variable_pc2, warning
FROM pca_diagnostic_audit_cases
ORDER BY model_name;
