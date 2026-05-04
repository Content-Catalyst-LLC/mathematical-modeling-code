-- Statistics for Systems Modeling schema
-- Stores statistical model metadata, estimates, diagnostics, and uncertainty intervals.

CREATE TABLE IF NOT EXISTS statistical_models (
    model_id INTEGER PRIMARY KEY,
    model_name TEXT NOT NULL,
    model_family TEXT NOT NULL,
    outcome_name TEXT NOT NULL,
    purpose TEXT NOT NULL,
    interpretation_note TEXT
);

CREATE TABLE IF NOT EXISTS statistical_variables (
    variable_id INTEGER PRIMARY KEY,
    model_id INTEGER NOT NULL,
    variable_name TEXT NOT NULL,
    variable_role TEXT NOT NULL,
    measurement_note TEXT,
    FOREIGN KEY (model_id) REFERENCES statistical_models(model_id)
);

CREATE TABLE IF NOT EXISTS statistical_estimates (
    estimate_id INTEGER PRIMARY KEY,
    model_id INTEGER NOT NULL,
    term TEXT NOT NULL,
    estimate_value REAL NOT NULL,
    standard_error REAL,
    lower_95 REAL,
    upper_95 REAL,
    interpretation_note TEXT,
    FOREIGN KEY (model_id) REFERENCES statistical_models(model_id)
);

CREATE TABLE IF NOT EXISTS model_diagnostics (
    diagnostic_id INTEGER PRIMARY KEY,
    model_id INTEGER NOT NULL,
    diagnostic_name TEXT NOT NULL,
    diagnostic_value REAL NOT NULL,
    interpretation_note TEXT,
    FOREIGN KEY (model_id) REFERENCES statistical_models(model_id)
);

CREATE TABLE IF NOT EXISTS resampling_runs (
    run_id INTEGER PRIMARY KEY,
    model_id INTEGER NOT NULL,
    method TEXT NOT NULL,
    iterations INTEGER NOT NULL,
    target_parameter TEXT NOT NULL,
    interpretation_note TEXT,
    FOREIGN KEY (model_id) REFERENCES statistical_models(model_id)
);

INSERT INTO statistical_models
(model_id, model_name, model_family, outcome_name, purpose, interpretation_note)
VALUES
(1, 'Synthetic Systems Burden Model', 'linear regression', 'system_burden', 'Estimate association among exposure, capacity, governance quality, and system burden.', 'Used for educational examples in estimation, uncertainty, diagnostics, and resampling.');
