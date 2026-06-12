-- Assumption and model design governance schema.

DROP TABLE IF EXISTS sensitivity_plan;
DROP TABLE IF EXISTS scenario_parameter;
DROP TABLE IF EXISTS assumption_register;
DROP TABLE IF EXISTS assumption_type;
DROP TABLE IF EXISTS model_design_record;

CREATE TABLE assumption_type (
    assumption_type TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    typical_test TEXT NOT NULL
);

CREATE TABLE assumption_register (
    assumption_id INTEGER PRIMARY KEY,
    assumption_key TEXT NOT NULL,
    statement TEXT NOT NULL,
    assumption_type TEXT NOT NULL,
    role TEXT NOT NULL,
    risk_if_false TEXT NOT NULL,
    sensitivity_test TEXT NOT NULL,
    review_status TEXT NOT NULL CHECK (review_status IN ('active', 'review', 'revise', 'archive')),
    FOREIGN KEY (assumption_type) REFERENCES assumption_type(assumption_type)
);

CREATE TABLE scenario_parameter (
    scenario TEXT PRIMARY KEY,
    initial_stock REAL NOT NULL CHECK (initial_stock >= 0),
    capacity REAL NOT NULL CHECK (capacity > 0),
    inflow REAL NOT NULL CHECK (inflow >= 0),
    demand REAL NOT NULL CHECK (demand >= 0),
    loss_rate REAL NOT NULL CHECK (loss_rate >= 0),
    periods INTEGER NOT NULL CHECK (periods > 0),
    description TEXT
);

CREATE TABLE sensitivity_plan (
    plan_id INTEGER PRIMARY KEY,
    assumption_key TEXT NOT NULL,
    test_name TEXT NOT NULL,
    low_case TEXT,
    high_case TEXT,
    review_priority TEXT NOT NULL CHECK (review_priority IN ('low', 'medium', 'high')),
    FOREIGN KEY (assumption_key) REFERENCES assumption_register(assumption_key)
);

CREATE TABLE model_design_record (
    record_id INTEGER PRIMARY KEY,
    design_choice TEXT NOT NULL,
    rationale TEXT NOT NULL,
    limitation TEXT NOT NULL,
    revision_trigger TEXT NOT NULL
);

INSERT INTO assumption_type VALUES
('abstraction', 'Represents a complex target through a simpler object.', 'Compare aggregate and disaggregated models.'),
('boundary', 'Defines what is inside or outside the model.', 'Boundary critique and scenario expansion.'),
('scale', 'Defines spatial temporal or organizational resolution.', 'Resolution and time-step sensitivity.'),
('functional_form', 'Defines mathematical relationship among variables.', 'Alternative model forms and residual diagnostics.'),
('parameter', 'Defines values that shape model behavior.', 'Calibration uncertainty and parameter sweeps.'),
('uncertainty', 'Defines what randomness or unknowns are represented.', 'Monte Carlo uncertainty propagation.'),
('computational', 'Defines solver algorithm and implementation choices.', 'Verification convergence and regression tests.'),
('interpretive', 'Defines how outputs map to decisions or claims.', 'Decision-context and stakeholder review.');

INSERT INTO assumption_register(assumption_key, statement, assumption_type, role, risk_if_false, sensitivity_test, review_status) VALUES
('aggregate_stock', 'The resource system is represented by one aggregate stock variable.', 'abstraction', 'Keeps the first model interpretable.', 'Spatial subgroup or access differences may be hidden.', 'Compare aggregate and disaggregated versions.', 'review'),
('fixed_capacity', 'Capacity is fixed within each scenario.', 'boundary', 'Defines the upper stock constraint.', 'Operating rules or infrastructure changes may alter usable capacity.', 'Compare lower and higher capacity scenarios.', 'active'),
('deterministic_inflow', 'Inflow is represented as a scenario value rather than a random process.', 'uncertainty', 'Keeps the demonstration deterministic.', 'Shortage risk may be understated.', 'Add low baseline and high inflow scenarios.', 'review'),
('proportional_losses', 'Losses are proportional to current stock.', 'functional_form', 'Provides a simple loss mechanism.', 'Losses may depend on temperature leakage season or surface area.', 'Compare proportional and process-based losses.', 'review'),
('shortage_proxy', 'Shortage periods are used as a risk metric.', 'interpretive', 'Summarizes failure frequency.', 'Severity duration and affected users may be hidden.', 'Compare shortage frequency severity and duration metrics.', 'review');

INSERT INTO scenario_parameter VALUES
('baseline',80,100,8,6,0.015,60,'Reference assumption-aware stock-flow scenario'),
('low_inflow',80,100,5,6,0.015,60,'Lower inflow sensitivity scenario'),
('higher_losses',80,100,8,6,0.035,60,'Higher loss-rate sensitivity scenario'),
('lower_capacity',70,75,8,6,0.015,60,'Lower usable capacity scenario'),
('compound_stress',70,80,5,7,0.030,60,'Combined stress scenario');

INSERT INTO sensitivity_plan(assumption_key, test_name, low_case, high_case, review_priority) VALUES
('fixed_capacity', 'capacity sweep', 'lower_capacity', 'baseline', 'medium'),
('deterministic_inflow', 'inflow sensitivity', 'low_inflow', 'baseline', 'high'),
('proportional_losses', 'loss-rate sensitivity', 'baseline', 'higher_losses', 'high'),
('shortage_proxy', 'metric comparison', 'shortage frequency', 'shortage severity', 'high');

INSERT INTO model_design_record(design_choice, rationale, limitation, revision_trigger) VALUES
('Use aggregate stock-flow model', 'Preserves accumulation and depletion while remaining transparent.', 'May hide spatial and distributional effects.', 'Use disaggregated model if subgroup outcomes matter.'),
('Use deterministic scenarios', 'Keeps first model interpretable.', 'Does not represent probabilistic uncertainty.', 'Add stochastic ensemble if risk estimation is required.');
