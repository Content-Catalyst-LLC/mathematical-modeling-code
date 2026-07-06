.headers on
.mode column

SELECT 'DIMENSIONALITY REDUCTION GOVERNANCE REGISTRY' AS section;
SELECT governance_name, modeling_role, review_requirement, responsible_use_warning
FROM dimensionality_reduction_governance_registry
ORDER BY governance_key;

SELECT 'FEATURE MATRIX METADATA' AS section;
SELECT feature_name, measurement_role, preprocessing_note, governance_warning
FROM feature_matrix_metadata
ORDER BY feature_name;

SELECT 'DIMENSIONALITY REDUCTION AUDIT CASES' AS section;
SELECT workflow_name, scenario_name, observation_count, feature_count, retained_components, cumulative_explained_variance, reconstruction_rmse, dominant_component_feature, preprocessing_summary, validation_warning, interpretation_warning
FROM dimensionality_reduction_audit_cases
ORDER BY workflow_name;
