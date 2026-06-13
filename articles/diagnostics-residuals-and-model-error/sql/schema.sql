-- Diagnostics, residuals, and model error governance schema.

DROP TABLE IF EXISTS diagnostic_component_guide;
DROP TABLE IF EXISTS diagnostic_observation;
DROP TABLE IF EXISTS diagnostic_register;
DROP TABLE IF EXISTS diagnostic_layer_type;

CREATE TABLE diagnostic_layer_type (
    diagnostic_layer TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    typical_failure TEXT NOT NULL
);

CREATE TABLE diagnostic_register (
    record_id INTEGER PRIMARY KEY,
    record_key TEXT NOT NULL,
    diagnostic_layer TEXT NOT NULL,
    modeling_role TEXT NOT NULL,
    review_question TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('active', 'review', 'revise', 'archive')),
    FOREIGN KEY (diagnostic_layer) REFERENCES diagnostic_layer_type(diagnostic_layer)
);

CREATE TABLE diagnostic_observation (
    time INTEGER PRIMARY KEY,
    diagnostic_group TEXT NOT NULL,
    observed_value REAL NOT NULL,
    predicted_value REAL NOT NULL,
    decision_threshold REAL NOT NULL
);

CREATE TABLE diagnostic_component_guide (
    diagnostic_layer TEXT PRIMARY KEY,
    meaning TEXT NOT NULL,
    example TEXT NOT NULL,
    review_question TEXT NOT NULL
);

INSERT INTO diagnostic_layer_type VALUES
('bias','Directional model error.','Positive and negative errors hide systematic overprediction or underprediction.'),
('decision_support','Error near action thresholds.','Average accuracy hides wrong decision triggers.'),
('subgroup','Context-specific model performance.','Overall metric hides uneven model reliability.'),
('tail_error','Extreme residual behavior.','Rare but consequential cases are ignored.'),
('model_form','Structural model misspecification.','Residual pattern reveals missing structure.'),
('uncertainty','Adequacy of uncertainty communication.','Uncertainty bands do not reflect diagnostic weakness.'),
('governance','Diagnostic documentation and use limits.','Model is used beyond its diagnostic evidence.');

INSERT INTO diagnostic_register(record_key, diagnostic_layer, modeling_role, review_question, status) VALUES
('residual_bias','bias','Reviews directional error across observations','Does the model systematically overpredict or underpredict?','active'),
('threshold_error','decision_support','Reviews residuals near action thresholds','Could residual error change the decision?','review'),
('group_error','subgroup','Compares error across diagnostic groups','Does performance differ across contexts?','review'),
('outlier_review','tail_error','Flags unusually large residuals','Do extreme residuals reveal data or model-form problems?','review'),
('structural_error','model_form','Reviews whether residual patterns suggest missing structure','Is error random or structurally patterned?','review'),
('uncertainty_review','uncertainty','Connects diagnostic evidence to uncertainty communication','Are uncertainty claims adequate for the error pattern?','review');

INSERT INTO diagnostic_observation VALUES
(1,'baseline',82.0,81.5,70.0),
(2,'baseline',79.5,80.2,70.0),
(3,'baseline',77.0,78.4,70.0),
(4,'baseline',74.3,75.6,70.0),
(5,'threshold',71.5,72.8,70.0),
(6,'threshold',69.2,71.0,70.0),
(7,'threshold',67.8,69.8,70.0),
(8,'stress',65.5,68.0,70.0),
(9,'stress',63.0,66.4,70.0),
(10,'stress',61.1,65.2,70.0);

INSERT INTO diagnostic_component_guide VALUES
('bias','Directional model error','mean error','Does error lean positive or negative?'),
('decision_support','Error near action thresholds','threshold disagreement','Could error change a decision?'),
('subgroup','Context-specific model performance','group MAE','Does error differ across groups?'),
('tail_error','Extreme residual behavior','outlier flags','Do rare cases reveal important failure?'),
('model_form','Structural model misspecification','residual pattern','Does error suggest missing structure?'),
('uncertainty','Adequacy of uncertainty communication','interval review','Does uncertainty reflect diagnostic weakness?'),
('governance','Diagnostic documentation and use limits','assessment card','Where should outputs be treated with caution?');
