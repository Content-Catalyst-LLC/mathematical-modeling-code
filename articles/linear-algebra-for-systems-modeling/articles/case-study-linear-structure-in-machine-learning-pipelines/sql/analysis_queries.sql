.headers on
.mode column

SELECT 'MACHINE LEARNING PIPELINE GOVERNANCE REGISTRY' AS section;
SELECT governance_name, modeling_role, review_requirement, responsible_use_warning
FROM machine_learning_pipeline_governance_registry
ORDER BY governance_key;

SELECT 'FEATURE METADATA' AS section;
SELECT feature_name, measurement_role, preprocessing_note, governance_warning
FROM ml_pipeline_feature_metadata
ORDER BY feature_name;

SELECT 'MACHINE LEARNING LINEAR STRUCTURE AUDIT CASES' AS section;
SELECT workflow_name, scenario_name, observation_count, feature_count, train_count, test_count, model_family, regularization_strength, test_rmse, max_absolute_residual, largest_weight_feature, preprocessing_summary, leakage_warning, interpretation_warning
FROM machine_learning_linear_structure_audit_cases
ORDER BY workflow_name;
