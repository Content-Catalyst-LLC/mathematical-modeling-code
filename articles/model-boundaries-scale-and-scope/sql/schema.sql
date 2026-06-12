-- Boundary, scale, and scope governance schema.

DROP TABLE IF EXISTS scope_matrix;
DROP TABLE IF EXISTS scenario_parameter;
DROP TABLE IF EXISTS boundary_register;
DROP TABLE IF EXISTS boundary_type;
DROP TABLE IF EXISTS model_scope_statement;

CREATE TABLE boundary_type (
    boundary_type TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    typical_failure TEXT NOT NULL
);

CREATE TABLE boundary_register (
    boundary_id INTEGER PRIMARY KEY,
    boundary_key TEXT NOT NULL,
    boundary_type TEXT NOT NULL,
    included TEXT NOT NULL,
    excluded TEXT NOT NULL,
    risk_if_excluded TEXT NOT NULL,
    review_question TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('active', 'review', 'revise', 'archive')),
    FOREIGN KEY (boundary_type) REFERENCES boundary_type(boundary_type)
);

CREATE TABLE scenario_parameter (
    scenario TEXT PRIMARY KEY,
    boundary_version TEXT NOT NULL,
    initial_stock REAL NOT NULL CHECK (initial_stock >= 0),
    capacity REAL NOT NULL CHECK (capacity > 0),
    inflow REAL NOT NULL CHECK (inflow >= 0),
    demand REAL NOT NULL CHECK (demand >= 0),
    loss_rate REAL NOT NULL CHECK (loss_rate >= 0),
    policy_savings REAL NOT NULL CHECK (policy_savings >= 0),
    periods INTEGER NOT NULL CHECK (periods > 0),
    description TEXT
);

CREATE TABLE scope_matrix (
    scope_id INTEGER PRIMARY KEY,
    scope_type TEXT NOT NULL,
    supported_use TEXT NOT NULL,
    unsupported_or_prohibited_use TEXT NOT NULL,
    validation_needed TEXT NOT NULL
);

CREATE TABLE model_scope_statement (
    statement_id INTEGER PRIMARY KEY,
    supported_use TEXT NOT NULL,
    exploratory_use TEXT NOT NULL,
    prohibited_use TEXT NOT NULL,
    evidence_required_for_expansion TEXT NOT NULL
);

INSERT INTO boundary_type VALUES
('physical', 'Material or spatial system limits.', 'Physical process outside the boundary drives outputs.'),
('temporal', 'Start, end, and time horizon.', 'Delayed or long-term effects are missed.'),
('spatial', 'Location, geometry, adjacency, or region.', 'Local variation or spillovers are hidden.'),
('population', 'Who or what is included.', 'Subgroup outcomes disappear.'),
('mechanism', 'Processes represented explicitly.', 'Important mechanisms are hidden inside parameters.'),
('data', 'Evidence available to the model.', 'Unobserved or biased data define the model world.'),
('decision', 'Choices and consequences included in the decision frame.', 'Model output overreaches its decision scope.'),
('uncertainty', 'Unknowns represented in the model.', 'Risk is understated or mischaracterized.');

INSERT INTO boundary_register(boundary_key, boundary_type, included, excluded, risk_if_excluded, review_question, status) VALUES
('physical_stock_boundary', 'physical', 'storage inflow demand losses capacity', 'spatial distribution quality local access', 'Local shortages or quality limits may be hidden.', 'Does aggregate storage match the intended use?', 'active'),
('uncertainty_boundary', 'uncertainty', 'scenario inflow and demand values', 'probabilistic inflow demand variability extreme events', 'Shortage risk may be understated.', 'Should uncertain drivers be represented probabilistically?', 'review'),
('policy_boundary', 'decision', 'policy savings as a demand reduction', 'implementation capacity compliance enforcement equity', 'Policy performance may be overstated.', 'Are institutional constraints inside the model boundary?', 'review'),
('time_horizon_boundary', 'temporal', '60-period planning horizon', 'long-term infrastructure change and regime shifts', 'Long-term fragility may be missed.', 'Does the time horizon match the decision horizon?', 'review'),
('population_boundary', 'population', 'aggregate users', 'user groups access differences vulnerable populations', 'Distributional effects may be hidden.', 'Are subgroup outputs needed before decision use?', 'review');

INSERT INTO scenario_parameter VALUES
('narrow_baseline','narrow_stock_flow',80,100,8,6,0.015,0,60,'Narrow conceptual stock-flow model'),
('low_inflow_boundary_test','uncertainty_expanded',80,100,5,6,0.015,0,60,'Boundary test with lower inflow'),
('policy_savings_boundary_test','policy_expanded',80,100,5,6,0.015,1.5,60,'Policy boundary with demand reduction'),
('longer_stress_boundary','temporal_expanded',70,80,5,7,0.030,0.5,120,'Longer stress boundary'),
('subgroup_visibility_test','population_expanded',60,75,4,6,0.025,0.25,60,'Proxy for subgroup or local stress');

INSERT INTO scope_matrix(scope_type, supported_use, unsupported_or_prohibited_use, validation_needed) VALUES
('conceptual_explanation','Clarify boundary and stock-flow structure','Precise operational forecast','Domain validation and empirical calibration'),
('scenario_exploration','Compare plausible boundary versions','Assign probabilities to scenarios','Probabilistic uncertainty model'),
('short_term_planning','Support bounded-horizon review','Long-term infrastructure certification','Extended horizon validation'),
('policy_support','Inform deliberation with uncertainty','Replace institutional judgment','Stakeholder review and governance process'),
('subgroup_analysis','Screen for distributional visibility','Make equity claims without subgroup data','Disaggregated data and subgroup validation');

INSERT INTO model_scope_statement VALUES
(1, 'Conceptual explanation and first-pass boundary review.', 'Scenario comparison under stated assumptions.', 'Operational forecasting, certification, or distributional claims without further validation.', 'Boundary review, scale review, empirical validation, uncertainty analysis, and scope governance.');
