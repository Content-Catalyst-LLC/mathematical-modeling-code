-- Model interpretation and decision-making governance schema.

DROP TABLE IF EXISTS stakeholder_decision_guide;
DROP TABLE IF EXISTS decision_option;
DROP TABLE IF EXISTS interpretation_register;
DROP TABLE IF EXISTS interpretation_layer_type;

CREATE TABLE interpretation_layer_type (
    interpretation_layer TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    typical_failure TEXT NOT NULL
);

CREATE TABLE interpretation_register (
    record_id INTEGER PRIMARY KEY,
    record_key TEXT NOT NULL,
    interpretation_layer TEXT NOT NULL,
    model_role TEXT NOT NULL,
    decision_question TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('active', 'review', 'revise', 'archive')),
    FOREIGN KEY (interpretation_layer) REFERENCES interpretation_layer_type(interpretation_layer)
);

CREATE TABLE decision_option (
    option_key TEXT PRIMARY KEY,
    option_name TEXT NOT NULL,
    expected_stock REAL NOT NULL,
    lower_bound REAL NOT NULL,
    upper_bound REAL NOT NULL,
    implementation_burden REAL NOT NULL,
    consequence_if_wrong REAL NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE stakeholder_decision_guide (
    stakeholder_group TEXT PRIMARY KEY,
    decision_concern TEXT NOT NULL,
    interpretation_need TEXT NOT NULL,
    governance_question TEXT NOT NULL
);

INSERT INTO interpretation_layer_type VALUES
('result','Meaning of the model output.','Output is treated as direct reality.'),
('uncertainty','Uncertainty and plausible range.','Central estimate is interpreted alone.'),
('decision_threshold','Action boundary or trigger condition.','Threshold is hidden or treated as purely technical.'),
('values','Tradeoffs, objectives, and consequence weights.','Value judgments are hidden inside the model.'),
('governance','Decision ownership, use limits, monitoring, and accountability.','The model is treated as the decision owner.'),
('communication','How interpretation is conveyed to users.','Conditional result is communicated as certainty.');

INSERT INTO interpretation_register(record_key, interpretation_layer, model_role, decision_question, status) VALUES
('output_meaning','result','Explains what the output represents','What claim is being made from the model output?','active'),
('uncertainty_meaning','uncertainty','Connects uncertainty range to interpretation','Could uncertainty change the decision?','review'),
('threshold_review','decision_threshold','Reviews proximity to action boundary','Does the result cross or approach the threshold?','review'),
('value_tradeoff','values','Documents tradeoffs and objectives','Which values are represented or excluded?','review'),
('governance_review','governance','Documents decision ownership and use limits','Who owns the decision and monitoring plan?','review');

INSERT INTO decision_option VALUES
('no_action','No immediate action',52.0,38.0,66.0,1.0,9.0,'Continue current behavior and monitor informally'),
('monitoring','Formal monitoring',54.0,42.0,68.0,3.0,6.0,'Increase measurement and update model if trigger values appear'),
('moderate_intervention','Moderate intervention',60.0,50.0,72.0,5.0,4.0,'Reduce extraction moderately while preserving adaptive monitoring'),
('strong_intervention','Strong intervention',68.0,58.0,78.0,8.0,2.0,'Reduce extraction aggressively to maximize safety margin');

INSERT INTO stakeholder_decision_guide VALUES
('decision_owner','Accountable action','Decision summary and use limits','Who owns the final decision?'),
('technical_reviewer','Model credibility','Assumptions validation uncertainty and diagnostics','Has evidence been reviewed?'),
('affected_public','Consequences and fairness','Plain-language uncertainty and impact','Who bears risk?'),
('domain_expert','Mechanism plausibility','Model structure and omitted mechanisms','Does representation make sense?'),
('future_maintainer','Update and monitoring','Triggers and revalidation plan','When should the model be revised?');
