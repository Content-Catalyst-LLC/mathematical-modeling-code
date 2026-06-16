DROP TABLE IF EXISTS runge_kutta_assumption_registry;
DROP TABLE IF EXISTS runge_kutta_audit_cases;

CREATE TABLE runge_kutta_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO runge_kutta_assumption_registry VALUES
('rate_function','Rate function','Defines the differential equation evaluated at each stage.','Encodes growth, decay, feedback, transition, forcing, inflow, or outflow.','A strong numerical method cannot fix a poorly specified rate function.'),
('stage_structure','Stage structure','Defines where slopes are sampled inside the time step.','Controls how the method represents within-step change.','Stage formulas should be documented when methods are implemented manually.'),
('weights','Slope weights','Define how stage slopes are combined into the update.','Determine method order and approximation behavior.','Wrong weights can silently change the numerical method.'),
('step_size','Step size','Defines the time increment used by each solver update.','Controls accuracy, cost, and stability.','Step-size sensitivity should be tested.'),
('stability_review','Stability review','Checks whether the method remains numerically controlled.','Helps prevent solver artifacts from being interpreted as system behavior.','Explicit RK methods can struggle with stiff systems.'),
('benchmark_comparison','Benchmark comparison','Compares RK results to exact, refined, or independently computed solutions.','Helps distinguish numerical error from modeled dynamics.','Synthetic benchmarks do not guarantee empirical validity.');

CREATE TABLE runge_kutta_audit_cases (
    scenario TEXT NOT NULL,
    initial_value REAL NOT NULL,
    decay_rate REAL NOT NULL,
    step_size REAL NOT NULL,
    stop_time REAL NOT NULL,
    method_family TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO runge_kutta_audit_cases VALUES
('euler_vs_rk4_exponential_decay_benchmark',100.0,0.35,0.5,20.0,'Euler and classical RK4','Runge-Kutta estimates depend on rate function, step size, smoothness, stiffness, and benchmark comparison.');
