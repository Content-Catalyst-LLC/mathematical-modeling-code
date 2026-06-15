DROP TABLE IF EXISTS flow_assumption_registry;
DROP TABLE IF EXISTS flow_audit_cases;

CREATE TABLE flow_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO flow_assumption_registry VALUES
('vector_field_definition','Vector field definition','Defines the field used for flux and circulation.','Determines what movement force pressure transport or tendency means.','Flux and circulation are not interpretable without meaningful vector components and units.'),
('surface_boundary','Surface boundary','Defines where flux crossing is measured.','Represents a control surface system boundary envelope threshold or interface.','Flux answers a boundary-crossing question only if the boundary is meaningful.'),
('curve_orientation','Curve orientation','Defines positive direction for circulation.','Determines whether loop flow is counted as positive or negative.','Reversing path direction reverses circulation sign.'),
('normal_orientation','Normal orientation','Defines positive direction for flux.','Determines whether crossing is interpreted as inflow or outflow.','Reversing the normal reverses flux sign.'),
('sampling_resolution','Sampling resolution','Defines curve segments or surface patches used in numerical approximation.','Shapes computed flux and circulation values.','Coarse sampling may miss local flow variation.'),
('boundary_meaning','Boundary meaning','Connects geometry to a system boundary or pathway.','Supports responsible interpretation of crossing looping or exchange.','Arbitrary boundaries can answer irrelevant questions.');

CREATE TABLE flow_audit_cases (
    scenario TEXT NOT NULL,
    segment_count INTEGER NOT NULL,
    approximate_flux REAL NOT NULL,
    approximate_circulation REAL NOT NULL,
    mean_tangential_alignment REAL NOT NULL,
    mean_normal_alignment REAL NOT NULL,
    field_description TEXT NOT NULL,
    geometry_description TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO flow_audit_cases VALUES
('coarse_circle',16,0.0,6.122,0.980,0.0,'rotating field F=<-y,x>','counterclockwise circle with radius 1','Coarse path sampling; circulation and flux should be checked with more segments.'),
('medium_circle',64,0.0,6.273,0.998,0.0,'rotating field F=<-y,x>','counterclockwise circle with radius 1','Synthetic flow audit; document field meaning orientation units and boundary choice.'),
('fine_circle',256,0.0,6.282,1.000,0.0,'rotating field F=<-y,x>','counterclockwise circle with radius 1','Synthetic flow audit; document field meaning orientation units and boundary choice.');
