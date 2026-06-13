-- Uncertainty in mathematical models governance schema.

DROP TABLE IF EXISTS uncertainty_component_guide;
DROP TABLE IF EXISTS uncertain_parameter;
DROP TABLE IF EXISTS uncertainty_register;
DROP TABLE IF EXISTS uncertainty_layer_type;

CREATE TABLE uncertainty_layer_type (
    uncertainty_layer TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    typical_failure TEXT NOT NULL
);

CREATE TABLE uncertainty_register (
    record_id INTEGER PRIMARY KEY,
    record_key TEXT NOT NULL,
    uncertainty_layer TEXT NOT NULL,
    modeling_role TEXT NOT NULL,
    review_question TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('active', 'review', 'revise', 'archive')),
    FOREIGN KEY (uncertainty_layer) REFERENCES uncertainty_layer_type(uncertainty_layer)
);

CREATE TABLE uncertain_parameter (
    parameter_name TEXT PRIMARY KEY,
    low REAL NOT NULL,
    baseline REAL NOT NULL,
    high REAL NOT NULL,
    uncertainty_type TEXT NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE uncertainty_component_guide (
    uncertainty_layer TEXT PRIMARY KEY,
    meaning TEXT NOT NULL,
    example TEXT NOT NULL,
    review_question TEXT NOT NULL
);

INSERT INTO uncertainty_layer_type VALUES
('data','Uncertainty in observations or input values.','Precise outputs are built on weak measurements.'),
('parameter','Uncertainty in estimated or assumed values.','Fitted values are treated as exact.'),
('model_form','Uncertainty about mathematical structure.','The model form is treated as unquestionably correct.'),
('scenario','Uncertainty about future conditions.','Scenario assumptions are treated as predictions.'),
('aleatory','Irreducible variability or randomness.','Natural variation is hidden as deterministic certainty.'),
('decision_support','Uncertainty around thresholds and action.','Uncertainty changes action without disclosure.'),
('governance','Documentation and communication.','Future users cannot see what uncertainty was assessed.');

INSERT INTO uncertainty_register(record_key, uncertainty_layer, modeling_role, review_question, status) VALUES
('measurement_uncertainty','data','Reviews uncertainty in observed or input values','How reliable are the measured inputs?','active'),
('parameter_uncertainty','parameter','Documents plausible parameter ranges','How much do estimated parameters affect outputs?','review'),
('structural_uncertainty','model_form','Reviews uncertainty about the model structure','Could another plausible model form change the conclusion?','review'),
('scenario_uncertainty','scenario','Documents uncertainty about future conditions','Which future assumptions control the result?','review'),
('decision_uncertainty','decision_support','Connects uncertainty to thresholds and action','Could uncertainty reverse the decision?','review');

INSERT INTO uncertain_parameter VALUES
('initial_stock',72.0,80.0,88.0,'measurement','Starting stock estimate'),
('growth_rate',0.04,0.08,0.12,'parameter','Dynamic replenishment rate'),
('carrying_capacity',100.0,120.0,140.0,'structural','System boundary assumption'),
('extraction_rate',0.08,0.12,0.18,'scenario','Policy and behavior driver'),
('shock_intensity',0.00,0.03,0.08,'aleatory','Stress and disturbance term');

INSERT INTO uncertainty_component_guide VALUES
('data','Uncertainty in observations or input values','sensor error','How reliable are the measured inputs?'),
('parameter','Uncertainty in estimated values','growth rate interval','How much do parameters affect outputs?'),
('model_form','Uncertainty about model structure','alternative equations','Would another structure change conclusions?'),
('scenario','Uncertainty about future conditions','policy scenario','Which future assumptions control outcomes?'),
('aleatory','Irreducible variability or randomness','shock intensity','How should variability be represented?'),
('decision_support','Uncertainty around thresholds and action','threshold probability','Could uncertainty reverse the decision?'),
('governance','Documentation and communication','use-limit statement','What uncertainty remains unresolved?');
