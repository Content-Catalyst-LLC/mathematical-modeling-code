-- Limits, failure, and the ethics of modeling governance schema.

DROP TABLE IF EXISTS model_ethics_domain_guide;
DROP TABLE IF EXISTS model_ethics_risk_case;
DROP TABLE IF EXISTS model_failure_register;
DROP TABLE IF EXISTS model_failure_type;

CREATE TABLE model_failure_type (
    failure_mode TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    typical_harm TEXT NOT NULL
);

CREATE TABLE model_failure_register (
    record_id INTEGER PRIMARY KEY,
    record_key TEXT NOT NULL,
    failure_mode TEXT NOT NULL,
    model_stage TEXT NOT NULL,
    ethical_issue TEXT NOT NULL,
    likely_cause TEXT NOT NULL,
    review_status TEXT NOT NULL CHECK (review_status IN ('active', 'review', 'revise', 'archive')),
    FOREIGN KEY (failure_mode) REFERENCES model_failure_type(failure_mode)
);

CREATE TABLE model_ethics_risk_case (
    case_key TEXT PRIMARY KEY,
    model_name TEXT NOT NULL,
    intended_use TEXT NOT NULL,
    severity REAL NOT NULL,
    likelihood REAL NOT NULL,
    detectability_gap REAL NOT NULL,
    uncertainty_level REAL NOT NULL,
    equity_concern REAL NOT NULL,
    accountability_gap REAL NOT NULL
);

CREATE TABLE model_ethics_domain_guide (
    area TEXT PRIMARY KEY,
    review_use TEXT NOT NULL,
    typical_artifacts TEXT NOT NULL
);

INSERT INTO model_failure_type VALUES
('boundary_failure','Important system effects are excluded.','Hidden consequences or externalized harm.'),
('data_bias','Training or evidence data are unrepresentative.','Unequal error, exclusion, or distorted visibility.'),
('validation_gap','Model is used beyond tested domain.','Unsupported decision authority.'),
('false_precision','Outputs appear more certain than evidence supports.','Overconfidence and weak monitoring.'),
('accountability_gap','No clear owner for decisions or harms.','Responsibility shifting.'),
('scope_creep','Model spreads beyond approved use.','Misuse and unsupported authority.');

INSERT INTO model_failure_register(record_key, failure_mode, model_stage, ethical_issue, likely_cause, review_status) VALUES
('boundary_failure','boundary_failure','design','hidden consequences','narrow boundary or scale choice','review'),
('data_bias','data_bias','data','unequal error and exclusion','measurement selection or historical bias','review'),
('validation_gap','validation_gap','validation','unsupported decision authority','scope creep or weak approval process','review'),
('false_precision','false_precision','communication','overconfidence and public misunderstanding','missing uncertainty communication','review'),
('accountability_gap','accountability_gap','governance','responsibility shifting','missing model owner or decision owner','revise'),
('scope_creep','scope_creep','deployment','misuse and unsupported authority','weak approval and monitoring process','revise');

INSERT INTO model_ethics_risk_case VALUES
('exploratory_model','Exploratory planning model','learning and scenario discussion',0.35,0.35,0.25,0.60,0.30,0.25),
('allocation_model','Resource allocation model','prioritizing scarce resources',0.85,0.55,0.55,0.65,0.75,0.70),
('public_dashboard','Public risk dashboard','communicating population risk',0.70,0.50,0.45,0.80,0.55,0.60),
('automated_score','Automated scoring model','triggering institutional action',0.90,0.60,0.70,0.60,0.80,0.85);

INSERT INTO model_ethics_domain_guide VALUES
('problem_framing','Checks whether the right problem is being modeled','purpose statement stakeholder note decision context'),
('data_review','Checks evidence quality representation and measurement','data provenance missingness report proxy audit'),
('model_design','Checks assumptions boundaries objectives and constraints','assumption log boundary record objective record'),
('validation','Checks evidence for intended use','validation report domain of use stress tests'),
('communication','Checks uncertainty and interpretation','uncertainty brief communication guide dashboard caveats'),
('deployment','Checks approved use monitoring and incident response','approval record monitoring plan incident playbook'),
('equity_review','Checks distributional harm and unequal error','subgroup diagnostics impact review contestability pathway'),
('accountability','Checks model owner decision owner and review process','governance register owner record use-limit statement');
