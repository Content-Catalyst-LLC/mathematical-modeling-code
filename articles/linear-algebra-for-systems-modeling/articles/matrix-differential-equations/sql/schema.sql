DROP TABLE IF EXISTS matrix_differential_assumption_registry;
DROP TABLE IF EXISTS matrix_differential_audit_cases;

CREATE TABLE matrix_differential_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO matrix_differential_assumption_registry VALUES
('state_vector','State vector','Defines the coordinates of continuous-time system state.','Determines what the model can track through time.','State variables require units scales and domain definitions.'),
('system_matrix','System matrix','Maps current state into instantaneous rate of change.','Encodes rate coupling among variables.','Matrix entries are rate parameters and require time-unit clarity.'),
('continuous_time','Continuous-time interpretation','Uses dx/dt = Ax rather than x_next = Ax.','Determines the correct evolution operator and stability rule.','Do not apply discrete-time spectral-radius rules to a continuous-time generator.'),
('matrix_exponential','Matrix exponential','Advances the initial state through continuous time.','Represents the continuous state transition operator.','Numerical computation of exp(At) should use reliable algorithms.'),
('stability','Continuous-time stability','Classifies modes using eigenvalue real parts.','Shows whether disturbances decay persist oscillate or amplify.','Stable eigenvalues do not automatically imply practical safety or desirability.'),
('solver_review','Solver review','Checks numerical integration method step size and stiffness.','Determines whether simulated trajectories are reliable.','Naive time stepping can distort stiff or sensitive continuous systems.');

CREATE TABLE matrix_differential_audit_cases (
    system_name TEXT NOT NULL,
    state_names TEXT NOT NULL,
    system_matrix TEXT NOT NULL,
    initial_state TEXT NOT NULL,
    time_horizon REAL NOT NULL,
    final_state_estimate TEXT NOT NULL,
    initial_norm REAL NOT NULL,
    final_norm REAL NOT NULL,
    eigenvalue_1 REAL NOT NULL,
    eigenvalue_2 REAL NOT NULL,
    max_real_part REAL NOT NULL,
    stability_classification TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO matrix_differential_audit_cases VALUES
('two_state_matrix_differential_equation_audit','infrastructure_stress|service_delay','-0.280000,0.080000;0.120000,-0.340000','10.000000,4.000000',10.0,'1.558000,0.882000',10.770330,1.790000,-0.2,-0.42,-0.2,'asymptotically_stable_continuous_time','Matrix differential equations depend on state definitions units time scale matrix source solver choices stiffness review and domain constraints.');
