DROP TABLE IF EXISTS domain_rule;
DROP TABLE IF EXISTS model_scenario;

CREATE TABLE domain_rule (
    rule_key TEXT PRIMARY KEY,
    variable_name TEXT NOT NULL,
    lower_bound REAL,
    upper_bound REAL,
    rule_description TEXT NOT NULL
);

CREATE TABLE model_scenario (
    scenario_key TEXT PRIMARY KEY,
    initial_state REAL NOT NULL,
    growth_rate REAL NOT NULL,
    capacity REAL NOT NULL,
    time_horizon REAL NOT NULL,
    interpretation TEXT NOT NULL
);

INSERT INTO domain_rule VALUES
('initial_state_nonnegative','initial_state',0.0,NULL,'Initial state must be nonnegative.'),
('growth_rate_nonnegative','growth_rate',0.0,NULL,'Growth rate must be nonnegative.'),
('capacity_positive','capacity',0.000001,NULL,'Capacity must be positive.'),
('time_horizon_nonnegative','time_horizon',0.0,NULL,'Time horizon must be nonnegative.'),
('initial_state_capacity','initial_state',NULL,NULL,'Initial state should not exceed capacity.');

INSERT INTO model_scenario VALUES
('baseline',10.0,0.20,100.0,20.0,'Valid bounded-growth scenario'),
('near_capacity',95.0,0.20,100.0,20.0,'Valid scenario near output capacity'),
('invalid_negative_state',-5.0,0.20,100.0,20.0,'Invalid because initial state is negative'),
('invalid_capacity',10.0,0.20,0.0,20.0,'Invalid because capacity is nonpositive'),
('outside_capacity',120.0,0.20,100.0,20.0,'Invalid because initial state exceeds capacity'),
('negative_rate',10.0,-0.10,100.0,20.0,'Invalid because rate is negative');
