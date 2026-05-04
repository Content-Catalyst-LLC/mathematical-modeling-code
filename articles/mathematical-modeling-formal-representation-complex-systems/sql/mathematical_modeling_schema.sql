-- Mathematical Modeling SQL schema
-- Educational schema for models, parameters, assumptions, calibration runs, validation metrics, and simulation outputs.

CREATE TABLE IF NOT EXISTS models (
    model_id INTEGER PRIMARY KEY,
    model_name TEXT NOT NULL,
    model_family TEXT NOT NULL,
    purpose TEXT NOT NULL,
    description TEXT NOT NULL,
    boundary_note TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS model_parameters (
    parameter_id INTEGER PRIMARY KEY,
    model_id INTEGER NOT NULL,
    parameter_name TEXT NOT NULL,
    parameter_symbol TEXT NOT NULL,
    parameter_value REAL,
    unit TEXT,
    interpretation_note TEXT,
    FOREIGN KEY (model_id) REFERENCES models(model_id)
);

CREATE TABLE IF NOT EXISTS model_assumptions (
    assumption_id INTEGER PRIMARY KEY,
    model_id INTEGER NOT NULL,
    assumption_text TEXT NOT NULL,
    confidence REAL NOT NULL,
    impact_if_wrong REAL NOT NULL,
    testing_method TEXT,
    FOREIGN KEY (model_id) REFERENCES models(model_id)
);

CREATE TABLE IF NOT EXISTS simulation_runs (
    run_id INTEGER PRIMARY KEY,
    model_id INTEGER NOT NULL,
    run_name TEXT NOT NULL,
    scenario_name TEXT,
    parameter_set_name TEXT,
    created_at TEXT,
    interpretation_note TEXT,
    FOREIGN KEY (model_id) REFERENCES models(model_id)
);

CREATE TABLE IF NOT EXISTS simulation_outputs (
    output_id INTEGER PRIMARY KEY,
    run_id INTEGER NOT NULL,
    time_step INTEGER,
    output_name TEXT NOT NULL,
    output_value REAL NOT NULL,
    unit TEXT,
    FOREIGN KEY (run_id) REFERENCES simulation_runs(run_id)
);

CREATE TABLE IF NOT EXISTS calibration_results (
    calibration_id INTEGER PRIMARY KEY,
    model_id INTEGER NOT NULL,
    parameter_name TEXT NOT NULL,
    estimated_value REAL NOT NULL,
    objective_value REAL,
    calibration_method TEXT NOT NULL,
    FOREIGN KEY (model_id) REFERENCES models(model_id)
);

CREATE TABLE IF NOT EXISTS validation_metrics (
    validation_id INTEGER PRIMARY KEY,
    model_id INTEGER NOT NULL,
    metric_name TEXT NOT NULL,
    metric_value REAL NOT NULL,
    validation_context TEXT,
    interpretation_note TEXT,
    FOREIGN KEY (model_id) REFERENCES models(model_id)
);

INSERT INTO models
(model_id, model_name, model_family, purpose, description, boundary_note)
VALUES
(1, 'Logistic Growth Teaching Model', 'Dynamic discrete model', 'Education and demonstration', 'Synthetic model for demonstrating simulation, calibration, and sensitivity analysis.', 'Designed for teaching modeling workflows, not for real-world forecasting.');
