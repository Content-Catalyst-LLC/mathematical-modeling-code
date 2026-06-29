DROP TABLE IF EXISTS geometric_transformation_assumption_registry;
DROP TABLE IF EXISTS projection_reflection_audit_cases;

CREATE TABLE geometric_transformation_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO geometric_transformation_assumption_registry VALUES
('projection','Projection','Maps a vector onto a target subspace.','Retains model-representable structure and separates residual structure.','The target subspace must be justified.'),
('residual','Residual','Difference between the original vector and its projection.','Represents unexplained discarded or unmodeled structure.','Residuals may contain important signal not merely noise.'),
('orthogonality','Orthogonality','Perpendicularity under an inner product.','Defines what it means for residuals to be independent of modeled directions.','Orthogonality depends on the chosen geometry or weighting.'),
('projection_matrix','Projection matrix','A matrix satisfying idempotence with symmetry for orthogonal projection.','Maps observations to fitted or retained structure.','Projection matrices should be checked for idempotence and symmetry.'),
('reflection','Reflection','Preserves mirror-subspace components and reverses perpendicular components.','Represents symmetry reversal or orientation change.','Reflection is not the same as approximation or information loss.'),
('distance_geometry','Distance geometry','Uses norms and inner products to measure closeness and angle.','Determines what counts as closest approximation or residual size.','Units scaling and weighting affect geometric conclusions.');

CREATE TABLE projection_reflection_audit_cases (
    system_name TEXT NOT NULL,
    original_vector TEXT NOT NULL,
    unit_direction TEXT NOT NULL,
    projected_vector TEXT NOT NULL,
    residual_vector TEXT NOT NULL,
    residual_norm REAL NOT NULL,
    reflected_vector TEXT NOT NULL,
    projection_idempotence_error REAL NOT NULL,
    projection_symmetry_error REAL NOT NULL,
    reflection_involution_error REAL NOT NULL,
    length_preservation_error REAL NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO projection_reflection_audit_cases VALUES
('two_dimensional_geometric_transformation_audit','4.000000,3.000000','0.894427,0.447214','4.400000,2.200000','-0.400000,0.800000',0.894427,'4.800000,1.400000',0.0,0.0,0.0,0.0,'Projection and reflection interpretation depends on geometry units scaling and model purpose.');
