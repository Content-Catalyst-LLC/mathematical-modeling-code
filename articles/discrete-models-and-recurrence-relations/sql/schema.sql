-- Discrete models and recurrence relations governance schema.

DROP TABLE IF EXISTS recurrence_component_guide;
DROP TABLE IF EXISTS recurrence_scenario;
DROP TABLE IF EXISTS recurrence_model_register;
DROP TABLE IF EXISTS recurrence_component_type;

CREATE TABLE recurrence_component_type (
    component_type TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    typical_failure TEXT NOT NULL
);

CREATE TABLE recurrence_model_register (
    record_id INTEGER PRIMARY KEY,
    record_key TEXT NOT NULL,
    component_type TEXT NOT NULL,
    expression TEXT NOT NULL,
    interpretation TEXT NOT NULL,
    domain_or_step TEXT NOT NULL,
    review_question TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('active', 'review', 'revise', 'archive')),
    FOREIGN KEY (component_type) REFERENCES recurrence_component_type(component_type)
);

CREATE TABLE recurrence_scenario (
    scenario TEXT PRIMARY KEY,
    initial_storage REAL NOT NULL CHECK (initial_storage >= 0),
    initial_demand REAL NOT NULL CHECK (initial_demand >= 0),
    capacity REAL NOT NULL CHECK (capacity > 0),
    inflow REAL NOT NULL CHECK (inflow >= 0),
    loss_rate REAL NOT NULL CHECK (loss_rate >= 0),
    demand_response REAL NOT NULL CHECK (demand_response >= 0),
    periods INTEGER NOT NULL CHECK (periods > 0),
    adaptive_demand INTEGER NOT NULL CHECK (adaptive_demand IN (0, 1)),
    description TEXT
);

CREATE TABLE recurrence_component_guide (
    component_type TEXT PRIMARY KEY,
    meaning TEXT NOT NULL,
    example TEXT NOT NULL,
    review_question TEXT NOT NULL
);

INSERT INTO recurrence_component_type VALUES
('state_variable','Quantity remembered from step to step.','State definition is vague or not observed.'),
('update_rule','Rule for computing the next state.','Update order or mechanism is hidden.'),
('initial_condition','Starting state for iteration.','Initial state is uncertain or inappropriate.'),
('boundary_rule','Limit or clipping rule for valid state.','Boundary events are hidden by clipping.'),
('parameter','Value shaping recurrence behavior.','Parameter is uncalibrated or transferred carelessly.'),
('output_diagnostic','Derived trajectory behavior summary.','Endpoint values hide stepwise behavior.'),
('step_definition','Meaning and scale of one update.','Step size does not match modeled process.');

INSERT INTO recurrence_model_register(record_key, component_type, expression, interpretation, domain_or_step, review_question, status) VALUES
('storage','state_variable','S_t','Current resource storage at period t','0 <= S_t <= K','Is storage directly observed and bounded?','active'),
('storage_update','update_rule','S[t+1] = min(K max(0 S[t] + I[t] - D[t] - lambda*S[t]))','Storage updates through inflow demand and proportional loss','one_period','Are boundary events reported rather than hidden by clipping?','active'),
('demand_update','update_rule','D[t+1] = max(0 D[t] - alpha*Q[t])','Demand adapts after shortage','one_period','Is demand truly adaptive or should it be external input?','review'),
('initial_storage','initial_condition','S_0','Starting storage','0 <= S_0 <= K','How was the starting state measured?','review'),
('shortage','output_diagnostic','Q[t] = max(0 -raw_next_storage)','Unmet demand before boundary clipping','reported_each_period','Is shortage accumulated reported or clipped away?','review'),
('step_definition','step_definition','t_to_t_plus_1','One discrete update interval','period_or_iteration','What does one step represent?','review');

INSERT INTO recurrence_scenario VALUES
('baseline',80,7,100,6,0.015,0.0,60,0,'Baseline storage recurrence'),
('high_demand',80,10,100,6,0.015,0.0,60,0,'Higher demand recurrence stress scenario'),
('adaptive_demand',45,10,80,4,0.020,0.20,60,1,'Adaptive demand response after shortage'),
('tight_capacity',70,7,75,8,0.015,0.0,60,0,'Tight capacity boundary scenario'),
('rapid_loss',80,7,100,6,0.050,0.0,60,0,'Higher proportional loss scenario');

INSERT INTO recurrence_component_guide VALUES
('state_variable','Quantity remembered from step to step','S_t','What system condition is tracked?'),
('update_rule','Rule for next state','S[t+1] = F(S[t])','What mechanism creates the update?'),
('initial_condition','Starting state','S_0','How was the starting state measured?'),
('boundary_rule','Limit on valid state','0 <= S_t <= K','Are boundary events reported?'),
('parameter','Value shaping recurrence','lambda','Is it calibrated estimated or assumed?'),
('output_diagnostic','Derived behavior summary','shortage periods','Does output describe trajectory behavior?'),
('step_definition','Meaning of one step','month or generation','Does the step match the modeled process?');
