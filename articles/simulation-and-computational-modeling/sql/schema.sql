-- Simulation and computational modeling governance schema.

DROP TABLE IF EXISTS simulation_component_guide;
DROP TABLE IF EXISTS simulation_scenario;
DROP TABLE IF EXISTS simulation_model_register;
DROP TABLE IF EXISTS simulation_component_type;

CREATE TABLE simulation_component_type (
    component_type TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    typical_failure TEXT NOT NULL
);

CREATE TABLE simulation_model_register (
    record_id INTEGER PRIMARY KEY,
    record_key TEXT NOT NULL,
    component_type TEXT NOT NULL,
    computational_structure TEXT NOT NULL,
    interpretation TEXT NOT NULL,
    review_question TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('active', 'review', 'revise', 'archive')),
    FOREIGN KEY (component_type) REFERENCES simulation_component_type(component_type)
);

CREATE TABLE simulation_scenario (
    scenario TEXT PRIMARY KEY,
    initial_stock REAL NOT NULL CHECK (initial_stock >= 0),
    growth_rate REAL NOT NULL CHECK (growth_rate >= 0),
    carrying_capacity REAL NOT NULL CHECK (carrying_capacity > 0),
    extraction REAL NOT NULL CHECK (extraction >= 0),
    shock_probability REAL NOT NULL CHECK (shock_probability >= 0 AND shock_probability <= 1),
    shock_fraction REAL NOT NULL CHECK (shock_fraction >= 0 AND shock_fraction <= 1),
    steps INTEGER NOT NULL CHECK (steps > 0),
    replications INTEGER NOT NULL CHECK (replications > 0)
);

CREATE TABLE simulation_component_guide (
    component_type TEXT PRIMARY KEY,
    meaning TEXT NOT NULL,
    example TEXT NOT NULL,
    review_question TEXT NOT NULL
);

INSERT INTO simulation_component_type VALUES
('state','Model quantity tracked over time.','State definition is ambiguous.'),
('update_rule','Rule for moving from one state to the next.','Code diverges from the mathematical specification.'),
('numerical_method','Approximation or solver method.','Step size or solver setting creates artifacts.'),
('scenario_definition','Alternative assumption set.','Scenario framing is biased or undocumented.'),
('stochastic_protocol','Randomness and replication plan.','Single-run storytelling replaces ensemble evidence.'),
('output_metric','Computed result or decision metric.','Output metric does not support the claim.'),
('validation_diagnostic','Credibility check.','Model is not valid for intended use.');

INSERT INTO simulation_model_register(record_key, component_type, computational_structure, interpretation, review_question, status) VALUES
('state_variable','state','resource_stock','The model tracks resource stock over time','Is the stock definition consistent with the modeled system?','review'),
('update_rule','update_rule','R_next = R + growth - extraction - shock','Stock changes through regeneration extraction and stochastic shocks','Does the update rule match the conceptual model?','review'),
('time_step','numerical_method','discrete_annual_step','The model advances in equal time increments','Is the time step appropriate for the process?','review'),
('ensemble_protocol','stochastic_protocol','multiple_random_seeds_per_scenario','Stochastic variation is summarized across replications','Are enough replications used to characterize uncertainty?','active'),
('scenario_comparison','scenario_definition','baseline_high_extraction_adaptive_policy_shock_stress','Scenarios compare alternative assumptions and stress cases','Are scenario definitions transparent and meaningful?','review'),
('decision_metric','output_metric','depletion_probability','The model estimates probability of crossing a depletion threshold','Is this metric appropriate for decision support?','review');

INSERT INTO simulation_scenario VALUES
('baseline',70.0,0.18,100.0,6.0,0.05,0.10,50,60),
('high_extraction',70.0,0.18,100.0,10.0,0.05,0.10,50,60),
('adaptive_policy',70.0,0.18,100.0,6.0,0.05,0.10,50,60),
('shock_stress',70.0,0.18,100.0,6.0,0.15,0.22,50,60);

INSERT INTO simulation_component_guide VALUES
('state','Model quantity tracked over time','resource_stock','Is the state definition valid?'),
('update_rule','Rule for moving from one state to the next','R_next = F(R)','Does code match the equation?'),
('numerical_method','Approximation or solver method','discrete time step','Is the method stable and accurate?'),
('scenario_definition','Alternative assumption set','high extraction','Are scenarios transparent?'),
('stochastic_protocol','Randomness and replication plan','multiple seeds','Are replications sufficient?'),
('output_metric','Computed result or decision metric','depletion probability','Does the output support the decision?'),
('validation_diagnostic','Credibility check','known-case comparison','Is the model valid for the intended purpose?');
