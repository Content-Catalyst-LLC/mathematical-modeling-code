-- Robustness, fragility, and model dependence governance schema.

DROP TABLE IF EXISTS dependence_component_guide;
DROP TABLE IF EXISTS robustness_scenario;
DROP TABLE IF EXISTS robustness_register;
DROP TABLE IF EXISTS dependence_layer_type;

CREATE TABLE dependence_layer_type (
    dependence_layer TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    typical_failure TEXT NOT NULL
);

CREATE TABLE robustness_register (
    record_id INTEGER PRIMARY KEY,
    record_key TEXT NOT NULL,
    dependence_layer TEXT NOT NULL,
    modeling_role TEXT NOT NULL,
    review_question TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('active', 'review', 'revise', 'archive')),
    FOREIGN KEY (dependence_layer) REFERENCES dependence_layer_type(dependence_layer)
);

CREATE TABLE robustness_scenario (
    scenario_key TEXT PRIMARY KEY,
    model_form TEXT NOT NULL,
    scenario TEXT NOT NULL,
    extraction_multiplier REAL NOT NULL,
    shock REAL NOT NULL,
    review_question TEXT NOT NULL
);

CREATE TABLE dependence_component_guide (
    dependence_layer TEXT PRIMARY KEY,
    meaning TEXT NOT NULL,
    example TEXT NOT NULL,
    review_question TEXT NOT NULL
);

INSERT INTO dependence_layer_type VALUES
('parameter','Dependence on values or ranges.','Conclusion reverses under plausible parameter changes.'),
('model_form','Dependence on mathematical structure.','Alternative model forms disagree.'),
('scenario','Dependence on future assumptions.','Recommendation holds only under favorable scenario.'),
('decision_threshold','Dependence on action boundary.','Small output change reverses decision.'),
('data','Dependence on sample, calibration window, or preprocessing.','Result does not transfer across contexts.'),
('metric','Dependence on evaluation criterion.','Model ranking changes by metric.'),
('governance','Documentation and communication.','Hidden dependence creates false confidence.');

INSERT INTO robustness_register(record_key, dependence_layer, modeling_role, review_question, status) VALUES
('parameter_dependence','parameter','Reviews whether results depend on plausible parameter ranges','Do parameter changes reverse the conclusion?','review'),
('structural_dependence','model_form','Compares alternative mathematical structures','Do plausible model forms disagree?','review'),
('scenario_dependence','scenario','Reviews whether conclusions depend on future assumptions','Does the recommendation hold under stress scenarios?','review'),
('threshold_fragility','decision_threshold','Measures whether small changes reverse action','How close is the output to decision reversal?','review'),
('data_dependence','data','Reviews sensitivity to calibration windows and samples','Does evidence from one context transfer responsibly?','review');

INSERT INTO robustness_scenario VALUES
('linear_baseline','linear_decline','baseline',1.0,0.00,'Does the baseline conclusion hold?'),
('linear_stress','linear_decline','stress',1.25,0.05,'Does linear structure survive stress?'),
('dynamic_baseline','logistic_recovery','baseline',1.0,0.00,'Does recovery change the conclusion?'),
('dynamic_stress','logistic_recovery','stress',1.25,0.05,'Does recovery remain adequate under stress?'),
('threshold_baseline','threshold_shift','baseline',1.0,0.00,'Does threshold behavior change baseline interpretation?'),
('threshold_stress','threshold_shift','stress',1.25,0.05,'Does stress produce threshold fragility?');

INSERT INTO dependence_component_guide VALUES
('parameter','Dependence on values or ranges','growth rate range','Do parameter changes reverse the conclusion?'),
('model_form','Dependence on mathematical structure','linear versus threshold model','Do plausible model forms disagree?'),
('scenario','Dependence on future assumptions','stress scenario','Does the recommendation survive adverse conditions?'),
('decision_threshold','Dependence on action boundary','critical stock threshold','How close is decision reversal?'),
('data','Dependence on sample or calibration window','rolling calibration','Does evidence transfer responsibly?'),
('metric','Dependence on evaluation criterion','RMSE versus tail loss','Does ranking change by metric?'),
('governance','Documentation and communication','use-limit statement','Where is hidden dependence a risk?');
