DROP TABLE IF EXISTS related_rates_assumption_registry;

CREATE TABLE related_rates_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO related_rates_assumption_registry VALUES
('time_dependent_variables','Time-dependent variables','Variables are treated as functions of time.','Clarifies which quantities are changing and which are held fixed.','Forgetting that a variable depends on time produces incorrect derivatives.'),
('model_relationship','Model relationship','A relationship such as y=f(x) or F(x,y)=0 links the variables.','Defines the structure through which rates are converted.','If the relationship is invalid, the inferred rate is invalid.'),
('driving_rate','Driving rate','A known or estimated rate such as dx/dt is supplied.','Identifies the motion that drives the inferred rate.','Noisy or uncertain driving rates propagate into the target rate.'),
('operating_point','Operating point','Derivatives are evaluated at the current state.','Keeps the related-rate claim local and state-specific.','Nonlinear systems may imply different rate conversions at different points.'),
('conditioning','Conditioning','Derivative or Jacobian values determine stability of rate conversion.','Shows whether inferred rates are robust to measurement and model error.','Small denominators or near-singular derivatives can destabilize the inference.');
