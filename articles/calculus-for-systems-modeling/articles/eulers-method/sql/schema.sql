DROP TABLE IF EXISTS euler_method_assumption_registry;
DROP TABLE IF EXISTS euler_method_audit_cases;

CREATE TABLE euler_method_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO euler_method_assumption_registry VALUES
('rate_function','Rate function','Defines the differential equation used to compute the slope.','Encodes growth, decay, feedback, forcing, inflow, outflow, or transition behavior.','A numerically accurate simulation can still be misleading if the rate function is poorly specified.'),
('initial_condition','Initial condition','Defines the starting state of the simulation.','Controls the trajectory from the first step onward.','Initial-condition uncertainty should be documented.'),
('step_size','Step size','Defines the finite time interval used in each update.','Controls accuracy, stability, and computational cost.','Step-size sensitivity should be tested.'),
('simulation_horizon','Simulation horizon','Defines how long the iterative update is repeated.','Controls how much error can accumulate.','Long horizons require stronger sensitivity and stability review.'),
('stability_check','Stability check','Evaluates whether numerical behavior remains controlled.','Prevents numerical artifacts from being interpreted as system behavior.','Stability conditions depend on the equation and method.'),
('benchmark_comparison','Benchmark comparison','Compares Euler results to exact solutions or refined numerical estimates when available.','Helps distinguish numerical error from modeled dynamics.','Synthetic benchmarks do not guarantee empirical validity.');

CREATE TABLE euler_method_audit_cases (
    scenario TEXT NOT NULL,
    initial_value REAL NOT NULL,
    decay_rate REAL NOT NULL,
    step_size REAL NOT NULL,
    stop_time REAL NOT NULL,
    stability_multiplier REAL NOT NULL,
    stability_status TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO euler_method_audit_cases VALUES
('exponential_decay_benchmark',100.0,0.35,0.1,20.0,0.965,'stable_for_simple_decay','Euler estimates depend on time step, rate function, initial condition, stability, and accumulated error.');
