-- Mathematical modeling in artificial intelligence and data systems governance schema.

DROP TABLE IF EXISTS ai_data_systems_domain_guide;
DROP TABLE IF EXISTS model_candidate;
DROP TABLE IF EXISTS ai_model_register;
DROP TABLE IF EXISTS ai_model_role_type;

CREATE TABLE ai_model_role_type (
    model_role TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    typical_failure TEXT NOT NULL
);

CREATE TABLE ai_model_register (
    record_id INTEGER PRIMARY KEY,
    record_key TEXT NOT NULL,
    model_role TEXT NOT NULL,
    model_family TEXT NOT NULL,
    data_domain TEXT NOT NULL,
    decision_context TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('active', 'review', 'revise', 'archive')),
    FOREIGN KEY (model_role) REFERENCES ai_model_role_type(model_role)
);

CREATE TABLE model_candidate (
    candidate_key TEXT PRIMARY KEY,
    model_name TEXT NOT NULL,
    validation_score REAL NOT NULL,
    calibration_error REAL NOT NULL,
    subgroup_error_gap REAL NOT NULL,
    drift_score REAL NOT NULL,
    interpretability_score REAL NOT NULL,
    privacy_risk REAL NOT NULL,
    deployment_criticality REAL NOT NULL
);

CREATE TABLE ai_data_systems_domain_guide (
    area TEXT PRIMARY KEY,
    modeling_use TEXT NOT NULL,
    typical_model_forms TEXT NOT NULL
);

INSERT INTO ai_model_role_type VALUES
('prediction','Estimates likely outcomes from inputs.','Prediction is mistaken for causal explanation or certainty.'),
('ranking','Orders items, cases, or options by score.','Visibility and opportunity effects are not reviewed.'),
('generation','Produces plausible outputs from prompts or contexts.','Plausibility is mistaken for verification.'),
('monitoring','Tracks drift, incidents, quality, and degradation.','Deployment is treated as the end of modeling.'),
('governance','Documents model purpose, validation, risk, owner, use limits, and accountability.','Decision responsibility is shifted to the model.');

INSERT INTO ai_model_register(record_key, model_role, model_family, data_domain, decision_context, status) VALUES
('prediction_model','prediction','supervised_learning','structured_records','risk scoring with human review','active'),
('ranking_model','ranking','learning_to_rank','recommendation_logs','prioritization and visibility','review'),
('generative_model','generation','language_model','text_corpus','drafting and synthesis support','review'),
('monitoring_model','monitoring','drift_detection','deployment_streams','post-deployment governance','review'),
('governance_model','governance','model_card_and_audit_register','model_lifecycle_records','accountability and review','review');

INSERT INTO model_candidate VALUES
('baseline_logistic','Baseline logistic model',0.76,0.050,0.080,0.120,0.920,0.080,0.62),
('tree_ensemble','Tree ensemble',0.83,0.070,0.140,0.180,0.620,0.130,0.70),
('neural_model','Neural model',0.86,0.095,0.190,0.240,0.380,0.180,0.82),
('constrained_model','Constrained calibrated model',0.81,0.035,0.060,0.100,0.780,0.090,0.66);

INSERT INTO ai_data_systems_domain_guide VALUES
('predictive_analytics','Estimate likely outcomes from structured records','Regression classification ensembles calibrated models'),
('recommendation_systems','Rank and suggest items content actions or pathways','Collaborative filtering learning-to-rank embeddings'),
('generative_systems','Produce plausible text images code audio or structured outputs','Language models diffusion models sequence models'),
('anomaly_detection','Flag unusual patterns for review','Distance models isolation forests autoencoders statistical monitors'),
('monitoring_and_drift','Track deployment changes and model degradation','Drift detection calibration monitoring performance dashboards'),
('model_governance','Document purpose validation risk ownership and use limits','Model cards audit registers risk controls'),
('decision_support','Assist human review without replacing decision authority','Scoring models triage tools constrained optimization'),
('data_infrastructure','Maintain pipeline quality schema stability and reproducibility','Validation checks schemas lineage systems');
