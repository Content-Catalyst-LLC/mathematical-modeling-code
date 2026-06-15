DROP TABLE IF EXISTS phase_space_assumption_registry;
DROP TABLE IF EXISTS phase_portrait_audit_cases;

CREATE TABLE phase_space_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO phase_space_assumption_registry VALUES
('state_space_range','State-space range','Defines the domain shown in the phase line or phase plane.','Determines which system states are treated as relevant or meaningful.','A phase portrait can mislead if important regions are cropped or invalid regions are shown.'),
('vector_field','Vector field','Assigns a derivative vector to each state-space point.','Shows the local direction and speed of system change.','Vector-field arrows depend on equations parameters scaling and grid resolution.'),
('nullclines','Nullclines','Identify where one component of motion is zero.','Reveal directional boundaries and equilibrium candidates.','Nullclines require domain checks and parameter documentation.'),
('trajectory_selection','Trajectory selection','Chooses initial conditions for simulated paths.','Shows possible histories through state space.','Selected trajectories may overrepresent some outcomes and hide others.'),
('stability_classification','Stability classification','Labels local behavior near equilibria.','Supports interpretation of recovery instability spirals cycles or thresholds.','Local stability labels should not be treated as global guarantees.'),
('solver_method','Solver method','Defines how trajectories are approximated computationally.','Supports reproducible phase-portrait construction.','Step size and solver choice can distort phase behavior.');

CREATE TABLE phase_portrait_audit_cases (
    scenario TEXT NOT NULL,
    alpha REAL NOT NULL,
    beta REAL NOT NULL,
    delta REAL NOT NULL,
    gamma REAL NOT NULL,
    x_min REAL NOT NULL,
    x_max REAL NOT NULL,
    y_min REAL NOT NULL,
    y_max REAL NOT NULL,
    grid_step_x REAL NOT NULL,
    grid_step_y REAL NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO phase_portrait_audit_cases VALUES
('predator_prey_phase_plane',0.7,0.05,0.02,0.5,0.0,60.0,0.0,30.0,5.0,3.0,'Vector-field values depend on parameter values, state ranges, scaling, and the assumed interaction structure.');
