-- Sensitivity analysis and robustness governance schema.

DROP TABLE IF EXISTS sensitivity_component_guide;
DROP TABLE IF EXISTS sensitivity_parameter;
DROP TABLE IF EXISTS sensitivity_register;
DROP TABLE IF EXISTS sensitivity_layer_type;

CREATE TABLE sensitivity_layer_type (
    sensitivity_layer TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    typical_failure TEXT NOT NULL
);

CREATE TABLE sensitivity_register (
    record_id INTEGER PRIMARY KEY,
    record_key TEXT NOT NULL,
    sensitivity_layer TEXT NOT NULL,
    modeling_role TEXT NOT NULL,
    review_question TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('active', 'review', 'revise', 'archive')),
    FOREIGN KEY (sensitivity_layer) REFERENCES sensitivity_layer_type(sensitivity_layer)
);

CREATE TABLE sensitivity_parameter (
    parameter_name TEXT PRIMARY KEY,
    baseline REAL NOT NULL,
    low REAL NOT NULL,
    high REAL NOT NULL,
    uncertainty_label TEXT NOT NULL
);

CREATE TABLE sensitivity_component_guide (
    sensitivity_layer TEXT PRIMARY KEY,
    meaning TEXT NOT NULL,
    example TEXT NOT NULL,
    review_question TEXT NOT NULL
);

INSERT INTO sensitivity_layer_type VALUES
('local_sensitivity','Small changes near a baseline.','Narrow local checks are mistaken for full robustness.'),
('global_sensitivity','Influence across broad uncertainty ranges.','Interactions and nonlinear effects are missed.'),
('robustness','Stability under plausible variation.','Fragile conclusions are presented as stable.'),
('decision_support','Sensitivity near action thresholds.','Small changes reverse decisions without disclosure.'),
('model_form','Dependence on mathematical structure.','Structural uncertainty is hidden.'),
('data_quality','Evidence priority for influential factors.','High-sensitivity inputs remain poorly measured.'),
('governance','Documentation and communication.','Future users cannot see what was tested.');

INSERT INTO sensitivity_register(record_key, sensitivity_layer, modeling_role, review_question, status) VALUES
('parameter_sweep','local_sensitivity','Varies individual parameters across plausible ranges','Which parameters most influence model output?','active'),
('threshold_fragility','decision_support','Reviews whether outputs cross a decision threshold','Can plausible variation reverse the decision?','review'),
('scenario_stress','robustness','Tests model behavior under adverse scenario conditions','Does the conclusion survive stress assumptions?','review'),
('structural_dependence','model_form','Reviews whether conclusions depend on model structure','Would alternative model forms support the same conclusion?','review'),
('evidence_priority','data_quality','Identifies high-sensitivity inputs that need better evidence','Where would better data most reduce uncertainty?','review');

INSERT INTO sensitivity_parameter VALUES
('initial_stock',80.0,72.0,88.0,'measurement'),
('growth_rate',0.08,0.04,0.12,'parameter'),
('carrying_capacity',120.0,100.0,140.0,'structural'),
('extraction_rate',0.12,0.08,0.18,'policy'),
('shock_intensity',0.03,0.00,0.08,'scenario');

INSERT INTO sensitivity_component_guide VALUES
('local_sensitivity','Small changes near a baseline','one-at-a-time sweep','Which parameter drives output near baseline?'),
('global_sensitivity','Influence across broad uncertainty ranges','sampling-based review','Which factors dominate across plausible uncertainty?'),
('robustness','Stability under plausible variation','stress scenario','Does the conclusion survive disturbance?'),
('decision_support','Sensitivity near action thresholds','threshold crossing','Can uncertainty reverse action?'),
('model_form','Dependence on model structure','alternative model form','Does conclusion survive structural alternatives?'),
('data_quality','Value of better evidence','high-sensitivity input','Where would better data matter most?'),
('governance','Documentation and communication','assessment card','Where is the model robust or fragile?');
