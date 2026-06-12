-- Modeling governance and reproducibility schema for "What Is Mathematical Modeling?"

DROP TABLE IF EXISTS model_runs;
DROP TABLE IF EXISTS scenario_parameters;
DROP TABLE IF EXISTS validation_metrics;
DROP TABLE IF EXISTS model_assumptions;
DROP TABLE IF EXISTS decision_records;

CREATE TABLE model_assumptions (
    assumption_id INTEGER PRIMARY KEY,
    article_slug TEXT NOT NULL,
    assumption_text TEXT NOT NULL,
    risk_if_false TEXT NOT NULL,
    review_status TEXT NOT NULL CHECK (review_status IN ('active', 'review', 'revise', 'archive'))
);

CREATE TABLE scenario_parameters (
    scenario TEXT PRIMARY KEY,
    initial_state REAL NOT NULL CHECK (initial_state >= 0),
    growth_rate REAL NOT NULL,
    carrying_capacity REAL NOT NULL CHECK (carrying_capacity > 0),
    time_step REAL NOT NULL CHECK (time_step > 0),
    steps INTEGER NOT NULL CHECK (steps > 0),
    description TEXT
);

CREATE TABLE model_runs (
    run_id INTEGER PRIMARY KEY,
    scenario TEXT NOT NULL,
    method TEXT NOT NULL CHECK (method IN ('euler', 'rk4', 'analytical', 'monte_carlo', 'other')),
    run_timestamp TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    output_path TEXT NOT NULL,
    code_version TEXT,
    FOREIGN KEY (scenario) REFERENCES scenario_parameters(scenario)
);

CREATE TABLE validation_metrics (
    metric_id INTEGER PRIMARY KEY,
    run_id INTEGER NOT NULL,
    metric_name TEXT NOT NULL,
    metric_value REAL NOT NULL,
    metric_units TEXT,
    adequacy_threshold REAL,
    pass_fail TEXT CHECK (pass_fail IN ('pass', 'fail', 'review')),
    FOREIGN KEY (run_id) REFERENCES model_runs(run_id)
);

CREATE TABLE decision_records (
    record_id INTEGER PRIMARY KEY,
    decision_title TEXT NOT NULL,
    modeling_choice TEXT NOT NULL,
    rationale TEXT NOT NULL,
    implications TEXT NOT NULL,
    review_date TEXT NOT NULL
);

INSERT INTO model_assumptions(article_slug, assumption_text, risk_if_false, review_status) VALUES
('what-is-mathematical-modeling', 'Growth is bounded by a fixed carrying capacity within each scenario.', 'Model may misrepresent systems with changing capacity or external shocks.', 'active'),
('what-is-mathematical-modeling', 'The state variable is nonnegative and continuous.', 'Discrete, negative, or discontinuous states require another model form.', 'active'),
('what-is-mathematical-modeling', 'Parameters are constant during each run.', 'Time-varying dynamics may be hidden.', 'review');

INSERT INTO scenario_parameters(scenario, initial_state, growth_rate, carrying_capacity, time_step, steps, description) VALUES
('baseline', 10.0, 0.35, 100.0, 0.1, 160, 'Reference bounded-growth scenario'),
('low_growth', 10.0, 0.20, 100.0, 0.1, 160, 'Lower intrinsic growth'),
('high_growth', 10.0, 0.50, 100.0, 0.1, 160, 'Higher intrinsic growth'),
('lower_capacity', 10.0, 0.35, 70.0, 0.1, 160, 'Reduced capacity'),
('higher_capacity', 10.0, 0.35, 140.0, 0.1, 160, 'Expanded capacity');

INSERT INTO decision_records(decision_title, modeling_choice, rationale, implications, review_date) VALUES
('Use logistic growth as opening model', 'Nonlinear bounded-growth differential equation', 'Simple enough to inspect but rich enough to demonstrate assumptions, parameters, numerical methods, and uncertainty.', 'Should not be mistaken for a universal population or engineering model.', '2026-06-11');
