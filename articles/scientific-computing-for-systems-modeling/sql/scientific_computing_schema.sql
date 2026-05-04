-- Scientific Computing for Systems Modeling schema
-- Stores workflow metadata, parameters, runs, outputs, diagnostics, and assumptions.

CREATE TABLE IF NOT EXISTS computational_workflows (
    workflow_id INTEGER PRIMARY KEY,
    workflow_name TEXT NOT NULL,
    workflow_type TEXT NOT NULL,
    purpose TEXT NOT NULL,
    interpretation_note TEXT
);

CREATE TABLE IF NOT EXISTS workflow_parameters (
    parameter_id INTEGER PRIMARY KEY,
    workflow_id INTEGER NOT NULL,
    parameter_name TEXT NOT NULL,
    parameter_value REAL,
    unit TEXT,
    interpretation_note TEXT,
    FOREIGN KEY (workflow_id) REFERENCES computational_workflows(workflow_id)
);

CREATE TABLE IF NOT EXISTS workflow_runs (
    run_id INTEGER PRIMARY KEY,
    workflow_id INTEGER NOT NULL,
    scenario_id TEXT NOT NULL,
    algorithm_name TEXT NOT NULL,
    run_status TEXT NOT NULL,
    created_at TEXT,
    interpretation_note TEXT,
    FOREIGN KEY (workflow_id) REFERENCES computational_workflows(workflow_id)
);

CREATE TABLE IF NOT EXISTS workflow_outputs (
    output_id INTEGER PRIMARY KEY,
    run_id INTEGER NOT NULL,
    output_name TEXT NOT NULL,
    output_value REAL,
    output_unit TEXT,
    FOREIGN KEY (run_id) REFERENCES workflow_runs(run_id)
);

CREATE TABLE IF NOT EXISTS workflow_diagnostics (
    diagnostic_id INTEGER PRIMARY KEY,
    run_id INTEGER NOT NULL,
    diagnostic_name TEXT NOT NULL,
    diagnostic_value REAL,
    interpretation_note TEXT,
    FOREIGN KEY (run_id) REFERENCES workflow_runs(run_id)
);

CREATE TABLE IF NOT EXISTS workflow_assumptions (
    assumption_id INTEGER PRIMARY KEY,
    workflow_id INTEGER NOT NULL,
    assumption_text TEXT NOT NULL,
    confidence REAL,
    impact_if_wrong REAL,
    testing_method TEXT,
    FOREIGN KEY (workflow_id) REFERENCES computational_workflows(workflow_id)
);

INSERT INTO computational_workflows
(workflow_id, workflow_name, workflow_type, purpose, interpretation_note)
VALUES
(1, 'Logistic Simulation Sweep', 'simulation and sensitivity workflow', 'Evaluate dynamic model behavior across parameter values.', 'Educational workflow for scientific computing and systems modeling.'),
(2, 'Numerical Methods Demonstration', 'numerical approximation workflow', 'Demonstrate integration and root-finding methods.', 'Educational workflow for numerical approximation and diagnostics.');
