.headers on
.mode column

SELECT 'DIMENSIONALITY REDUCTION GOVERNANCE REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM dimensionality_reduction_governance_registry
ORDER BY assumption_key;

SELECT 'DIMENSIONALITY REDUCTION AUDIT CASES' AS section;
SELECT model_name, observations, original_dimensions, reduced_dimensions, method, preprocessing, preservation_target, explained_variance_retained, relative_reconstruction_error, mean_pairwise_distance_distortion, warning
FROM dimensionality_reduction_audit_cases
ORDER BY model_name;
