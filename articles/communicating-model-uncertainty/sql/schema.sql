-- Communicating model uncertainty governance schema.

DROP TABLE IF EXISTS audience_guide;
DROP TABLE IF EXISTS uncertainty_message;
DROP TABLE IF EXISTS communication_record;
DROP TABLE IF EXISTS communication_layer_type;

CREATE TABLE communication_layer_type (
    communication_layer TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    typical_failure TEXT NOT NULL
);

CREATE TABLE communication_record (
    record_id INTEGER PRIMARY KEY,
    record_key TEXT NOT NULL,
    communication_layer TEXT NOT NULL,
    audience TEXT NOT NULL,
    message_goal TEXT NOT NULL,
    plain_language_statement TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('active', 'review', 'revise', 'archive')),
    FOREIGN KEY (communication_layer) REFERENCES communication_layer_type(communication_layer)
);

CREATE TABLE uncertainty_message (
    message_key TEXT PRIMARY KEY,
    uncertainty_type TEXT NOT NULL,
    technical_statement TEXT NOT NULL,
    plain_language_statement TEXT NOT NULL,
    decision_relevance TEXT NOT NULL
);

CREATE TABLE audience_guide (
    audience TEXT PRIMARY KEY,
    main_need TEXT NOT NULL,
    communication_emphasis TEXT NOT NULL
);

INSERT INTO communication_layer_type VALUES
('result','Central model result and baseline interpretation.','Baseline result is overstated as certain.'),
('uncertainty','Output ranges, intervals, and uncertainty sources.','Uncertainty is vague or unlabeled.'),
('decision_threshold','Threshold risk and action reversal.','Uncertainty is disconnected from action.'),
('model_limit','Structural limits and validation boundaries.','Model form limits are hidden.'),
('governance','Use limits, update triggers, and accountability.','Outputs travel beyond evidence.'),
('scenario','Scenario and future-condition communication.','Scenarios are mistaken for forecasts.');

INSERT INTO communication_record(record_key, communication_layer, audience, message_goal, plain_language_statement, status) VALUES
('central_result','result','decision_maker','State the baseline model result without overstating certainty','The baseline model projects the system above the minimum threshold but the result is conditional on current assumptions','active'),
('uncertainty_range','uncertainty','public','Explain plausible output variation','Across plausible model settings outcomes cover a range rather than a single exact number','review'),
('threshold_risk','decision_threshold','decision_maker','Explain whether uncertainty could reverse action','Some plausible runs cross the action threshold so the decision should be treated as fragile','review'),
('structural_limit','model_limit','technical_reviewer','State model-form limitations','The model does not fully represent behavioral adaptation or regime change','review'),
('use_limit','governance','future_user','Prevent use outside the evidence base','This model supports risk comparison and monitoring not automatic action outside the validated domain','review');

INSERT INTO uncertainty_message VALUES
('parameter_uncertainty','parameter','Parameter estimates vary across plausible calibration ranges','Some model inputs are estimated rather than known exactly','Better evidence about sensitive parameters could change confidence'),
('scenario_uncertainty','scenario','Outputs differ across named future conditions','These scenarios explore different possible futures not guaranteed forecasts','The decision should be tested across adverse and baseline futures'),
('structural_uncertainty','model_form','Alternative model forms produce different threshold behavior','Another plausible model structure could lead to a different conclusion','Model disagreement should be preserved in the decision summary'),
('threshold_fragility','decision_threshold','Some plausible model runs cross the action threshold','The recommendation could change if conditions move slightly','Use monitoring buffer or adaptive response');

INSERT INTO audience_guide VALUES
('technical_reviewer','Auditability and method transparency','Assumptions diagnostics code uncertainty methods and validation scope'),
('decision_maker','Action relevance and risk','Thresholds robustness fragility consequences and monitoring needs'),
('public','Clear meaning without false certainty','Plain-language ranges scenario labels limitations and consequences'),
('domain_expert','Mechanism and plausibility','Model structure omitted mechanisms and boundary assumptions'),
('affected_stakeholder','Consequences and fairness','Subgroup uncertainty risk burden and affected consequences'),
('future_user','Reproducibility and update path','Use limits update triggers and uncertainty monitoring');
