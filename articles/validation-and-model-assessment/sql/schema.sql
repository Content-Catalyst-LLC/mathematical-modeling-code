-- Validation and model assessment governance schema.

DROP TABLE IF EXISTS validation_threshold;
DROP TABLE IF EXISTS validation_component_guide;
DROP TABLE IF EXISTS validation_observation;
DROP TABLE IF EXISTS validation_register;
DROP TABLE IF EXISTS validation_layer_type;

CREATE TABLE validation_layer_type (
    validation_layer TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    typical_failure TEXT NOT NULL
);

CREATE TABLE validation_register (
    record_id INTEGER PRIMARY KEY,
    record_key TEXT NOT NULL,
    validation_layer TEXT NOT NULL,
    modeling_role TEXT NOT NULL,
    assessment_question TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('active', 'review', 'revise', 'archive')),
    FOREIGN KEY (validation_layer) REFERENCES validation_layer_type(validation_layer)
);

CREATE TABLE validation_observation (
    time INTEGER PRIMARY KEY,
    observed_value REAL NOT NULL,
    predicted_value REAL NOT NULL,
    scenario TEXT NOT NULL
);

CREATE TABLE validation_component_guide (
    validation_layer TEXT PRIMARY KEY,
    meaning TEXT NOT NULL,
    example TEXT NOT NULL,
    review_question TEXT NOT NULL
);

CREATE TABLE validation_threshold (
    purpose TEXT PRIMARY KEY,
    rmse_threshold REAL NOT NULL,
    max_abs_error_threshold REAL NOT NULL,
    classification TEXT NOT NULL
);

INSERT INTO validation_layer_type VALUES
('conceptual','Model structure, assumptions, boundaries, and purpose.','Model fits data but represents the wrong system.'),
('verification','Implementation correctness.','Code does not match the model specification.'),
('evidence','Data quality, provenance, and alignment.','Validation evidence is weak or mismatched.'),
('diagnostics','Post-fit residual and error behavior.','Systematic error is hidden by averages.'),
('generalization','Performance beyond fitting evidence.','Model overfits calibration data.'),
('benchmarking','Comparison to baselines and alternatives.','Complexity is accepted without comparison.'),
('uncertainty','Sensitivity, robustness, and uncertainty review.','Outputs appear more certain than warranted.'),
('decision_support','Fitness for purpose and use limits.','Model is used beyond appropriate scope.');

INSERT INTO validation_register(record_key, validation_layer, modeling_role, assessment_question, status) VALUES
('conceptual_validity','conceptual','Reviews model structure assumptions boundaries and purpose','Does the model represent the intended system well enough?','review'),
('implementation_verification','verification','Checks that code implements the specified model logic','Does the implementation match the model specification?','active'),
('data_validation','evidence','Reviews observations units provenance and alignment','Are validation data relevant and reliable?','review'),
('residual_diagnostics','diagnostics','Examines residuals bias and error patterns','Do residuals show systematic model failure?','active'),
('out_of_sample_assessment','generalization','Tests performance beyond calibration data','Does the model generalize to relevant new evidence?','review'),
('benchmark_comparison','benchmarking','Compares model performance to baselines or external evidence','Does the model outperform simpler or accepted alternatives?','review'),
('uncertainty_review','uncertainty','Reviews sensitivity robustness and uncertainty ranges','Could uncertainty change the model-supported decision?','review'),
('fitness_for_purpose','decision_support','Assesses adequacy for the intended use','Is the model credible enough for the stated purpose?','review');

INSERT INTO validation_observation VALUES
(10,70.1,70.8,'holdout'),
(11,68.9,69.7,'holdout'),
(12,67.4,68.3,'holdout'),
(13,65.8,66.9,'holdout'),
(14,64.2,65.1,'holdout'),
(15,62.1,63.8,'stress'),
(16,60.4,61.3,'stress'),
(17,58.8,59.9,'stress');

INSERT INTO validation_component_guide VALUES
('conceptual','Model structure assumptions boundaries and purpose','assumption review','Does the structure fit the intended use?'),
('verification','Implementation correctness','unit tests','Does code match the specification?'),
('evidence','Data quality provenance and alignment','data validation','Are observations reliable and comparable?'),
('diagnostics','Post-fit error and residual behavior','residual plot','Where does the model fail?'),
('generalization','Performance beyond fitting evidence','holdout test','Does performance transfer?'),
('benchmarking','Comparison to baselines and alternatives','simple baseline','Is complexity justified?'),
('uncertainty','Sensitivity robustness and uncertainty review','scenario matrix','Could uncertainty change conclusions?'),
('decision_support','Fitness for purpose and use limits','assessment card','Is the model adequate for this decision?');

INSERT INTO validation_threshold VALUES
('scenario_screening',1.25,2.00,'adequate_for_scenario_screening'),
('limited_review',2.50,4.00,'limited_use_requires_review'),
('not_adequate',999.00,999.00,'not_adequate_without_revision');
