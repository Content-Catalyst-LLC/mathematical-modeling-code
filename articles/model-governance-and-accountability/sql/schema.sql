-- Model governance and accountability schema.

DROP TABLE IF EXISTS governance_domain_guide;
DROP TABLE IF EXISTS model_lifecycle_checklist;
DROP TABLE IF EXISTS model_governance_risk_case;
DROP TABLE IF EXISTS model_governance_register;
DROP TABLE IF EXISTS risk_tier_type;

CREATE TABLE risk_tier_type (
    risk_tier TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    review_requirement TEXT NOT NULL
);

CREATE TABLE model_governance_register (
    record_key TEXT PRIMARY KEY,
    model_name TEXT NOT NULL,
    model_purpose TEXT NOT NULL,
    risk_tier TEXT NOT NULL,
    validation_status TEXT NOT NULL,
    use_limit_status TEXT NOT NULL,
    monitoring_status TEXT NOT NULL,
    model_owner TEXT NOT NULL,
    decision_owner TEXT NOT NULL,
    FOREIGN KEY (risk_tier) REFERENCES risk_tier_type(risk_tier)
);

CREATE TABLE model_governance_risk_case (
    case_key TEXT PRIMARY KEY,
    model_name TEXT NOT NULL,
    error_risk REAL NOT NULL,
    uncertainty_level REAL NOT NULL,
    consequence_level REAL NOT NULL,
    scope_misuse_risk REAL NOT NULL,
    accountability_gap REAL NOT NULL
);

CREATE TABLE model_lifecycle_checklist (
    lifecycle_stage TEXT PRIMARY KEY,
    review_question TEXT NOT NULL,
    artifact TEXT NOT NULL
);

CREATE TABLE governance_domain_guide (
    area TEXT PRIMARY KEY,
    governance_use TEXT NOT NULL,
    typical_artifacts TEXT NOT NULL
);

INSERT INTO risk_tier_type VALUES
('low','Low consequence internal or exploratory model.','Basic documentation and owner review.'),
('medium','Model supports operational planning or moderate consequence decisions.','Validation, use limits, and monitoring required.'),
('high','Model affects resources, safety, public systems, or institutional strategy.','Independent review, uncertainty brief, monitoring, and approval required.'),
('critical','Model may affect rights, safety, clinical decisions, automated decisions, or major public consequences.','Formal governance board review, strict use limits, monitoring, incident process, and decision ownership required.');

INSERT INTO model_governance_register VALUES
('infrastructure_risk','Infrastructure risk prioritization model','planning support for repair prioritization','high','validated_with_limits','approved_with_limits','active','infrastructure analytics team','capital planning office'),
('public_health_demand','Public health demand model','scenario planning for service demand','high','review_required','draft','pending','health modeling team','public health operations'),
('supply_chain_resilience','Supply chain resilience model','stress testing supplier dependency','medium','validated_with_limits','approved_with_limits','active','operations research group','procurement leadership'),
('ai_triage_support','AI-assisted triage support model','decision support under clinical review','critical','review_required','not_approved','pending','clinical analytics team','clinical governance board');

INSERT INTO model_governance_risk_case VALUES
('infrastructure_risk','Infrastructure risk prioritization model',0.38,0.56,0.82,0.42,0.24),
('public_health_demand','Public health demand model',0.50,0.68,0.86,0.48,0.32),
('supply_chain_resilience','Supply chain resilience model',0.36,0.52,0.65,0.40,0.22),
('ai_triage_support','AI-assisted triage support model',0.62,0.72,0.95,0.70,0.55);

INSERT INTO model_lifecycle_checklist VALUES
('design','What problem is the model intended to address?','purpose_and_decision_context_statement'),
('data_preparation','Are data sources appropriate documented and lawful to use?','data_lineage_and_quality_report'),
('construction','What assumptions equations parameters and constraints are used?','model_specification_and_assumption_register'),
('testing','Does the implementation match the intended logic?','unit_tests_diagnostics_and_code_review'),
('validation','Is the model fit for its intended use?','validation_report'),
('approval','Who approved the model and under what limits?','approval_and_use_limit_record'),
('deployment','How will users access interpret and apply the model?','deployment_and_communication_plan'),
('monitoring','How will drift misuse or failure be detected?','monitoring_dashboard_and_review_schedule'),
('revision','What evidence triggers recalibration or redesign?','revision_trigger_log'),
('retirement','When should the model stop being used?','retirement_decision_record');

INSERT INTO governance_domain_guide VALUES
('purpose_definition','Define what the model is for and not for','purpose statement use case record decision-context note'),
('ownership','Assign model owner data owner reviewer and decision owner','ownership register accountability card'),
('data_governance','Review data provenance quality access privacy and limits','data lineage report quality checklist'),
('validation','Assess whether the model is fit for intended use','validation report diagnostics sensitivity analysis'),
('use_limits','Specify approved and prohibited uses','use-limit statement approved-domain note'),
('monitoring','Detect drift error misuse incidents and context changes','monitoring dashboard incident log'),
('revision','Update model when evidence or conditions change','revision trigger record change log'),
('retirement','Stop use when evidence is insufficient or context changes','retirement criteria archive note');
