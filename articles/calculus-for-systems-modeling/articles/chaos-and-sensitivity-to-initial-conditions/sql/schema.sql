DROP TABLE IF EXISTS chaos_assumption_registry;
DROP TABLE IF EXISTS chaos_audit_cases;

CREATE TABLE chaos_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO chaos_assumption_registry VALUES
('initial_condition','Initial condition','Defines the starting state of a trajectory.','Determines the baseline path used in sensitivity analysis.','Initial-condition uncertainty should be documented and tested.'),
('perturbation_size','Perturbation size','Defines the small difference between nearby starting states.','Tests whether small uncertainty grows over time.','Different perturbation sizes may reveal different numerical behavior.'),
('nonlinear_update_rule','Nonlinear update rule','Defines how the system evolves from one state to the next.','Represents feedback self-limitation interaction or amplification.','Chaos claims depend on model form and parameter values.'),
('lyapunov_estimate','Lyapunov estimate','Measures average divergence of nearby trajectories.','Supports claims about sensitivity to initial conditions.','Lyapunov estimates depend on burn-in sample length and numerical precision.'),
('forecast_horizon','Forecast horizon','Identifies the time range over which prediction remains useful.','Supports responsible communication of prediction limits.','Forecast horizons depend on acceptable error and uncertainty growth.'),
('numerical_precision','Numerical precision','Defines computational limits of simulation.','Affects long-run trajectory reproducibility in sensitive systems.','Rounding and solver choices can affect chaotic simulations.');

CREATE TABLE chaos_audit_cases (
    model TEXT NOT NULL,
    r REAL NOT NULL,
    x0 REAL NOT NULL,
    perturbation REAL NOT NULL,
    steps INTEGER NOT NULL,
    burn_in INTEGER NOT NULL,
    sample_steps INTEGER NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO chaos_audit_cases VALUES
('logistic_map',3.9,0.2,0.00000001,100,100,1000,'Trajectory divergence depends on parameter value, initial uncertainty, numerical precision, and iteration count.');
