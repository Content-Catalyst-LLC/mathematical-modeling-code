-- Model comparison and selection governance schema.

DROP TABLE IF EXISTS selection_criteria;
DROP TABLE IF EXISTS model_candidate;
DROP TABLE IF EXISTS model_selection_register;
DROP TABLE IF EXISTS selection_layer_type;

CREATE TABLE selection_layer_type (
    selection_layer TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    typical_failure TEXT NOT NULL
);

CREATE TABLE model_selection_register (
    record_id INTEGER PRIMARY KEY,
    record_key TEXT NOT NULL,
    selection_layer TEXT NOT NULL,
    modeling_role TEXT NOT NULL,
    review_question TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('active', 'review', 'revise', 'archive')),
    FOREIGN KEY (selection_layer) REFERENCES selection_layer_type(selection_layer)
);

CREATE TABLE model_candidate (
    model_id TEXT PRIMARY KEY,
    model_family TEXT NOT NULL,
    calibration_rmse REAL NOT NULL,
    validation_rmse REAL NOT NULL,
    parameter_count INTEGER NOT NULL,
    interpretability_score REAL NOT NULL,
    robustness_score REAL NOT NULL,
    decision_relevance_score REAL NOT NULL
);

CREATE TABLE selection_criteria (
    criterion TEXT PRIMARY KEY,
    meaning TEXT NOT NULL,
    selection_role TEXT NOT NULL,
    risk_if_ignored TEXT NOT NULL
);

INSERT INTO selection_layer_type VALUES
('alternatives','Candidate model set and baselines.','Weak candidate set makes selection appear stronger than it is.'),
('generalization','Performance beyond calibration data.','Model is selected despite overfitting.'),
('parsimony','Complexity and parameter burden.','Extra complexity is accepted without evidence.'),
('communication','Interpretability and explainability.','Users cannot understand why the model was selected.'),
('uncertainty','Robustness and sensitivity under assumptions.','Selected model is fragile.'),
('decision_support','Connection between model choice and intended use.','Technical winner does not support the decision.');

INSERT INTO model_selection_register(record_key, selection_layer, modeling_role, review_question, status) VALUES
('candidate_set','alternatives','Defines the models being compared','Are plausible baselines and alternatives included?','review'),
('validation_error','generalization','Compares performance on data not used for fitting','Does the selected model generalize?','active'),
('complexity_penalty','parsimony','Penalizes unnecessary complexity','Is added complexity justified by evidence?','review'),
('interpretability','communication','Assesses whether model behavior can be explained','Can users understand why this model was selected?','review'),
('robustness','uncertainty','Reviews stability under assumptions and stress','Does the preferred model remain credible under uncertainty?','review'),
('decision_relevance','decision_support','Links model selection to the intended use','Does model performance matter for the decision?','review');

INSERT INTO model_candidate VALUES
('baseline_naive','baseline',2.90,3.05,0,0.95,0.72,0.55),
('linear_trend','statistical',1.80,2.10,2,0.88,0.70,0.68),
('logistic_growth','mechanistic',1.25,1.42,3,0.76,0.82,0.86),
('stochastic_shock','stochastic',1.05,1.60,6,0.58,0.88,0.90),
('high_flex_curve','flexible',0.45,2.75,9,0.35,0.40,0.52);

INSERT INTO selection_criteria VALUES
('validation_rmse','Out-of-sample prediction error','Generalization evidence','Model may overfit calibration data'),
('parameter_count','Number of fitted or adjustable parameters','Complexity review','Complexity may appear free'),
('interpretability_score','Ability to explain model behavior','Communication and governance','Users may not understand selected model'),
('robustness_score','Stability under plausible changes','Uncertainty review','Selected model may be fragile'),
('decision_relevance_score','Alignment with intended use','Decision support','Technical winner may not support action'),
('overfit_gap','Validation error minus calibration error','Overfit diagnostic','Flexible models may win on known data only');
