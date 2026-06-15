DROP TABLE IF EXISTS greens_theorem_assumption_registry;
DROP TABLE IF EXISTS greens_theorem_audit_cases;

CREATE TABLE greens_theorem_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO greens_theorem_assumption_registry VALUES
('vector_field_definition','Vector field definition','Defines P and Q in the planar vector field.','Determines what flow movement force or tendency means.','Green''s theorem is not interpretable without a meaningful vector field.'),
('closed_boundary','Closed boundary','Defines the curve C that encloses region R.','Represents the system boundary threshold district patch or region edge.','The boundary must match the region used in the area integral.'),
('positive_orientation','Positive orientation','Defines the sign convention for circulation.','Determines whether boundary movement is counted as positive or negative.','Reversing orientation reverses circulation sign.'),
('curl_or_divergence_form','Curl or divergence form','Specifies whether circulation form or flux form is being used.','Separates loop movement from boundary crossing.','Flux and circulation forms answer different modeling questions.'),
('sampling_resolution','Sampling resolution','Defines boundary segments and interior grid cells.','Shapes numerical comparison between boundary and interior estimates.','Coarse sampling can make theorem-side comparisons misleading.'),
('boundary_region_match','Boundary-region match','Links the curve to the area it encloses.','Ensures the theorem compares the same system boundary and interior.','Mismatched geometry invalidates interpretation.');

CREATE TABLE greens_theorem_audit_cases (
    scenario TEXT NOT NULL,
    boundary_segments_per_side INTEGER NOT NULL,
    interior_grid_step REAL NOT NULL,
    boundary_circulation REAL NOT NULL,
    interior_curl_integral REAL NOT NULL,
    boundary_flux REAL NOT NULL,
    interior_divergence_integral REAL NOT NULL,
    circulation_gap REAL NOT NULL,
    flux_gap REAL NOT NULL,
    field_description TEXT NOT NULL,
    region_description TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO greens_theorem_audit_cases VALUES
('coarse_audit',8,0.5,8.0,8.0,8.0,8.0,0.0,0.0,'circulation F=<-y,x>; flux G=<x,y>','positively oriented square [-1,1] x [-1,1]','Coarse boundary or interior sampling; refine before interpreting the theorem comparison.'),
('medium_audit',32,0.25,8.0,8.0,8.0,8.0,0.0,0.0,'circulation F=<-y,x>; flux G=<x,y>','positively oriented square [-1,1] x [-1,1]','Synthetic Green''s theorem audit; document field region orientation units and numerical method.'),
('fine_audit',128,0.125,8.0,8.0,8.0,8.0,0.0,0.0,'circulation F=<-y,x>; flux G=<x,y>','positively oriented square [-1,1] x [-1,1]','Synthetic Green''s theorem audit; document field region orientation units and numerical method.');
