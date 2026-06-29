DROP TABLE IF EXISTS long_run_transition_assumption_registry;
DROP TABLE IF EXISTS long_run_transition_audit_cases;

CREATE TABLE long_run_transition_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO long_run_transition_assumption_registry VALUES
('state_space','State space','Defines the coordinates of the transition system.','Determines what can persist converge cycle or absorb.','Long-run behavior is only meaningful if the states are meaningful.'),
('transition_matrix','Transition matrix','Defines the repeated update operator.','Determines how distributions evolve over time.','Repeated powers assume the transition rule remains valid.'),
('stationary_distribution','Stationary distribution','Solves pi P = pi under the row-vector convention.','Represents a distribution unchanged by one transition.','Stationary does not always mean reached from every initial condition.'),
('convergence','Convergence','Describes whether pi_0 P^t approaches a limit.','Supports claims about long-run system composition.','Periodic or reducible systems may not converge simply.'),
('initial_condition_sensitivity','Initial-condition sensitivity','Tests whether different starting distributions produce different outcomes.','Shows whether the system forgets or preserves starting conditions.','Absorbing and reducible systems can preserve path dependence.'),
('practical_horizon','Practical horizon','Compares convergence time with decision time scale.','Determines whether the mathematical long run is operationally relevant.','A limit reached too slowly may not matter for the decision.');

CREATE TABLE long_run_transition_audit_cases (
    system_name TEXT NOT NULL,
    states TEXT NOT NULL,
    orientation TEXT NOT NULL,
    stationary_estimate TEXT NOT NULL,
    distribution_a_after_25_steps TEXT NOT NULL,
    distribution_b_after_25_steps TEXT NOT NULL,
    convergence_distance_a REAL NOT NULL,
    convergence_distance_b REAL NOT NULL,
    initial_condition_gap_after_25_steps REAL NOT NULL,
    row_sum_error REAL NOT NULL,
    nonnegative INTEGER NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO long_run_transition_audit_cases VALUES
('long_run_infrastructure_condition_transition_audit','good|fair|poor','row_stochastic_row_vector_update_pi_next_equals_pi_P','0.233333,0.488889,0.277778','0.236019,0.487126,0.276855','0.231024,0.490132,0.278844',0.005372,0.004064,0.01028,0.0,1,'Long-run behavior depends on state definitions time step stationarity convergence speed closed classes and transition-matrix validity.');
