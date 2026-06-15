DROP TABLE IF EXISTS divergence_theorem_assumption_registry;
DROP TABLE IF EXISTS divergence_theorem_audit_cases;

CREATE TABLE divergence_theorem_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO divergence_theorem_assumption_registry VALUES
('vector_field_definition','Vector field definition','Defines the field used for boundary flux and divergence.','Determines what flow transport force movement or tendency means.','The divergence theorem is not interpretable without a meaningful vector field.'),
('closed_surface','Closed surface','Defines the boundary across which outward flux is measured.','Represents the system boundary control surface envelope or interface.','The surface must fully enclose the volume used in the theorem.'),
('enclosed_volume','Enclosed volume','Defines the region over which divergence is accumulated.','Represents the system interior compartment region or control volume.','The volume must match the closed surface used for boundary flux.'),
('outward_normals','Outward normals','Define positive direction for flux through the boundary.','Determine whether crossing is interpreted as export or import.','Inverted normals can reverse conservation conclusions.'),
('divergence_computation','Divergence computation','Defines how local source-sink behavior is computed.','Supports comparison between interior source balance and boundary exchange.','Finite-difference divergence estimates may amplify noise.'),
('mesh_resolution','Mesh resolution','Defines surface patches and volume cells.','Shapes numerical comparison between boundary and volume estimates.','Coarse meshes can make conservation comparisons misleading.');

CREATE TABLE divergence_theorem_audit_cases (
    scenario TEXT NOT NULL,
    grid_steps INTEGER NOT NULL,
    boundary_flux REAL NOT NULL,
    volume_divergence_integral REAL NOT NULL,
    absolute_gap REAL NOT NULL,
    field_description TEXT NOT NULL,
    volume_description TEXT NOT NULL,
    normal_note TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO divergence_theorem_audit_cases VALUES
('coarse_audit',4,3.0,3.0,0.0,'F=<x,y,z>; divergence = 3','unit cube [0,1] x [0,1] x [0,1]','all six cube faces use outward normals','Coarse grid; refine before interpreting the boundary-volume comparison.'),
('medium_audit',16,3.0,3.0,0.0,'F=<x,y,z>; divergence = 3','unit cube [0,1] x [0,1] x [0,1]','all six cube faces use outward normals','Synthetic divergence theorem audit; document field volume boundary normals units and numerical method.'),
('fine_audit',64,3.0,3.0,0.0,'F=<x,y,z>; divergence = 3','unit cube [0,1] x [0,1] x [0,1]','all six cube faces use outward normals','Synthetic divergence theorem audit; document field volume boundary normals units and numerical method.');
