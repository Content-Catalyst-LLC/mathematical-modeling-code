-- Calibration, estimation, and parameter fitting governance schema.

DROP TABLE IF EXISTS calibration_component_guide;
DROP TABLE IF EXISTS calibration_observation;
DROP TABLE IF EXISTS parameter_grid;
DROP TABLE IF EXISTS calibration_register;
DROP TABLE IF EXISTS calibration_layer_type;

CREATE TABLE calibration_layer_type (
    calibration_layer TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    typical_failure TEXT NOT NULL
);

CREATE TABLE calibration_register (
    record_id INTEGER PRIMARY KEY,
    record_key TEXT NOT NULL,
    calibration_layer TEXT NOT NULL,
    modeling_role TEXT NOT NULL,
    diagnostic_question TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('active', 'review', 'revise', 'archive')),
    FOREIGN KEY (calibration_layer) REFERENCES calibration_layer_type(calibration_layer)
);

CREATE TABLE calibration_observation (
    time INTEGER PRIMARY KEY,
    observed_stock REAL NOT NULL,
    extraction REAL NOT NULL
);

CREATE TABLE parameter_grid (
    grid_id INTEGER PRIMARY KEY,
    growth_rate_min REAL NOT NULL,
    growth_rate_max REAL NOT NULL,
    growth_rate_step REAL NOT NULL,
    carrying_capacity_min REAL NOT NULL,
    carrying_capacity_max REAL NOT NULL,
    carrying_capacity_step REAL NOT NULL,
    CHECK (growth_rate_min <= growth_rate_max),
    CHECK (carrying_capacity_min <= carrying_capacity_max),
    CHECK (growth_rate_step > 0),
    CHECK (carrying_capacity_step > 0)
);

CREATE TABLE calibration_component_guide (
    calibration_layer TEXT PRIMARY KEY,
    meaning TEXT NOT NULL,
    example TEXT NOT NULL,
    review_question TEXT NOT NULL
);

INSERT INTO calibration_layer_type VALUES
('evidence','Observed or experimental information used for fitting.','Data relevance, measurement error, or scope is unclear.'),
('loss','Formal model-data mismatch criterion.','Objective function is hidden or inappropriate.'),
('parameter_space','Allowed range or structure of parameters.','Bounds shape results invisibly.'),
('optimization','Search method for fitted values.','Numerical method is undocumented or unstable.'),
('diagnostics','Post-fit error review.','Residual structure is ignored.'),
('uncertainty','Parameter and output uncertainty.','Best-fit values are overclaimed.'),
('validation','Credibility beyond calibration data.','Good fit is confused with validation.'),
('governance','Use limits and review status.','Fitted model is used beyond evidence.');

INSERT INTO calibration_register(record_key, calibration_layer, modeling_role, diagnostic_question, status) VALUES
('calibration_data','evidence','Provides observed stock and extraction values for fitting','Are observations aligned with model output and units?','review'),
('objective_function','loss','Uses sum of squared residuals to compare model and evidence','Does squared-error loss match modeling purpose?','review'),
('parameter_bounds','parameter_space','Constrains growth rate and carrying capacity to plausible ranges','Are bounds justified and documented?','review'),
('residual_diagnostics','diagnostics','Checks bias error and residual structure after fitting','Do residuals show systematic model error?','active'),
('validation_split','validation','Separates calibration evidence from holdout evidence','Does the fitted model generalize beyond calibration data?','review'),
('parameter_uncertainty','uncertainty','Preserves plausible ranges and review notes for fitted values','How stable are fitted parameter values?','review');

INSERT INTO calibration_observation VALUES
(0,70.0,5.5),
(1,72.8,5.8),
(2,74.1,6.2),
(3,75.0,6.4),
(4,75.5,6.8),
(5,75.2,7.0),
(6,74.7,7.1),
(7,73.8,7.4),
(8,72.6,7.6),
(9,71.2,7.8);

INSERT INTO parameter_grid(growth_rate_min, growth_rate_max, growth_rate_step, carrying_capacity_min, carrying_capacity_max, carrying_capacity_step)
VALUES (0.08,0.26,0.01,85,125,5);

INSERT INTO calibration_component_guide VALUES
('evidence','Observed or experimental information used for fitting','stock observations','Are data relevant and reliable?'),
('loss','Formal mismatch criterion','sum of squared residuals','Does loss match purpose?'),
('parameter_space','Allowed range or structure of parameters','growth bounds','Are bounds justified?'),
('optimization','Search method for parameter values','grid search','Are settings reproducible?'),
('diagnostics','Post-fit error review','residual table','Are errors systematic?'),
('uncertainty','Parameter and output uncertainty','bootstrap interval','How stable are estimates?'),
('validation','Credibility beyond calibration data','holdout observations','Does model generalize?'),
('governance','Review and use-limit layer','audit card','What should not be inferred?');
