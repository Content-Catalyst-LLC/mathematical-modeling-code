DROP TABLE IF EXISTS stokes_theorem_assumption_registry;
DROP TABLE IF EXISTS stokes_theorem_audit_cases;

CREATE TABLE stokes_theorem_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO stokes_theorem_assumption_registry VALUES
('vector_field_definition','Vector field definition','Defines the field used for boundary circulation and curl.','Determines what flow force movement transport or tendency means.','Stokes theorem is not interpretable without a meaningful vector field.'),
('surface_definition','Surface definition','Defines the oriented surface across which curl is accumulated.','Represents an interface slice membrane control surface or conceptual surface.','The surface must be connected to the boundary curve used in the theorem.'),
('boundary_curve','Boundary curve','Defines the closed path around which circulation is measured.','Represents the loop edge or system boundary where circulation is interpreted.','The curve must be the boundary of the selected surface.'),
('orientation_consistency','Orientation consistency','Links surface normal and boundary direction by the right-hand rule.','Determines sign for rotational interpretation.','Orientation errors can reverse the conclusion.'),
('curl_computation','Curl computation','Defines how local rotational structure is computed.','Supports comparison between local rotation and boundary circulation.','Finite-difference curl estimates may amplify noise.'),
('sampling_resolution','Sampling resolution','Defines boundary segments and surface patches.','Shapes numerical comparison between line and surface estimates.','Coarse sampling can make theorem comparisons misleading.');

CREATE TABLE stokes_theorem_audit_cases (
    scenario TEXT NOT NULL,
    radius REAL NOT NULL,
    boundary_segments INTEGER NOT NULL,
    radial_steps INTEGER NOT NULL,
    boundary_circulation REAL NOT NULL,
    surface_curl_flux REAL NOT NULL,
    absolute_gap REAL NOT NULL,
    field_description TEXT NOT NULL,
    surface_description TEXT NOT NULL,
    orientation_note TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO stokes_theorem_audit_cases VALUES
('coarse_audit',1.0,32,8,6.242890,6.283185,0.040295,'F=<-y,x,0>; curl F=<0,0,2>','horizontal disk with upward normal','counterclockwise boundary orientation viewed from positive z','Coarse boundary or surface sampling; refine before interpreting the theorem comparison.'),
('medium_audit',1.0,128,32,6.280662,6.283185,0.002523,'F=<-y,x,0>; curl F=<0,0,2>','horizontal disk with upward normal','counterclockwise boundary orientation viewed from positive z','Synthetic Stokes theorem audit; document field surface boundary orientation units and numerical method.'),
('fine_audit',1.0,512,128,6.283027,6.283185,0.000158,'F=<-y,x,0>; curl F=<0,0,2>','horizontal disk with upward normal','counterclockwise boundary orientation viewed from positive z','Synthetic Stokes theorem audit; document field surface boundary orientation units and numerical method.');
