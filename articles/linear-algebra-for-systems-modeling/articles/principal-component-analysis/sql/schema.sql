DROP TABLE IF EXISTS pca_governance_registry;
DROP TABLE IF EXISTS pca_diagnostic_audit_cases;

CREATE TABLE pca_governance_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO pca_governance_registry VALUES
('data_matrix_construction','Data matrix construction','Defines observations variables entries units and missing-data treatment.','Determines what principal components can represent.','PCA interpretation is only as meaningful as the matrix construction.'),
('centering','Centering','Subtracts variable means before decomposition.','Defines the baseline around which variation is measured.','Uncentered PCA may capture mean offsets rather than variation structure.'),
('scaling','Scaling','Determines whether variables are analyzed in original units or standardized units.','Controls whether high-variance variables dominate the components.','Scaling choices can substantially change PCA results.'),
('retained_components','Retained components','Defines how many principal directions are kept.','Determines compression dimensionality reduction reconstruction error and residual variation.','Discarded components may contain rare local or high-consequence structure.'),
('explained_variance','Explained variance','Measures variance captured by each component.','Supports rank selection and dimensionality-reduction review.','Explained variance is not the same as causal ethical or decision importance.'),
('loadings_interpretation','Loadings interpretation','Defines how variable contributions to components are read.','Connects component directions to original variables.','Loadings describe mathematical directions not automatic mechanisms.'),
('residual_review','Residual review','Defines how reconstruction error and discarded variation are assessed.','Determines whether low-dimensional approximation is adequate.','Residuals should be reviewed before being dismissed as noise.'),
('outlier_review','Outlier review','Assesses the influence of extreme observations on variance directions.','Supports robust interpretation of component structure.','Outliers may represent error rare cases or important system transitions.');

CREATE TABLE pca_diagnostic_audit_cases (
    model_name TEXT NOT NULL,
    observations INTEGER NOT NULL,
    variables INTEGER NOT NULL,
    preprocessing TEXT NOT NULL,
    retained_components INTEGER NOT NULL,
    explained_variance_ratio TEXT NOT NULL,
    cumulative_explained_variance REAL NOT NULL,
    relative_reconstruction_error REAL NOT NULL,
    largest_loading_variable_pc1 TEXT NOT NULL,
    largest_loading_variable_pc2 TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO pca_diagnostic_audit_cases VALUES
('synthetic_pca_diagnostic_audit',8,5,'centered_and_standardized',2,'0.946;0.044;0.007;0.002;0.001',0.990,0.100,'transport_delay','water_demand','PCA components depend on data matrix construction centering scaling outliers retained-rank choice explained-variance criteria residual review and domain interpretation.');
