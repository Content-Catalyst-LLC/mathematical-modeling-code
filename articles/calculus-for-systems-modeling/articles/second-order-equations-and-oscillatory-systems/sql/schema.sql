DROP TABLE IF EXISTS second_order_assumption_registry;
DROP TABLE IF EXISTS second_order_audit_cases;

CREATE TABLE second_order_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO second_order_assumption_registry VALUES
('state_variable_definition','State variable definition','Defines the quantity governed by the second-order equation.','Determines what the model tracks through position or deviation.','Unclear state definitions make oscillatory behavior uninterpretable.'),
('velocity_state','Velocity or rate state','Represents the first derivative of the state variable.','Captures movement momentum or adjustment speed.','Second-order models require both state and rate initial conditions.'),
('damping_assumption','Damping assumption','Represents velocity-dependent loss or resistance.','Models friction dissipation adjustment cost or institutional resistance.','Damping may not be linear or constant in real systems.'),
('restoring_assumption','Restoring assumption','Represents state-dependent pull toward equilibrium.','Models stiffness correction pressure target seeking or feedback.','Linear restoring force may fail far from equilibrium.'),
('forcing_term','Forcing term','Represents external input shock or periodic driver.','Models demand policy environment load or intervention.','Forcing should be measured estimated or clearly labeled as scenario input.'),
('numerical_method','Numerical method','Defines how the second-order equation is approximated as a first-order system.','Supports reproducible simulation and solver review.','Oscillatory systems are sensitive to step size and solver choice.');

CREATE TABLE second_order_audit_cases (
    scenario TEXT NOT NULL,
    initial_position REAL NOT NULL,
    initial_velocity REAL NOT NULL,
    damping_ratio REAL NOT NULL,
    natural_frequency REAL NOT NULL,
    forcing_amplitude REAL NOT NULL,
    forcing_frequency REAL NOT NULL,
    time_step REAL NOT NULL,
    steps INTEGER NOT NULL,
    method TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO second_order_audit_cases VALUES
('underdamped_unforced',1.0,0.0,0.2,1.0,0.0,1.0,0.02,500,'explicit_euler_first_order_system','Explicit Euler is transparent but can distort oscillatory systems if the step size is too large.'),
('forced_near_resonance',1.0,0.0,0.1,1.0,0.2,1.0,0.02,500,'explicit_euler_first_order_system','External forcing near natural frequency can amplify response.');
