DROP TABLE IF EXISTS calibration_governance_registry;
DROP TABLE IF EXISTS calibration_parameter_records;

CREATE TABLE calibration_governance_registry (
    calibration_key TEXT PRIMARY KEY,
    calibration_name TEXT NOT NULL,
    analytical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO calibration_governance_registry VALUES
('calibration_data','Calibration data','Observed or target values used to fit parameters.','Connects model structure to evidence.','Calibration data may be incomplete, biased, noisy, or context-specific.'),
('residuals','Residuals','Differences between observed and predicted values.','Shows where model fit is strong or weak.','Residual patterns should be inspected, not only summarized.'),
('loss_function','Loss function','Aggregates residuals into an optimization objective.','Defines what kind of mismatch the calibration minimizes.','Loss-function choice encodes judgment and should be documented.'),
('parameter_bounds','Parameter bounds','Restrict parameter search to plausible values.','Prevents unrealistic fits and supports interpretability.','Bounds can drive results and should not be hidden.'),
('identifiability_review','Identifiability review','Checks whether data can meaningfully constrain parameters.','Protects against overconfident parameter estimates.','Poor identifiability should narrow claims.'),
('validation_boundary','Validation boundary','Separates fitted behavior from tested generalization.','Clarifies what the calibrated model has and has not demonstrated.','Calibration is not validation.');

CREATE TABLE calibration_parameter_records (
    parameter_name TEXT PRIMARY KEY,
    baseline_value REAL NOT NULL,
    lower_bound REAL NOT NULL,
    upper_bound REAL NOT NULL,
    unit_note TEXT NOT NULL,
    calibration_warning TEXT NOT NULL
);

INSERT INTO calibration_parameter_records VALUES
('growth_rate',0.34,0.22,0.42,'per time unit','Growth-rate estimates depend on data, loss function, and tested range.');
INSERT INTO calibration_parameter_records VALUES
('carrying_capacity',105.0,85.0,125.0,'state units','Capacity estimates should be reviewed with residuals and sensitivity.');
INSERT INTO calibration_parameter_records VALUES
('initial_value',10.0,10.0,10.0,'state units','Fixed parameters should still be documented.');
