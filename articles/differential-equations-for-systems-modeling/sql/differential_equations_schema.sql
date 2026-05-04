-- Differential Equations for Systems Modeling schema
-- Stores dynamic model metadata, parameters, simulation runs, outputs, and assumptions.

CREATE TABLE IF NOT EXISTS dynamic_models (
    model_id INTEGER PRIMARY KEY,
    model_name TEXT NOT NULL,
    model_family TEXT NOT NULL,
    equation_description TEXT NOT NULL,
    domain_context TEXT,
    interpretation_note TEXT
);

CREATE TABLE IF NOT EXISTS state_variables (
    variable_id INTEGER PRIMARY KEY,
    model_id INTEGER NOT NULL,
    variable_name TEXT NOT NULL,
    variable_symbol TEXT NOT NULL,
    unit TEXT,
    interpretation_note TEXT,
    FOREIGN KEY (model_id) REFERENCES dynamic_models(model_id)
);

CREATE TABLE IF NOT EXISTS dynamic_parameters (
    parameter_id INTEGER PRIMARY KEY,
    model_id INTEGER NOT NULL,
    parameter_name TEXT NOT NULL,
    parameter_symbol TEXT NOT NULL,
    parameter_value REAL NOT NULL,
    unit TEXT,
    interpretation_note TEXT,
    FOREIGN KEY (model_id) REFERENCES dynamic_models(model_id)
);

CREATE TABLE IF NOT EXISTS simulation_runs (
    run_id INTEGER PRIMARY KEY,
    model_id INTEGER NOT NULL,
    run_name TEXT NOT NULL,
    solver_method TEXT NOT NULL,
    dt REAL,
    steps INTEGER,
    scenario_note TEXT,
    FOREIGN KEY (model_id) REFERENCES dynamic_models(model_id)
);

CREATE TABLE IF NOT EXISTS simulation_outputs (
    output_id INTEGER PRIMARY KEY,
    run_id INTEGER NOT NULL,
    time_value REAL NOT NULL,
    variable_name TEXT NOT NULL,
    variable_value REAL NOT NULL,
    FOREIGN KEY (run_id) REFERENCES simulation_runs(run_id)
);

CREATE TABLE IF NOT EXISTS model_assumptions (
    assumption_id INTEGER PRIMARY KEY,
    model_id INTEGER NOT NULL,
    assumption_text TEXT NOT NULL,
    confidence REAL,
    impact_if_wrong REAL,
    testing_method TEXT,
    FOREIGN KEY (model_id) REFERENCES dynamic_models(model_id)
);

INSERT INTO dynamic_models
(model_id, model_name, model_family, equation_description, domain_context, interpretation_note)
VALUES
(1, 'Logistic Growth Teaching Model', 'ordinary differential equation', 'dS/dt = rS(1 - S/K)', 'population dynamics and constrained growth', 'Used to demonstrate rates of change, equilibrium, sensitivity, and numerical simulation.'),
(2, 'Predator-Prey Teaching Model', 'coupled ordinary differential equations', 'dx/dt = alpha*x - beta*x*y; dy/dt = delta*x*y - gamma*y', 'ecological interaction', 'Used to demonstrate coupled dynamics and oscillatory behavior.'),
(3, 'SIR Teaching Model', 'compartment ordinary differential equations', 'dS/dt = -beta*S*I/N; dI/dt = beta*S*I/N - gamma*I; dR/dt = gamma*I', 'epidemiological systems', 'Used to demonstrate compartment modeling and dynamic transmission.');
