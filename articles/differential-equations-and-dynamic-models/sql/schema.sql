-- Differential equations and dynamic models governance schema.

DROP TABLE IF EXISTS dynamic_component_guide;
DROP TABLE IF EXISTS dynamic_scenario;
DROP TABLE IF EXISTS dynamic_model_register;
DROP TABLE IF EXISTS dynamic_component_type;

CREATE TABLE dynamic_component_type (
    component_type TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    typical_failure TEXT NOT NULL
);

CREATE TABLE dynamic_model_register (
    record_id INTEGER PRIMARY KEY,
    record_key TEXT NOT NULL,
    component_type TEXT NOT NULL,
    expression TEXT NOT NULL,
    interpretation TEXT NOT NULL,
    units_or_domain TEXT NOT NULL,
    review_question TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('active', 'review', 'revise', 'archive')),
    FOREIGN KEY (component_type) REFERENCES dynamic_component_type(component_type)
);

CREATE TABLE dynamic_scenario (
    scenario TEXT PRIMARY KEY,
    initial_storage REAL NOT NULL CHECK (initial_storage >= 0),
    capacity REAL NOT NULL CHECK (capacity > 0),
    inflow_rate REAL NOT NULL CHECK (inflow_rate >= 0),
    demand_rate REAL NOT NULL CHECK (demand_rate >= 0),
    loss_rate REAL NOT NULL CHECK (loss_rate >= 0),
    dt REAL NOT NULL CHECK (dt > 0),
    horizon REAL NOT NULL CHECK (horizon > 0),
    description TEXT
);

CREATE TABLE dynamic_component_guide (
    component_type TEXT PRIMARY KEY,
    meaning TEXT NOT NULL,
    example TEXT NOT NULL,
    review_question TEXT NOT NULL
);

INSERT INTO dynamic_component_type VALUES
('state_variable','Quantity that changes through time.','State definition is vague or not observed.'),
('rate_equation','Equation describing change over time.','Rate law is assumed without mechanism or units.'),
('initial_condition','Starting state for simulation or solution.','Initial state is uncertain or inappropriate.'),
('boundary_condition','Limit or edge condition.','Boundaries are ignored or hidden in code.'),
('parameter','Value shaping dynamic behavior.','Parameter is uncalibrated or transferred carelessly.'),
('numerical_setting','Solver choice or time-step setting.','Numerical artifacts are mistaken for system behavior.'),
('output_diagnostic','Derived behavior summary.','Endpoint values hide trajectory behavior.');

INSERT INTO dynamic_model_register(record_key, component_type, expression, interpretation, units_or_domain, review_question, status) VALUES
('storage','state_variable','S(t)','Current resource storage','resource_units','Is storage directly observed and bounded?','active'),
('storage_rate','rate_equation','dS/dt = I - D - lambda*S','Storage changes through inflow demand and proportional loss','resource_units_per_time','Do all rate terms share consistent units?','active'),
('initial_storage','initial_condition','S(0) = S0','Initial system state','0 <= S0 <= K','How was the initial state measured?','review'),
('nonnegativity_boundary','boundary_condition','S(t) >= 0','Storage cannot be negative','bounded_domain','How is the lower boundary enforced numerically?','review'),
('capacity_boundary','boundary_condition','S(t) <= K','Storage cannot exceed capacity','bounded_domain','Is capacity physical operational or assumed?','review'),
('time_step','numerical_setting','dt','Integration time step','positive_time_increment','Do conclusions change under smaller dt?','review');

INSERT INTO dynamic_scenario VALUES
('baseline',80,100,8,6,0.015,0.25,60,'Baseline resource trajectory'),
('high_demand',80,100,8,10,0.015,0.25,60,'Higher demand dynamic stress scenario'),
('high_loss',80,100,8,6,0.050,0.25,60,'Higher proportional loss scenario'),
('tight_capacity',70,75,8,6,0.015,0.25,60,'Tight capacity boundary scenario'),
('coarse_step_baseline',80,100,8,6,0.015,1.00,60,'Coarser Euler time step comparison');

INSERT INTO dynamic_component_guide VALUES
('state_variable','Quantity that changes through time','S(t)','What system condition is tracked?'),
('rate_equation','Equation for change','dS/dt = I - D - lambda*S','What mechanism creates the rate?'),
('initial_condition','Starting state','S(0) = S0','How was the starting state measured?'),
('boundary_condition','Limit on state','0 <= S <= K','How are boundaries enforced?'),
('parameter','Value shaping dynamics','lambda','Is it calibrated estimated or assumed?'),
('numerical_setting','Computation choice','dt','Does solver choice affect conclusions?'),
('output_diagnostic','Derived result','shortage periods','Does output describe behavior not just endpoint?');
