DROP TABLE IF EXISTS linear_dynamics_assumption_registry;
DROP TABLE IF EXISTS linear_dynamics_audit_cases;

CREATE TABLE linear_dynamics_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO linear_dynamics_assumption_registry VALUES
('state_vector','State vector','Defines the coordinates of system state.','Determines what the model can track over time.','Missing or poorly scaled state variables can distort dynamics.'),
('update_matrix','Update matrix','Maps current state to next state.','Encodes interaction coupling propagation or transition structure.','Matrix entries require units source documentation and validity review.'),
('time_step','Time step','Defines the interval between updates.','Determines the meaning of repeated matrix powers.','A matrix calibrated for one interval should not be reused at another interval without transformation.'),
('linearity','Linearity assumption','Assumes state variables combine through linear relationships.','Simplifies system evolution into matrix multiplication.','Thresholds constraints saturation and feedback can violate linearity.'),
('stability','Stability classification','Uses eigenvalues and spectral radius to classify repeated behavior.','Shows whether modes decay persist or amplify.','Eigenvalue stability does not automatically imply practical safety or desirability.'),
('valid_horizon','Valid horizon','Limits how long repeated updates should be trusted.','Defines the time range for credible simulation or interpretation.','A linear model may be valid locally or temporarily not indefinitely.');

CREATE TABLE linear_dynamics_audit_cases (
    system_name TEXT NOT NULL,
    state_names TEXT NOT NULL,
    update_matrix TEXT NOT NULL,
    initial_state TEXT NOT NULL,
    horizon INTEGER NOT NULL,
    final_state TEXT NOT NULL,
    initial_norm REAL NOT NULL,
    final_norm REAL NOT NULL,
    eigenvalue_1 REAL NOT NULL,
    eigenvalue_2 REAL NOT NULL,
    spectral_radius REAL NOT NULL,
    stability_classification TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO linear_dynamics_audit_cases VALUES
('two_state_linear_dynamics_audit','infrastructure_stress|service_delay','0.820000,0.120000;0.180000,0.760000','10.000000,4.000000',20,'3.626170,3.452104',10.770330,5.006380,0.94,0.64,0.94,'asymptotically_stable_discrete_time','Linear dynamics depend on state definitions units scaling time step matrix validity and whether linearity is structural or approximate.');
