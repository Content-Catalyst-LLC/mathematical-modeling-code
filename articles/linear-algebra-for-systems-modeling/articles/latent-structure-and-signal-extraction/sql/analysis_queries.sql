.headers on
.mode column

SELECT 'LATENT STRUCTURE GOVERNANCE REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM latent_structure_governance_registry
ORDER BY assumption_key;

SELECT 'LATENT STRUCTURE AUDIT CASES' AS section;
SELECT model_name, observations, variables, method, preprocessing, retained_rank, retained_signal_ratio, relative_reconstruction_error, maximum_observation_residual, highest_residual_observation, warning
FROM latent_structure_audit_cases
ORDER BY model_name;
