DROP TABLE IF EXISTS orthogonality_assumption_registry;
DROP TABLE IF EXISTS orthogonality_audit_cases;

CREATE TABLE orthogonality_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO orthogonality_assumption_registry VALUES
('inner_product','Inner product','Defines alignment angle length and orthogonality.','Determines what it means for system components to be separated.','Changing weights units or scaling can change orthogonality.'),
('dot_product_zero','Zero dot product','Defines perpendicularity under the standard Euclidean inner product.','Indicates no overlap between directions under the chosen geometry.','Zero dot product is not automatically real-world independence.'),
('orthogonal_set','Orthogonal set','A set of vectors with pairwise zero inner products.','Provides separated directions for representation or decomposition.','Vectors must be nonzero to form a basis.'),
('orthonormal_basis','Orthonormal basis','A basis of mutually orthogonal unit vectors.','Supports simple coordinates stable decomposition and clean projection.','Coordinates may be abstract even when numerically convenient.'),
('orthogonal_projection','Orthogonal projection','Separates vectors into subspace and orthogonal residual components.','Distinguishes modeled structure from residual structure.','Residuals may contain important excluded signal or bias.'),
('qr_decomposition','QR decomposition','Factors a matrix into orthonormal directions and triangular coefficients.','Supports stable least-squares and structured simplification workflows.','Rank and conditioning should still be reviewed.');

CREATE TABLE orthogonality_audit_cases (
    system_name TEXT NOT NULL,
    vector_a TEXT NOT NULL,
    vector_b TEXT NOT NULL,
    dot_product REAL NOT NULL,
    orthogonal_under_tolerance INTEGER NOT NULL,
    residual_norm REAL NOT NULL,
    orthonormality_error REAL NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO orthogonality_audit_cases VALUES
('three_component_orthogonality_audit','3.000000,1.000000,2.000000','1.000000,-1.000000,-1.000000',0.0,1,3.741657,0.0,'Orthogonality depends on geometry scaling units tolerance and domain interpretation.');
