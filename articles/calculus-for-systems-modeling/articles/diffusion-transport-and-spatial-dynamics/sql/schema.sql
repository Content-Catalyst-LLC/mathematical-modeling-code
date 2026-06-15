DROP TABLE IF EXISTS spatial_dynamics_assumption_registry;
DROP TABLE IF EXISTS spatial_audit_cases;

CREATE TABLE spatial_dynamics_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO spatial_dynamics_assumption_registry VALUES
('state_field','State field','Defines the distributed quantity modeled over space and time.','Represents concentration, temperature, density, risk, pressure, or another field.','Field meaning, units, and measurement basis should be explicit.'),
('diffusion_coefficient','Diffusion coefficient','Controls spreading or smoothing strength.','Represents mixing, dispersal, conductivity, permeability, or local spread.','Diffusion should be tied to a plausible mechanism.'),
('transport_velocity','Transport velocity','Controls directional movement through the domain.','Represents flow, wind, current, traffic speed, or directed movement.','Velocity magnitude, direction, and units should be documented.'),
('source_sink_terms','Source and sink terms','Add or remove quantity from the field.','Represent emissions, injection, decay, absorption, recovery, or extraction.','Sources and sinks should be tied to evidence or scenario assumptions.'),
('boundary_condition','Boundary condition','Defines behavior at the domain edge.','Represents inflow, outflow, containment, reflection, absorption, or exchange.','Boundary assumptions can dominate results and should be tested.'),
('grid_and_time_step','Grid and time step','Define numerical approximation resolution.','Control computational stability, detail, cost, and artifact risk.','Stability and grid-refinement checks should be recorded.');

CREATE TABLE spatial_audit_cases (
    scenario TEXT NOT NULL,
    grid_points INTEGER NOT NULL,
    diffusivity REAL NOT NULL,
    velocity REAL NOT NULL,
    dx REAL NOT NULL,
    dt REAL NOT NULL,
    steps INTEGER NOT NULL,
    diffusion_ratio REAL NOT NULL,
    transport_ratio REAL NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO spatial_audit_cases VALUES
('one_dimensional_advection_diffusion_teaching_grid',61,0.08,0.4,1.0,0.2,120,0.016,0.08,'Spatial dynamics depend on field meaning, boundary conditions, grid spacing, time step, and numerical stability.');
