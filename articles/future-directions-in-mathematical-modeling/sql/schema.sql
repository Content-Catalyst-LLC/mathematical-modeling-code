DROP TABLE IF EXISTS model_lifecycle_checklist;
DROP TABLE IF EXISTS future_modeling_domain_guide;
DROP TABLE IF EXISTS future_modeling_direction;
DROP TABLE IF EXISTS modeling_area_type;

CREATE TABLE modeling_area_type (
    modeling_area TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    governance_risk TEXT NOT NULL
);

CREATE TABLE future_modeling_direction (
    direction_key TEXT PRIMARY KEY,
    direction_name TEXT NOT NULL,
    modeling_area TEXT NOT NULL,
    complexity_relevance REAL NOT NULL,
    technical_maturity REAL NOT NULL,
    governance_need REAL NOT NULL,
    uncertainty_pressure REAL NOT NULL,
    human_judgment_need REAL NOT NULL,
    FOREIGN KEY (modeling_area) REFERENCES modeling_area_type(modeling_area)
);

CREATE TABLE future_modeling_domain_guide (
    area TEXT PRIMARY KEY,
    strategic_use TEXT NOT NULL,
    typical_artifacts TEXT NOT NULL
);

CREATE TABLE model_lifecycle_checklist (
    lifecycle_stage TEXT PRIMARY KEY,
    review_question TEXT NOT NULL,
    artifact TEXT NOT NULL
);

INSERT INTO modeling_area_type VALUES
('model_architecture','Hybrid models and model ensembles.','Combined models can become opaque without modular documentation.'),
('computational_workflow','AI-assisted and automated modeling workflows.','Automation can hide assumptions and create false authority.'),
('operational_modeling','Digital twins and living models.','Operational models can drift or be overused without monitoring.'),
('uncertainty_analysis','Uncertainty-aware workflows and sensitivity analysis.','Hidden uncertainty can undermine model trust.'),
('governance_and_legitimacy','Participatory and public-interest modeling.','Public impact requires legitimacy and contestability.'),
('research_infrastructure','Reproducible modeling infrastructure.','Irreproducible models weaken review and reuse.'),
('causal_prediction','Causal reasoning and machine learning.','Prediction without causal structure can fail under intervention.'),
('decision_support','Scenario modeling and deep uncertainty.','One forecast can mislead long-horizon decisions.');

INSERT INTO future_modeling_direction VALUES
('hybrid_models','Hybrid modeling and model ensembles','model_architecture',0.88,0.70,0.74,0.72,0.80),
('ai_assistance','AI-assisted modeling','computational_workflow',0.82,0.78,0.90,0.76,0.92),
('digital_twins','Digital twins and living models','operational_modeling',0.86,0.75,0.88,0.70,0.84),
('uncertainty_workflows','Uncertainty-aware modeling','uncertainty_analysis',0.90,0.72,0.82,0.92,0.86),
('participatory_modeling','Participatory and public-interest modeling','governance_and_legitimacy',0.78,0.62,0.86,0.68,0.94),
('reproducible_infrastructure','Reproducible modeling infrastructure','research_infrastructure',0.74,0.84,0.76,0.58,0.72),
('causal_ml','Causal reasoning and machine learning','causal_prediction',0.84,0.74,0.80,0.78,0.86),
('scenario_deep_uncertainty','Scenario modeling and deep uncertainty','decision_support',0.92,0.76,0.84,0.95,0.88);

INSERT INTO future_modeling_domain_guide VALUES
('hybrid_modeling','Combine model forms for complex questions','model portfolio architecture diagram model comparison record'),
('ai_assistance','Accelerate modeling while preserving human review','AI use log provenance record human judgment register'),
('digital_twins','Maintain operational links between models and systems','digital twin specification data integrity checklist drift monitor'),
('uncertainty_workflows','Make uncertainty visible across assumptions and scenarios','uncertainty brief sensitivity report scenario library'),
('causal_ml','Connect prediction with intervention reasoning','causal diagram identification note validation under shift'),
('participatory_modeling','Improve legitimacy relevance and boundary review','stakeholder review log boundary critique scenario workshop notes'),
('reproducible_infrastructure','Make modeling auditable rerunnable and maintainable','repository tests metadata environment outputs'),
('model_governance','Assign ownership use limits monitoring and retirement','model card governance card lifecycle protocol');

INSERT INTO model_lifecycle_checklist VALUES
('design','What is the model for and who is affected?','purpose_and_boundary_statement'),
('implementation','Can the workflow be rerun and tested?','repository_tests_environment'),
('validation','What evidence supports intended use?','validation_report'),
('deployment','What use is approved and prohibited?','use_limit_statement'),
('monitoring','How will drift error or misuse be detected?','monitoring_protocol'),
('revision','What evidence triggers update?','revision_trigger_record'),
('retirement','When should the model stop being used?','retirement_criteria');
