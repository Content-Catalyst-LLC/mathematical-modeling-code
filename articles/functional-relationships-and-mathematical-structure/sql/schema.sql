-- Functional relationships and mathematical structure governance schema.

DROP TABLE IF EXISTS structure_review_matrix;
DROP TABLE IF EXISTS structure_scenario;
DROP TABLE IF EXISTS relationship_register;
DROP TABLE IF EXISTS relationship_type;

CREATE TABLE relationship_type (
    relationship_type TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    typical_failure TEXT NOT NULL
);

CREATE TABLE relationship_register (
    relationship_id INTEGER PRIMARY KEY,
    relationship_key TEXT NOT NULL,
    relationship_type TEXT NOT NULL,
    expression TEXT NOT NULL,
    interpretation TEXT NOT NULL,
    structural_assumption TEXT NOT NULL,
    review_question TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('active', 'review', 'revise', 'archive')),
    FOREIGN KEY (relationship_type) REFERENCES relationship_type(relationship_type)
);

CREATE TABLE structure_scenario (
    scenario TEXT PRIMARY KEY,
    structure TEXT NOT NULL,
    initial_stock REAL NOT NULL CHECK (initial_stock >= 0),
    capacity REAL NOT NULL CHECK (capacity > 0),
    inflow REAL NOT NULL CHECK (inflow >= 0),
    demand REAL NOT NULL CHECK (demand >= 0),
    loss_rate REAL NOT NULL CHECK (loss_rate >= 0 AND loss_rate <= 1),
    feedback_strength REAL NOT NULL CHECK (feedback_strength >= 0),
    periods INTEGER NOT NULL CHECK (periods > 0),
    description TEXT
);

CREATE TABLE structure_review_matrix (
    structure TEXT PRIMARY KEY,
    appropriate_use TEXT NOT NULL,
    main_risk TEXT NOT NULL,
    diagnostic TEXT NOT NULL
);

INSERT INTO relationship_type VALUES
('linear_dynamic','Linear dynamic update over discrete time.','Linear default may hide nonlinear effects.'),
('bounded_dynamic','Dynamic update with bounds or constraints.','Constraint clipping may hide shortage or overflow.'),
('feedback','Output or state influences future input or state.','Feedback strength or delay may be unsupported.'),
('stochastic','Relationship includes random variation or uncertainty.','Distribution may be unjustified.'),
('threshold','Relationship changes after crossing a boundary.','Threshold may appear falsely precise.'),
('networked','State changes through relationships among connected units.','Aggregate model may hide relational vulnerability.'),
('optimization','Choice under objective and feasible set.','Objective function may hide values.');

INSERT INTO relationship_register(relationship_key, relationship_type, expression, interpretation, structural_assumption, review_question, status) VALUES
('linear_update','linear_dynamic','S[t+1] = S[t] + I[t] - D[t] - lambda*S[t]','Storage changes through inflow demand and proportional loss','Loss is proportional to current storage and demand is exogenous','Does the linear update behave reasonably across the intended domain?','active'),
('constrained_update','bounded_dynamic','S[t+1] = min(K, max(0, raw_next_stock))','Storage is bounded below by zero and above by capacity','Shortage and overflow may be clipped unless tracked separately','Do constraints hide shortage overflow or unmet demand?','review'),
('feedback_demand','feedback','D[t+1] = max(0, D[t] - alpha*shortage[t])','Demand adapts downward when shortage occurs','Shortage produces immediate demand response','Is demand response plausible delayed or institutionally mediated?','review'),
('stochastic_inflow','stochastic','I[t] = I_bar * exp(epsilon[t])','Inflow varies multiplicatively around a baseline','Random inflow shocks are independent and lognormal-like','Is the stochastic structure supported by evidence?','review'),
('threshold_release','threshold','u[t] = u_high if S[t] < T else u_low','Control action changes when storage crosses threshold','A sharp threshold represents a real or policy-defined regime change','Is the threshold measured estimated assumed or policy-defined?','review');

INSERT INTO structure_scenario VALUES
('linear_baseline','linear',80,100,8,6,0.015,0,60,'Unconstrained linear update'),
('constrained_baseline','constrained',80,100,8,6,0.015,0,60,'Bounded stock-flow update'),
('feedback_stress','feedback',40,60,3,7,0.050,0.20,60,'Feedback response under stress'),
('stochastic_inflow','stochastic',70,100,6,6,0.020,0,60,'Random inflow variation around baseline'),
('threshold_case','threshold',50,80,4,7,0.030,0.15,80,'Threshold-oriented stress case');

INSERT INTO structure_review_matrix VALUES
('linear','Local approximation or transparent explanation','Misses nonlinear thresholds saturation or compounding','Compare nonlinear alternative and boundary behavior'),
('constrained','Feasibility and domain enforcement','May hide shortage or overflow if clipped','Track constraint activity and violations separately'),
('feedback','Adaptive system behavior','Feedback strength or delay may be unsupported','Compare no-feedback delayed-feedback and feedback scenarios'),
('stochastic','Uncertain process representation','Distribution may be unjustified','Check uncertainty source and run sensitivity'),
('threshold','Regime-dependent behavior','Threshold may appear more precise than evidence supports','Test threshold range and smooth alternatives');
