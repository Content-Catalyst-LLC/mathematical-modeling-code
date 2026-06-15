DROP TABLE IF EXISTS line_integral_assumption_registry;
DROP TABLE IF EXISTS line_integral_audit_cases;

CREATE TABLE line_integral_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO line_integral_assumption_registry VALUES
('path_definition','Path definition','Specifies the curve or trajectory over which the integral is computed.','Determines the route corridor boundary or state-space path being analyzed.','A line integral is not interpretable without a clearly defined path.'),
('path_direction','Path direction','Defines the orientation of a parameterized curve.','Determines sign and interpretation for vector line integrals.','Reversing direction changes vector line-integral sign.'),
('scalar_field_units','Scalar field units','Defines the quantity accumulated per unit path length.','Supports exposure cost burden resistance or risk interpretation.','Scalar line-integral units combine field units and distance units.'),
('vector_field_units','Vector field units','Defines the directed field being dotted with displacement.','Supports work flow support resistance or circulation interpretation.','Component units and coordinate units must be compatible.'),
('sampling_resolution','Sampling resolution','Defines how the continuous path is approximated by segments.','Shapes computed path length scalar accumulation and vector alignment.','Coarse sampling can miss turns or field variation.');

CREATE TABLE line_integral_audit_cases (
    scenario TEXT NOT NULL,
    time_step REAL NOT NULL,
    point_count INTEGER NOT NULL,
    path_length REAL NOT NULL,
    scalar_line_integral REAL NOT NULL,
    vector_line_integral REAL NOT NULL,
    average_alignment REAL NOT NULL,
    maximum_segment_length REAL NOT NULL,
    path_description TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO line_integral_audit_cases VALUES
('coarse_path',1.0,7,7.42,11.2,17.6,2.3,1.40,'path r(t)=<t,sin(t)>','Time step is coarse; path turns and field variation may be undersampled.'),
('medium_path',0.5,13,7.60,11.5,18.2,2.4,0.70,'path r(t)=<t,sin(t)>','Synthetic line-integral audit; document path field units and interpolation.'),
('fine_path',0.25,26,7.63,11.7,18.5,2.4,0.35,'path r(t)=<t,sin(t)>','Synthetic line-integral audit; document path field units and interpolation.');
