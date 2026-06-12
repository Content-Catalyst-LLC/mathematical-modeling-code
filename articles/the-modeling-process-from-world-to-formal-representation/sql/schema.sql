-- Modeling process governance schema.

DROP TABLE IF EXISTS validation_metric;
DROP TABLE IF EXISTS model_run;
DROP TABLE IF EXISTS assumption_register;
DROP TABLE IF EXISTS scenario_parameter;
DROP TABLE IF EXISTS modeling_stage;
DROP TABLE IF EXISTS modeling_question;

CREATE TABLE modeling_question (
    question_id INTEGER PRIMARY KEY,
    article_slug TEXT NOT NULL,
    real_world_context TEXT NOT NULL,
    modeling_purpose TEXT NOT NULL,
    central_question TEXT NOT NULL,
    intended_use TEXT NOT NULL,
    decision_context TEXT NOT NULL
);

CREATE TABLE modeling_stage (
    stage_id INTEGER PRIMARY KEY,
    stage_order INTEGER NOT NULL,
    stage_name TEXT NOT NULL,
    guiding_question TEXT NOT NULL,
    expected_artifact TEXT NOT NULL
);

CREATE TABLE scenario_parameter (
    scenario TEXT PRIMARY KEY,
    initial_storage REAL NOT NULL CHECK (initial_storage >= 0),
    capacity REAL NOT NULL CHECK (capacity > 0),
    base_inflow REAL NOT NULL CHECK (base_inflow >= 0),
    base_demand REAL NOT NULL CHECK (base_demand >= 0),
    demand_growth REAL NOT NULL,
    loss_rate REAL NOT NULL CHECK (loss_rate >= 0),
    periods INTEGER NOT NULL CHECK (periods > 0),
    description TEXT
);

CREATE TABLE assumption_register (
    assumption_id INTEGER PRIMARY KEY,
    assumption_key TEXT NOT NULL,
    statement TEXT NOT NULL,
    role TEXT NOT NULL,
    risk_if_false TEXT NOT NULL,
    sensitivity_test TEXT NOT NULL,
    review_status TEXT NOT NULL CHECK (review_status IN ('active', 'review', 'revise', 'archive'))
);

CREATE TABLE model_run (
    run_id INTEGER PRIMARY KEY,
    scenario TEXT NOT NULL,
    method TEXT NOT NULL,
    output_path TEXT NOT NULL,
    run_timestamp TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    review_status TEXT NOT NULL CHECK (review_status IN ('active', 'review', 'revise', 'archive')),
    FOREIGN KEY (scenario) REFERENCES scenario_parameter(scenario)
);

CREATE TABLE validation_metric (
    metric_id INTEGER PRIMARY KEY,
    run_id INTEGER NOT NULL,
    metric_name TEXT NOT NULL,
    metric_value REAL NOT NULL,
    threshold_value REAL,
    pass_fail TEXT CHECK (pass_fail IN ('pass', 'fail', 'review')),
    FOREIGN KEY (run_id) REFERENCES model_run(run_id)
);

INSERT INTO modeling_question(article_slug, real_world_context, modeling_purpose, central_question, intended_use, decision_context) VALUES
('the-modeling-process-from-world-to-formal-representation', 'Reservoir storage under changing inflow demand losses and capacity limits', 'Demonstrate the movement from real-world question to formal representation', 'How does storage evolve under different assumptions?', 'Educational modeling-process demonstration', 'Scenario comparison sensitivity awareness and revision planning');

INSERT INTO modeling_stage(stage_order, stage_name, guiding_question, expected_artifact) VALUES
(1, 'Problem framing', 'What real-world question is the model meant to clarify?', 'Problem statement'),
(2, 'Intended use', 'Will the model explain predict simulate optimize control or support decisions?', 'Use statement'),
(3, 'Boundary selection', 'What is included excluded aggregated or external?', 'Boundary note'),
(4, 'Variable design', 'What quantities change and describe state?', 'Variable table'),
(5, 'Assumption design', 'What simplifications make the model possible?', 'Assumption register'),
(6, 'Formal formulation', 'How are quantities connected mathematically?', 'Equations constraints or algorithms'),
(7, 'Computation', 'What does the model imply under stated assumptions?', 'Scenario outputs'),
(8, 'Assessment', 'Does the model serve its intended purpose?', 'Diagnostics validation and uncertainty notes'),
(9, 'Revision', 'What changes after testing and interpretation?', 'Revision log');

INSERT INTO scenario_parameter VALUES
('baseline',80,100,8,6,0.010,0.015,60,'Reference scenario'),
('dry_inflow',80,100,5,6,0.010,0.015,60,'Lower inflow stress scenario'),
('high_demand_growth',80,100,8,6,0.030,0.015,60,'Higher demand growth scenario'),
('high_losses',80,100,8,6,0.010,0.035,60,'Higher losses scenario'),
('expanded_capacity',95,130,8,6,0.010,0.015,60,'Expanded capacity scenario');

INSERT INTO assumption_register(assumption_key, statement, role, risk_if_false, sensitivity_test, review_status) VALUES
('fixed_capacity', 'Reservoir capacity is fixed within each scenario', 'Defines storage upper bound', 'Usable storage may change over time', 'Compare capacity scenarios', 'active'),
('deterministic_inflow', 'Inflow is scenario-based rather than stochastic', 'Keeps the first model transparent', 'Shortage risk may be understated', 'Add stochastic inflow ensemble', 'review'),
('constant_demand_growth', 'Demand grows at a constant rate', 'Represents changing pressure', 'Seasonality and conservation behavior may be missed', 'Compare demand scenarios', 'review'),
('proportional_losses', 'Losses are proportional to storage', 'Represents storage-dependent loss', 'Losses may depend on season or infrastructure', 'Compare loss formulations', 'active');
