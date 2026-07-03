DROP TABLE IF EXISTS decomposition_governance_registry;
DROP TABLE IF EXISTS orthogonal_approximation_audit_cases;

CREATE TABLE decomposition_governance_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO decomposition_governance_registry VALUES
('subspace_choice','Subspace choice','Defines the modeled space used for projection or approximation.','Determines what structure the model can represent.','Changing the subspace changes what becomes signal and what becomes residual.'),
('basis_construction','Basis construction','Defines how basis vectors are selected or orthogonalized.','Determines numerical stability and interpretability of components.','Basis choice should be documented especially when variables are correlated or scaled differently.'),
('projection_method','Projection method','Defines how the modeled component is computed.','Determines whether approximation is computed through direct projection QR SVD or another method.','Method choice affects numerical stability and auditability.'),
('rank_tolerance','Rank tolerance','Defines numerical threshold for independent directions.','Determines whether small directions are retained or discarded.','Numerical rank depends on scaling tolerance and modeling purpose.'),
('residual_interpretation','Residual interpretation','Defines how unexplained variation is treated.','Determines whether residuals are considered noise missing structure outliers or model failure.','Residuals should not be dismissed as noise without review.'),
('conditioning_review','Conditioning review','Measures numerical sensitivity of approximation.','Supports stability assessment and method selection.','Ill-conditioned systems require careful solver choice and diagnostic reporting.'),
('validation_context','Validation context','Defines how approximation quality is evaluated.','Connects residual size and captured structure to the system question.','Small residuals do not guarantee meaningful or responsible interpretation.');

CREATE TABLE orthogonal_approximation_audit_cases (
    model_name TEXT NOT NULL,
    rows INTEGER NOT NULL,
    columns INTEGER NOT NULL,
    numerical_rank INTEGER NOT NULL,
    condition_number REAL NOT NULL,
    residual_norm REAL NOT NULL,
    relative_residual_norm REAL NOT NULL,
    orthogonality_error REAL NOT NULL,
    coefficient_norm REAL NOT NULL,
    method TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO orthogonal_approximation_audit_cases VALUES
('synthetic_orthogonal_approximation_audit',6,3,3,58.0,0.346410,0.032100,0.0,2.513000,'qr_least_squares','Orthogonal approximation results depend on subspace choice scaling rank tolerance conditioning solver method residual interpretation data provenance and validation context.');
