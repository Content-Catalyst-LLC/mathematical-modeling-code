DROP TABLE IF EXISTS explanation_governance_registry;
DROP TABLE IF EXISTS mechanism_records;

CREATE TABLE explanation_governance_registry (
    registry_key TEXT PRIMARY KEY,
    registry_name TEXT NOT NULL,
    analytical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO explanation_governance_registry VALUES
('mechanism_record','Mechanism record','Documents the process, entities, activities, organization, and evidence status.','Connects formal structure to how a system produces behavior.','A formal model without mechanism documentation may be descriptive only.'),
('formal_representation','Formal representation','Documents equations, variables, parameters, constraints, and computational steps.','Makes model structure explicit and reviewable.','Formal consistency does not guarantee explanatory validity.'),
('parameter_interpretation','Parameter interpretation','Documents parameter source, unit, range, evidence status, and model role.','Prevents fitted constants from being mistaken for causal mechanisms.','Calibrated parameters are not automatically causal quantities.'),
('causal_claim','Causal claim','States whether the model is making a causal or mechanistic assertion.','Separates formal dependence from causal dependence.','Functional dependence does not automatically imply causal explanation.'),
('validation_scope','Validation scope','Defines the evidence domain, purpose, and range of model adequacy.','Aligns model use with evidence and intended purpose.','A model can be valid for one purpose and invalid for another.'),
('claim_boundary','Claim boundary','Defines what kind of explanation, prediction, or decision support is justified.','Prevents formal outputs from being overinterpreted.','Formal structure supports explanation only when mechanism, evidence, and scope are documented.');

CREATE TABLE mechanism_records (
    record_id TEXT PRIMARY KEY,
    mechanism_name TEXT NOT NULL,
    represented_process TEXT NOT NULL,
    evidence_status TEXT NOT NULL,
    claim_type TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO mechanism_records VALUES
('stock_flow','stock_flow_accumulation','stock changes through inflow and outflow','synthetic teaching example','mechanistic','flows must represent real processes');
INSERT INTO mechanism_records VALUES
('feedback','balancing_feedback','state-dependent adjustment limits growth or change','formal teaching example','mechanistic','feedback parameters require process interpretation and evidence');
INSERT INTO mechanism_records VALUES
('threshold','threshold_transition','behavior changes after a critical value is crossed','scenario-based example','exploratory','threshold claims require scope and uncertainty notes');
