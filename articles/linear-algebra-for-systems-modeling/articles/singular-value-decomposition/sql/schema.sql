DROP TABLE IF EXISTS svd_governance_registry;
DROP TABLE IF EXISTS svd_diagnostic_audit_cases;

CREATE TABLE svd_governance_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO svd_governance_registry VALUES
('matrix_construction','Matrix construction','Defines the rows columns entries units and meaning of the matrix being decomposed.','Determines what singular vectors and singular values can represent.','SVD interpretation is only as meaningful as the matrix construction.'),
('preprocessing','Preprocessing','Defines centering scaling normalization missing-data handling and weighting.','Determines which directions dominate the singular spectrum.','Different preprocessing choices can produce different components.'),
('rank_tolerance','Rank tolerance','Defines which singular values count as numerically meaningful.','Determines numerical rank pseudoinverse behavior and truncation decisions.','Tolerance choices should be documented and sensitivity-tested.'),
('retained_rank','Retained rank','Defines how many singular components are kept.','Determines compression dimensionality reduction and approximation quality.','Discarded components may contain rare local or high-consequence structure.'),
('condition_number','Condition number','Measures sensitivity through the ratio of largest to smallest relevant singular value.','Supports numerical stability and inverse-problem review.','Large condition numbers warn against overinterpreting recovered coefficients.'),
('pseudoinverse_threshold','Pseudoinverse threshold','Defines which singular values are inverted.','Determines whether weak directions are recovered suppressed or regularized.','Inverting small singular values can amplify noise.'),
('component_interpretation','Component interpretation','Defines how singular vectors and singular components are interpreted.','Connects mathematical directions to system meaning.','Singular vectors are not automatic causes categories or mechanisms.'),
('residual_review','Residual review','Defines how discarded or unexplained structure is assessed.','Determines whether residual components are treated as noise omitted structure or warning signals.','Residuals should be reviewed before being dismissed.');

CREATE TABLE svd_diagnostic_audit_cases (
    model_name TEXT NOT NULL,
    rows INTEGER NOT NULL,
    columns INTEGER NOT NULL,
    singular_values TEXT NOT NULL,
    numerical_rank INTEGER NOT NULL,
    rank_tolerance REAL NOT NULL,
    condition_number REAL NOT NULL,
    retained_rank INTEGER NOT NULL,
    explained_energy_retained REAL NOT NULL,
    relative_reconstruction_error REAL NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO svd_diagnostic_audit_cases VALUES
('synthetic_svd_diagnostic_audit',6,4,'14.35;8.16;0.19;0.04',4,1e-10,358.75,2,0.9992,0.0283,'SVD components depend on matrix construction preprocessing scaling centering rank tolerance retained-rank choice numerical method and domain interpretation.');
