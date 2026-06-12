-- Equations, inequalities, and model logic governance schema.

DROP TABLE IF EXISTS transformation_audit;
DROP TABLE IF EXISTS logic_scenario;
DROP TABLE IF EXISTS formal_statement_register;
DROP TABLE IF EXISTS statement_type;

CREATE TABLE statement_type (
    statement_type TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    typical_failure TEXT NOT NULL
);

CREATE TABLE formal_statement_register (
    statement_id INTEGER PRIMARY KEY,
    statement_key TEXT NOT NULL,
    statement_type TEXT NOT NULL,
    expression TEXT NOT NULL,
    interpretation TEXT NOT NULL,
    domain_or_condition TEXT NOT NULL,
    review_question TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('active', 'review', 'revise', 'archive')),
    FOREIGN KEY (statement_type) REFERENCES statement_type(statement_type)
);

CREATE TABLE logic_scenario (
    scenario TEXT PRIMARY KEY,
    initial_stock REAL NOT NULL CHECK (initial_stock >= 0),
    capacity REAL NOT NULL CHECK (capacity > 0),
    inflow REAL NOT NULL CHECK (inflow >= 0),
    demand REAL NOT NULL CHECK (demand >= 0),
    loss_rate REAL NOT NULL CHECK (loss_rate >= 0 AND loss_rate <= 1),
    low_storage_threshold REAL NOT NULL CHECK (low_storage_threshold >= 0),
    demand_reduction REAL NOT NULL CHECK (demand_reduction >= 0),
    periods INTEGER NOT NULL CHECK (periods > 0),
    description TEXT
);

CREATE TABLE transformation_audit (
    transformation TEXT PRIMARY KEY,
    requirement TEXT NOT NULL,
    risk TEXT NOT NULL,
    review_question TEXT NOT NULL
);

INSERT INTO statement_type VALUES
('equation','Equality relationship such as definition balance update or fitted relation.','Equation status is unclear or overinterpreted.'),
('inequality','Order bound threshold constraint or feasible-region statement.','Constraint source or enforcement is hidden.'),
('definition','Formal definition of derived quantity.','Definition is mistaken for empirical evidence.'),
('domain_rule','Valid-value restriction for variable parameter function or transformation.','Invalid values enter computation.'),
('conditional_logic','If-then rule regime trigger or logic branch.','Policy or threshold logic is hidden.'),
('objective_rule','Optimization objective or priority rule.','Value judgments are hidden as technical form.');

INSERT INTO formal_statement_register(statement_key, statement_type, expression, interpretation, domain_or_condition, review_question, status) VALUES
('storage_balance','equation','S[t+1] = S[t] + I[t] - D[t] - lambda*S[t]','Storage changes through inflow demand and proportional loss','0 <= S[t]; 0 <= lambda <= 1','Are all relevant inflows outflows and losses represented?','active'),
('storage_bounds','inequality','0 <= S[t] <= K','Storage remains nonnegative and no greater than capacity','K > 0','Does clipping hide shortage or overflow?','review'),
('shortage_definition','definition','Q[t] = max(0, D[t] + lambda*S[t] - I[t] - S[t])','Shortage is positive only when demand and loss exceed available resources','Q[t] >= 0','Does shortage measure severity frequency or both?','review'),
('low_storage_rule','conditional_logic','if S[t] < T then D[t+1] = max(0, D[t] - delta)','Demand is reduced when storage falls below threshold','0 <= T <= K','Is the threshold measured assumed or policy-defined?','review'),
('loss_rate_domain','domain_rule','0 <= lambda <= 1','Loss rate is a valid fraction per time step','time step must match rate unit','Does the parameter domain match the model time step?','review');

INSERT INTO logic_scenario VALUES
('baseline_logic',80,100,8,6,0.015,35,0.5,60,'Reference equation and inequality logic scenario'),
('constraint_stress',40,60,3,7,0.050,25,1.0,60,'Stress scenario designed to activate shortage and low-storage logic'),
('tight_capacity',70,75,8,6,0.015,30,0.5,60,'Tight capacity scenario'),
('high_loss_logic',80,100,8,6,0.050,35,0.75,60,'Higher loss-rate domain and sensitivity scenario'),
('high_demand_logic',80,100,8,9,0.015,35,1.0,60,'Higher demand scenario designed to activate shortage logic');

INSERT INTO transformation_audit VALUES
('log_transform','x > 0','Zero or negative values become invalid','Are invalid values excluded or modeled separately?'),
('ratio','denominator != 0','Division by zero or unstable values','Is the denominator bounded away from zero?'),
('squaring','sign may be lost','Extraneous solutions may appear','Are candidate solutions checked in the original equation?'),
('linearization','local approximation range','Model may fail outside local range','What is the valid range of approximation?'),
('constraint_relaxation','penalty reflects intended tradeoff','Hard limit may become negotiable','Is this constraint allowed to be relaxed?'),
('normalization','reference scale is meaningful','Comparison may depend on arbitrary scale','Is the reference scale justified?');
