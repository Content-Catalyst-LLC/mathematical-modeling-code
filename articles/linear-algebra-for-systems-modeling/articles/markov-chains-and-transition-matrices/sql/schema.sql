DROP TABLE IF EXISTS markov_assumption_registry;
DROP TABLE IF EXISTS markov_transition_audit_cases;

CREATE TABLE markov_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO markov_assumption_registry VALUES
('state_definitions','State definitions','Define the coordinates of the transition system.','Determine what the model can observe and update.','Ambiguous or incomplete states distort the transition matrix.'),
('transition_orientation','Transition orientation','Specifies row-stochastic or column-stochastic convention.','Determines how state vectors are multiplied by the matrix.','Row-column confusion can transpose the model meaning.'),
('time_step','Time step','Defines the interval for each transition.','Determines whether probabilities are daily monthly annual or otherwise.','Transition probabilities cannot be reused across time scales without transformation.'),
('markov_assumption','Markov assumption','Assumes next state depends on current state rather than full history.','Simplifies state evolution into a transition matrix.','Path dependence memory and hidden variables can violate the assumption.'),
('stationarity','Stationarity','Assumes transition probabilities remain constant over the modeled horizon.','Supports repeated use of the same transition matrix.','Policy changes shocks climate behavior and technology can alter transitions.'),
('steady_state','Steady state','Distribution unchanged by the transition matrix.','Supports long-run composition analysis.','A stable distribution is not automatically desirable equitable or safe.');

CREATE TABLE markov_transition_audit_cases (
    system_name TEXT NOT NULL,
    states TEXT NOT NULL,
    orientation TEXT NOT NULL,
    transition_matrix TEXT NOT NULL,
    initial_distribution TEXT NOT NULL,
    row_sum_error REAL NOT NULL,
    nonnegative INTEGER NOT NULL,
    one_step_distribution TEXT NOT NULL,
    ten_step_distribution TEXT NOT NULL,
    steady_state_estimate TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO markov_transition_audit_cases VALUES
('infrastructure_condition_transition_audit','good|fair|poor','row_stochastic_row_vector_update_pi_next_equals_pi_P','0.820000,0.160000,0.020000;0.100000,0.760000,0.140000;0.030000,0.220000,0.750000','0.600000,0.300000,0.100000',0.0,1,'0.525000,0.346000,0.129000','0.286282,0.478868,0.234850','0.233333,0.488889,0.277778','Transition matrices depend on state definitions time step stationarity data quality and the Markov assumption.');
