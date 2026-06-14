-- AI-assisted modeling and human judgment governance schema.

DROP TABLE IF EXISTS ai_assisted_modeling_domain_guide;
DROP TABLE IF EXISTS human_judgment_case;
DROP TABLE IF EXISTS ai_assistance_register;
DROP TABLE IF EXISTS ai_role_type;

CREATE TABLE ai_role_type (
    ai_role TEXT PRIMARY KEY,
    appropriate_use TEXT NOT NULL,
    role_boundary TEXT NOT NULL
);

CREATE TABLE ai_assistance_register (
    record_id INTEGER PRIMARY KEY,
    record_key TEXT NOT NULL,
    modeling_stage TEXT NOT NULL,
    ai_role TEXT NOT NULL,
    artifact_type TEXT NOT NULL,
    provenance_required INTEGER NOT NULL,
    human_review_required INTEGER NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('exploratory', 'draft', 'active', 'review', 'revise', 'approved', 'archive', 'retired')),
    FOREIGN KEY (ai_role) REFERENCES ai_role_type(ai_role)
);

CREATE TABLE human_judgment_case (
    case_key TEXT PRIMARY KEY,
    judgment_point TEXT NOT NULL,
    decision_context TEXT NOT NULL,
    evidence_strength REAL NOT NULL,
    uncertainty_level REAL NOT NULL,
    consequence_level REAL NOT NULL,
    automation_bias_risk REAL NOT NULL,
    accountability_clarity REAL NOT NULL
);

CREATE TABLE ai_assisted_modeling_domain_guide (
    area TEXT PRIMARY KEY,
    review_use TEXT NOT NULL,
    typical_artifacts TEXT NOT NULL
);

INSERT INTO ai_role_type VALUES
('idea_generator','Suggest variables mechanisms scenarios and assumptions','Suggestions require evidence and review.'),
('code_assistant','Draft implementation tests and documentation','Generated code must be inspected and reproduced.'),
('diagnostic_aide','Summarize errors sensitivity anomalies and missing checks','Diagnostics require expert interpretation.'),
('documentation_assistant','Draft assumptions limitations and governance records','Documentation must be verified by accountable humans.'),
('review_companion','Generate challenge questions and alternative interpretations','Final review authority remains human.');

INSERT INTO ai_assistance_register(record_key, modeling_stage, ai_role, artifact_type, provenance_required, human_review_required, status) VALUES
('scenario_drafting','scenario_design','idea_generator','scenario_list',1,1,'review'),
('code_generation','computation','code_assistant','model_script',1,1,'review'),
('diagnostic_summary','validation','diagnostic_aide','diagnostic_report',1,1,'review'),
('communication_draft','communication','documentation_assistant','public_summary',1,1,'review'),
('governance_template','governance','review_companion','use_limit_statement',1,1,'active');

INSERT INTO human_judgment_case VALUES
('problem_frame','problem framing','public infrastructure stress model',0.72,0.58,0.80,0.45,0.70),
('data_fit','data fitness judgment','using administrative records',0.62,0.66,0.75,0.50,0.65),
('model_use','approved use decision','moving from exploratory to decision support',0.68,0.70,0.88,0.72,0.55),
('public_summary','communication approval','publishing model results',0.76,0.62,0.82,0.60,0.72);

INSERT INTO ai_assisted_modeling_domain_guide VALUES
('problem_framing','Define purpose and modeling boundary','purpose statement stakeholder note AI role policy'),
('data_review','Check data provenance measurement and missingness','data lineage data quality report proxy audit'),
('ai_assistance','Track where AI was used and what it produced','AI use log prompt log candidate artifact register'),
('model_design','Review generated equations code and model structures','model design rationale code review record'),
('validation','Check model logic diagnostics and intended-use evidence','validation checklist test report sensitivity analysis'),
('communication','Review generated summaries for overclaiming and missing uncertainty','communication brief caveat review public summary status'),
('governance','Assign responsibility escalation and use limits','governance card model owner decision owner use-limit statement'),
('monitoring','Track drift error misuse and revision needs','monitoring plan incident log retirement criteria');
