DROP TABLE IF EXISTS responsible_modeling_governance_registry;
DROP TABLE IF EXISTS responsible_modeling_records;

CREATE TABLE responsible_modeling_governance_registry (
    registry_key TEXT PRIMARY KEY,
    registry_name TEXT NOT NULL,
    analytical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO responsible_modeling_governance_registry VALUES
('purpose_record','Purpose record','Documents whether the model is teaching, exploratory, mechanistic, predictive, optimization-oriented, or decision-supportive.','Aligns interpretation with intended use.','A model should not be used for claims outside its stated purpose.'),
('assumption_record','Assumption record','Documents mathematical, empirical, computational, boundary, mechanistic, and normative assumptions.','Makes model dependence visible.','Hidden assumptions can create false confidence.'),
('parameter_record','Parameter record','Documents parameter value, unit, source, range, evidence status, and uncertainty.','Prevents parameter values from becoming unexamined authority.','A parameter value without evidence status is incomplete.'),
('validation_scope','Validation scope','Defines the evidence domain, purpose, and range of model adequacy.','Limits model use to tested or justified domains.','Validation is purpose-specific, not universal.'),
('communication_warning','Communication warning','Flags overprecision, scenario confusion, hidden values, or audience mismatch.','Supports responsible public interpretation.','A model result can be technically correct and still miscommunicated.'),
('claim_boundary','Claim boundary','Defines what the model can and cannot responsibly support.','Prevents overclaiming, scope drift, and unsupported decision authority.','Model conclusions should not exceed evidence, scope, and purpose.');

CREATE TABLE responsible_modeling_records (
    record_id TEXT PRIMARY KEY,
    record_type TEXT NOT NULL,
    record_name TEXT NOT NULL,
    category TEXT NOT NULL,
    permitted_use TEXT NOT NULL,
    prohibited_use TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO responsible_modeling_records VALUES
('purpose_teaching','purpose_record','synthetic_logistic_growth','teaching','illustrates growth saturation and carrying capacity','empirical forecast for a real population','synthetic teaching models should not be communicated as empirical evidence');
INSERT INTO responsible_modeling_records VALUES
('purpose_scenario','purpose_record','scenario_sweep','exploratory','compares behavior across plausible parameter scenarios','single-point prediction','scenario outputs should not be confused with forecasts');
INSERT INTO responsible_modeling_records VALUES
('assumption_growth','assumption_record','continuous_growth','mathematical','smooth approximation for teaching','unqualified real-world continuity claim','smooth model may hide shocks thresholds or discrete events');
INSERT INTO responsible_modeling_records VALUES
('claim_predictive','claim_boundary','predictive','validation','forecasts within validated domain and time horizon','predicts outside validation scope','validation is purpose-specific not universal');
