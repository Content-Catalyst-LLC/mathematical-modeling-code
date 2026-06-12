-- State variables and system representation governance schema.

DROP TABLE IF EXISTS variable_role_guide;
DROP TABLE IF EXISTS representation_scenario;
DROP TABLE IF EXISTS state_variable_register;
DROP TABLE IF EXISTS state_type;

CREATE TABLE state_type (
    state_type TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    typical_failure TEXT NOT NULL
);

CREATE TABLE state_variable_register (
    state_id INTEGER PRIMARY KEY,
    state_key TEXT NOT NULL,
    state_type TEXT NOT NULL,
    unit TEXT NOT NULL,
    interpretation TEXT NOT NULL,
    update_role TEXT NOT NULL,
    observability TEXT NOT NULL,
    review_question TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('active', 'review', 'revise', 'archive')),
    FOREIGN KEY (state_type) REFERENCES state_type(state_type)
);

CREATE TABLE representation_scenario (
    scenario TEXT PRIMARY KEY,
    representation TEXT NOT NULL CHECK (representation IN ('storage_only', 'adaptive_demand', 'condition_aware')),
    initial_storage REAL NOT NULL CHECK (initial_storage >= 0),
    initial_demand REAL NOT NULL CHECK (initial_demand >= 0),
    initial_condition REAL NOT NULL CHECK (initial_condition >= 0 AND initial_condition <= 1),
    capacity REAL NOT NULL CHECK (capacity > 0),
    inflow REAL NOT NULL CHECK (inflow >= 0),
    loss_rate REAL NOT NULL CHECK (loss_rate >= 0 AND loss_rate <= 1),
    demand_response REAL NOT NULL CHECK (demand_response >= 0),
    condition_decay REAL NOT NULL CHECK (condition_decay >= 0),
    periods INTEGER NOT NULL CHECK (periods > 0),
    description TEXT
);

CREATE TABLE variable_role_guide (
    role TEXT PRIMARY KEY,
    meaning TEXT NOT NULL,
    example TEXT NOT NULL,
    review_question TEXT NOT NULL
);

INSERT INTO state_type VALUES
('continuous_stock','Accumulated continuous quantity that persists over time.','Stocks are confused with flows or outputs.'),
('adaptive_state','State that changes in response to stress or feedback.','Adaptive behavior is treated as an external input.'),
('latent_condition','Hidden or proxy-observed system condition.','Unobserved state is treated as known.'),
('derived_output','Output calculated from state and inputs.','Output is mistaken for state.'),
('distributed_state','State repeated across nodes agents or regions.','Heterogeneity is hidden by aggregation.');

INSERT INTO state_variable_register(state_key, state_type, unit, interpretation, update_role, observability, review_question, status) VALUES
('storage','continuous_stock','resource_units','Current stored resource','Updated by inflow demand and loss','directly_observed','Does storage remain within capacity and nonnegativity bounds?','active'),
('demand','adaptive_state','resource_units_per_period','Demand that can adapt after shortage','Updated by shortage response logic','partially_observed','Is demand truly stateful or should it be treated as external input?','review'),
('infrastructure_condition','latent_condition','dimensionless_index','Condition of infrastructure supporting storage and delivery','Degrades under stress and affects effective loss','proxy_observed','Is the condition index validated or only assumed?','review'),
('shortage','derived_output','resource_units','Unmet demand after update','Derived from raw next-state balance','reported_output','Is shortage a state output or accumulated backlog?','review');

INSERT INTO representation_scenario VALUES
('storage_only_baseline','storage_only',80,7,1.0,100,6,0.015,0.0,0.0,60,'Minimal storage-only representation'),
('adaptive_demand_stress','adaptive_demand',45,8,1.0,80,4,0.020,0.20,0.0,60,'State representation with adaptive demand'),
('condition_aware_stress','condition_aware',45,8,0.85,80,4,0.020,0.20,0.002,60,'State representation with latent infrastructure condition'),
('high_capacity_storage_only','storage_only',80,7,1.0,150,6,0.015,0.0,0.0,60,'Larger-capacity storage-only comparison');

INSERT INTO variable_role_guide VALUES
('state_variable','Describes current system condition','storage','Does this quantity persist and affect future behavior?'),
('input','External driver or action','rainfall or intervention','Is this controlled observed or assumed?'),
('output','Reported or observed result','shortage or cost','Is this derived or directly observed?'),
('parameter','Fixed or slowly varying value','capacity or loss rate','Is this estimated calibrated assumed or scenario-defined?'),
('decision_variable','Quantity chosen by decision-maker','release amount','Who controls it and under what constraints?'),
('latent_state','Hidden condition inferred from observations','infrastructure condition','Can it be identified from data?'),
('derived_diagnostic','Quantity calculated from state and inputs','overflow or shortage','Is it being mistaken for state?');
