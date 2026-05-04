-- Calculus for Systems Modeling schema
-- Stores calculus-based simulation metadata.

CREATE TABLE IF NOT EXISTS calculus_models (
    model_id INTEGER PRIMARY KEY,
    model_name TEXT NOT NULL,
    model_family TEXT NOT NULL,
    equation_description TEXT NOT NULL,
    interpretation_note TEXT
);

CREATE TABLE IF NOT EXISTS calculus_parameters (
    parameter_id INTEGER PRIMARY KEY,
    model_id INTEGER NOT NULL,
    parameter_name TEXT NOT NULL,
    parameter_symbol TEXT NOT NULL,
    parameter_value REAL NOT NULL,
    unit TEXT,
    FOREIGN KEY (model_id) REFERENCES calculus_models(model_id)
);

CREATE TABLE IF NOT EXISTS calculus_simulation_runs (
    run_id INTEGER PRIMARY KEY,
    model_id INTEGER NOT NULL,
    run_name TEXT NOT NULL,
    dt REAL NOT NULL,
    steps INTEGER NOT NULL,
    interpretation_note TEXT,
    FOREIGN KEY (model_id) REFERENCES calculus_models(model_id)
);

CREATE TABLE IF NOT EXISTS calculus_outputs (
    output_id INTEGER PRIMARY KEY,
    run_id INTEGER NOT NULL,
    time REAL NOT NULL,
    state_value REAL NOT NULL,
    derivative_value REAL,
    FOREIGN KEY (run_id) REFERENCES calculus_simulation_runs(run_id)
);

INSERT INTO calculus_models
(model_id, model_name, model_family, equation_description, interpretation_note)
VALUES
(1, 'Logistic Growth Teaching Model', 'ordinary differential equation', 'dS/dt = rS(1 - S/K)', 'Used to demonstrate rates of change, accumulation, numerical simulation, and sensitivity analysis.');
