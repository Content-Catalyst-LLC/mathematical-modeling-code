DROP TABLE IF EXISTS latent_structure_governance_registry;
DROP TABLE IF EXISTS latent_structure_audit_cases;

CREATE TABLE latent_structure_governance_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO latent_structure_governance_registry VALUES
('observed_matrix','Observed matrix','Defines observations variables measurements units and missing-data handling.','Determines what latent structure can be inferred.','Latent structure is only as meaningful as the observed matrix construction.'),
('preprocessing','Preprocessing','Defines centering scaling normalization transformation weighting and filtering.','Determines which patterns appear dominant or residual.','Preprocessing choices can change extracted signal.'),
('method_choice','Method choice','Defines whether structure is extracted through SVD PCA factor models NMF ICA embeddings or another method.','Determines what kind of hidden structure the model is able to represent.','Different methods extract different structures and should not be interpreted interchangeably.'),
('rank_or_dimension','Rank or latent dimension','Defines how many components factors sources or latent coordinates are retained.','Controls signal extraction residual size interpretability and compression.','Rank choice should be justified and sensitivity-tested.'),
('signal_definition','Signal definition','Defines which extracted components are treated as structured signal.','Determines what is retained for interpretation monitoring or decision-making.','Signal is a modeling designation not an automatic property of the data.'),
('residual_review','Residual review','Defines how unexplained variation is assessed.','Supports detection of noise anomaly omitted structure subgroup mismatch or system change.','Residuals should be reviewed before being dismissed as noise.'),
('stability_validation','Stability validation','Assesses whether extracted structure persists across preprocessing samples time groups rank choices and seeds.','Supports trust in extracted signal.','Unstable latent structure should not be overinterpreted.'),
('responsible_interpretation','Responsible interpretation','Defines how latent components scores factors or embeddings are explained and used.','Prevents hidden coordinates from becoming unreviewed proxies for people places risk capacity or value.','Latent components are inferred model artifacts not automatic causes categories or truths.');

CREATE TABLE latent_structure_audit_cases (
    model_name TEXT NOT NULL,
    observations INTEGER NOT NULL,
    variables INTEGER NOT NULL,
    method TEXT NOT NULL,
    preprocessing TEXT NOT NULL,
    retained_rank INTEGER NOT NULL,
    retained_signal_ratio REAL NOT NULL,
    relative_reconstruction_error REAL NOT NULL,
    maximum_observation_residual REAL NOT NULL,
    highest_residual_observation INTEGER NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO latent_structure_audit_cases VALUES
('synthetic_latent_structure_signal_extraction_audit',9,6,'svd_low_rank_signal_extraction','centered_and_standardized',2,0.962,0.195,1.43,8,'Latent components are inferred model artifacts not automatic causes categories mechanisms or complete system truths.');
