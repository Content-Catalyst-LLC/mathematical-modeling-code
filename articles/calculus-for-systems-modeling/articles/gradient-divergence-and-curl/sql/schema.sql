DROP TABLE IF EXISTS field_operator_assumption_registry;
DROP TABLE IF EXISTS field_operator_audit_cases;

CREATE TABLE field_operator_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO field_operator_assumption_registry VALUES
('scalar_field_definition','Scalar field definition','Defines the field to which the gradient is applied.','Determines what steepest increase means in the modeled system.','A gradient is not interpretable without a meaningful scalar field.'),
('vector_field_definition','Vector field definition','Defines the field to which divergence and curl are applied.','Determines what spreading convergence or rotation means.','Divergence and curl require meaningful vector components and units.'),
('grid_spacing','Grid spacing','Defines numerical derivative resolution.','Shapes computed gradient divergence and curl values.','Coarse grids can miss local derivative structure.'),
('coordinate_system','Coordinate system','Defines derivative directions and spatial units.','Controls distance direction and operator interpretation.','Coordinate distortion can mislead derivative-based interpretation.'),
('boundary_handling','Boundary handling','Defines how derivatives are estimated near domain edges.','Shapes edge behavior and operator summaries.','Boundary estimates may be unstable or method-dependent.'),
('smoothing','Smoothing','Controls noise reduction before derivative estimation.','Shapes operator signals and may hide local structure.','Smoothing choices must be documented.');

CREATE TABLE field_operator_audit_cases (
    scenario TEXT NOT NULL,
    grid_step REAL NOT NULL,
    point_count INTEGER NOT NULL,
    mean_gradient_magnitude REAL NOT NULL,
    maximum_gradient_magnitude REAL NOT NULL,
    mean_divergence REAL NOT NULL,
    mean_curl REAL NOT NULL,
    maximum_abs_curl REAL NOT NULL,
    field_description TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO field_operator_audit_cases VALUES
('coarse_grid',1.0,9,2.145,2.828,0.0,2.0,2.0,'scalar f=x^2+y^2; vector F=<-y,x>','Grid step is coarse; local derivative structure may be undersampled.'),
('medium_grid',0.5,25,1.875,2.828,0.0,2.0,2.0,'scalar f=x^2+y^2; vector F=<-y,x>','Synthetic field-operator audit; document field definitions units grid and boundary rules.'),
('fine_grid',0.25,81,1.700,2.828,0.0,2.0,2.0,'scalar f=x^2+y^2; vector F=<-y,x>','Synthetic field-operator audit; document field definitions units grid and boundary rules.');
