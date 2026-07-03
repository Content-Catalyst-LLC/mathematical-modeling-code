DROP TABLE IF EXISTS compression_governance_registry;
DROP TABLE IF EXISTS compression_noise_audit_cases;

CREATE TABLE compression_governance_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO compression_governance_registry VALUES
('original_representation','Original representation','Defines the original matrix signal feature table image field or state representation.','Determines what compression can preserve or lose.','Compression is only as meaningful as the original representation.'),
('preprocessing','Preprocessing','Defines centering scaling normalization transformation filtering and weighting.','Determines which structure appears dominant or discardable.','Preprocessing choices can change compression results.'),
('compression_method','Compression method','Defines how the original representation is encoded approximated reconstructed or filtered.','Determines what structure is preserved.','Different compression methods preserve different structure.'),
('retained_rank','Retained rank','Defines how many components or directions are kept.','Controls compression ratio reconstruction error residuals and interpretability.','Rank choice should be justified and sensitivity-tested.'),
('noise_definition','Noise definition','Defines which variation is treated as noise or discardable residual.','Determines what is suppressed or ignored.','Discarded variation is not automatically noise.'),
('reconstruction_error','Reconstruction error','Measures how much original structure is not recovered by the compressed representation.','Supports fidelity review.','Aggregate error can hide localized loss.'),
('residual_review','Residual review','Defines how lost or unexplained information is examined.','Supports discovery of weak signals anomalies omitted structure or subgroup mismatch.','Residuals should be reviewed before being dismissed.'),
('responsible_simplification','Responsible simplification','Defines how compression is explained validated and governed.','Prevents compressed models from hiding consequential information loss.','Compression should clarify structure without concealing uncertainty or harm.');

CREATE TABLE compression_noise_audit_cases (
    model_name TEXT NOT NULL,
    rows INTEGER NOT NULL,
    columns INTEGER NOT NULL,
    method TEXT NOT NULL,
    preprocessing TEXT NOT NULL,
    retained_rank INTEGER NOT NULL,
    retained_energy_ratio REAL NOT NULL,
    discarded_energy_ratio REAL NOT NULL,
    compression_ratio REAL NOT NULL,
    relative_reconstruction_error REAL NOT NULL,
    maximum_row_residual REAL NOT NULL,
    highest_residual_row INTEGER NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO compression_noise_audit_cases VALUES
('synthetic_compression_noise_audit',9,6,'svd_low_rank_compression','centered_and_standardized',2,0.962,0.038,1.6875,0.195,1.43,8,'Discarded components are not automatically noise and may contain weak signals localized structure subgroup patterns anomalies or early warning behavior.');
