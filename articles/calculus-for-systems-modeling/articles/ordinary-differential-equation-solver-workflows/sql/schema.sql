DROP TABLE IF EXISTS ode_solver_assumption_registry;
DROP TABLE IF EXISTS ode_solver_audit_cases;

CREATE TABLE ode_solver_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO ode_solver_assumption_registry VALUES
('rate_function','Rate function','Defines the differential equation passed to the solver.','Encodes the modeled mechanism of continuous change.','A solver cannot correct a poorly specified rate function.'),
('initial_condition','Initial condition','Defines the starting state of the integration.','Controls the trajectory from the first step onward.','Initial-condition uncertainty should be documented.'),
('solver_method','Solver method','Defines the numerical algorithm used to approximate the solution.','Shapes accuracy, stability, cost, and interpretation.','Solver choice should be justified.'),
('tolerances','Tolerances','Control acceptable local error in adaptive methods.','Shape accuracy, runtime, and solver behavior.','Tolerances should be recorded with outputs.'),
('stiffness_review','Stiffness review','Checks whether fast and slow dynamics create solver difficulty.','Helps distinguish system structure from numerical artifact.','Explicit solvers can struggle with stiff systems.'),
('diagnostics','Diagnostics','Record solver status, warnings, errors, and benchmark comparisons.','Support reproducibility and responsible interpretation.','A completed run is not automatically a validated result.');

CREATE TABLE ode_solver_audit_cases (
    scenario TEXT NOT NULL,
    initial_value REAL NOT NULL,
    decay_rate REAL NOT NULL,
    step_size REAL NOT NULL,
    stop_time REAL NOT NULL,
    solver_method TEXT NOT NULL,
    absolute_tolerance REAL NOT NULL,
    relative_tolerance REAL NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO ode_solver_audit_cases VALUES
('fixed_step_rk4_exponential_decay_benchmark',100.0,0.35,0.5,20.0,'fixed_step_rk4',0.00000001,0.000001,'ODE solver outputs depend on equation, initial condition, method, tolerances, step size, stiffness, and diagnostics.');
