-- Probability for Systems Modeling schema
-- Stores probabilistic model metadata, assumptions, parameters, simulation runs, and outputs.

CREATE TABLE IF NOT EXISTS probabilistic_models (
    model_id INTEGER PRIMARY KEY,
    model_name TEXT NOT NULL,
    model_family TEXT NOT NULL,
    purpose TEXT NOT NULL,
    interpretation_note TEXT
);

CREATE TABLE IF NOT EXISTS probability_parameters (
    parameter_id INTEGER PRIMARY KEY,
    model_id INTEGER NOT NULL,
    parameter_name TEXT NOT NULL,
    parameter_value REAL,
    unit TEXT,
    interpretation_note TEXT,
    FOREIGN KEY (model_id) REFERENCES probabilistic_models(model_id)
);

CREATE TABLE IF NOT EXISTS probability_simulation_runs (
    run_id INTEGER PRIMARY KEY,
    model_id INTEGER NOT NULL,
    scenario_id TEXT NOT NULL,
    method TEXT NOT NULL,
    iterations INTEGER,
    random_seed INTEGER,
    interpretation_note TEXT,
    FOREIGN KEY (model_id) REFERENCES probabilistic_models(model_id)
);

CREATE TABLE IF NOT EXISTS probability_outputs (
    output_id INTEGER PRIMARY KEY,
    run_id INTEGER NOT NULL,
    output_name TEXT NOT NULL,
    output_value REAL,
    output_unit TEXT,
    FOREIGN KEY (run_id) REFERENCES probability_simulation_runs(run_id)
);

CREATE TABLE IF NOT EXISTS probability_assumptions (
    assumption_id INTEGER PRIMARY KEY,
    model_id INTEGER NOT NULL,
    assumption_text TEXT NOT NULL,
    confidence REAL,
    impact_if_wrong REAL,
    testing_method TEXT,
    FOREIGN KEY (model_id) REFERENCES probabilistic_models(model_id)
);

CREATE TABLE IF NOT EXISTS markov_transition_probabilities (
    transition_id INTEGER PRIMARY KEY,
    model_id INTEGER NOT NULL,
    from_state TEXT NOT NULL,
    to_state TEXT NOT NULL,
    probability REAL NOT NULL,
    interpretation_note TEXT,
    FOREIGN KEY (model_id) REFERENCES probabilistic_models(model_id)
);

INSERT INTO probabilistic_models
(model_id, model_name, model_family, purpose, interpretation_note)
VALUES
(1, 'Monte Carlo System Loss Model', 'Monte Carlo simulation', 'Estimate distribution of uncertain system loss.', 'Educational example for uncertainty analysis and tail risk.'),
(2, 'Beta-Binomial Updating Model', 'Bayesian updating', 'Update uncertain event probability after observations.', 'Educational example for posterior belief revision.'),
(3, 'Infrastructure State Markov Model', 'Markov chain', 'Simulate probabilistic transitions among stable, stressed, and failed states.', 'Educational example for state transition modeling.');
