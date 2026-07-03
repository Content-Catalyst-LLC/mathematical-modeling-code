.headers on
.mode column

SELECT 'COMPRESSION GOVERNANCE REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM compression_governance_registry
ORDER BY assumption_key;

SELECT 'COMPRESSION NOISE AUDIT CASES' AS section;
SELECT model_name, rows, columns, method, preprocessing, retained_rank, retained_energy_ratio, discarded_energy_ratio, compression_ratio, relative_reconstruction_error, maximum_row_residual, highest_residual_row, warning
FROM compression_noise_audit_cases
ORDER BY model_name;
