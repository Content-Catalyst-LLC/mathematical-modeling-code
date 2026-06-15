DROP TABLE IF EXISTS field_assumption_registry;
DROP TABLE IF EXISTS field_audit_cases;

CREATE TABLE field_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO field_assumption_registry VALUES
('domain_definition','Domain definition','Specifies where the scalar or vector field is defined.','Determines what spatial region or state space the model covers.','Field claims are incomplete without a valid domain.'),
('scalar_field_definition','Scalar field definition','Assigns a scalar value to each point in a domain.','Represents temperature density exposure risk pressure cost or suitability.','Scalar units and source assumptions must be documented.'),
('vector_field_definition','Vector field definition','Assigns a vector to each point in a domain.','Represents velocity flow force displacement or direction of change.','Vector component units and coordinate conventions must be documented.'),
('grid_resolution','Grid resolution','Defines computational sampling of a continuous field.','Shapes how field structure appears in numerical outputs.','Coarse grids may hide local hotspots discontinuities or directional changes.'),
('smoothness_assumption','Smoothness assumption','Allows derivatives gradients and continuous spatial reasoning.','Supports calculus-based field analysis.','Smooth field assumptions may hide thresholds breaks or network boundaries.'),
('visualization_choice','Visualization choice','Maps field values to arrows contours streamlines surfaces or colors.','Communicates field structure.','Visual choices can exaggerate or hide variation.');

CREATE TABLE field_audit_cases (
    scenario TEXT NOT NULL,
    grid_step REAL NOT NULL,
    point_count INTEGER NOT NULL,
    scalar_average REAL NOT NULL,
    scalar_minimum REAL NOT NULL,
    scalar_maximum REAL NOT NULL,
    vector_magnitude_average REAL NOT NULL,
    vector_magnitude_maximum REAL NOT NULL,
    domain_description TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO field_audit_cases VALUES
('coarse_grid',1.0,49,21.999,18.500,24.500,2.700,4.242641,'square domain [-3,3] x [-3,3]','Grid resolution is coarse; field structure may be undersampled.'),
('medium_grid',0.5,169,21.750,18.500,24.500,2.520,4.242641,'square domain [-3,3] x [-3,3]','Synthetic field audit; document domain units and interpolation assumptions.'),
('fine_grid',0.25,625,21.625,18.500,24.500,2.420,4.242641,'square domain [-3,3] x [-3,3]','Synthetic field audit; document domain units and interpolation assumptions.');
