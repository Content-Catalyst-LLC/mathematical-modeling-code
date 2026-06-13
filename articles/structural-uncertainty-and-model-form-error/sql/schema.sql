-- Structural uncertainty and model form error governance schema.

DROP TABLE IF EXISTS structural_component_guide;
DROP TABLE IF EXISTS model_form;
DROP TABLE IF EXISTS structural_uncertainty_register;
DROP TABLE IF EXISTS structural_layer_type;

CREATE TABLE structural_layer_type (
    structural_layer TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    typical_failure TEXT NOT NULL
);

CREATE TABLE structural_uncertainty_register (
    record_id INTEGER PRIMARY KEY,
    record_key TEXT NOT NULL,
    structural_layer TEXT NOT NULL,
    modeling_role TEXT NOT NULL,
    review_question TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('active', 'review', 'revise', 'archive')),
    FOREIGN KEY (structural_layer) REFERENCES structural_layer_type(structural_layer)
);

CREATE TABLE model_form (
    model_key TEXT PRIMARY KEY,
    model_family TEXT NOT NULL,
    structural_assumption TEXT NOT NULL,
    review_question TEXT NOT NULL
);

CREATE TABLE structural_component_guide (
    structural_layer TEXT PRIMARY KEY,
    meaning TEXT NOT NULL,
    example TEXT NOT NULL,
    review_question TEXT NOT NULL
);

INSERT INTO structural_layer_type VALUES
('model_family','Choice among mathematical modeling paradigms.','A familiar family is used rather than a suitable family.'),
('relationship','Mathematical relationship among variables.','Wrong functional form distorts system behavior.'),
('boundary','Included and excluded system scope.','Relevant drivers are outside the model.'),
('aggregation','Grouping of heterogeneous elements.','Average results hide subgroup or spatial risk.'),
('scale','Resolution of representation.','Model scale does not match decision scale.'),
('regime','Behavior under thresholds or stress.','Model assumes normal behavior during regime shift.'),
('governance','Documentation and communication.','Single-model authority is overstated.');

INSERT INTO structural_uncertainty_register(record_key, structural_layer, modeling_role, review_question, status) VALUES
('model_family_choice','model_family','Compares plausible mathematical model families','Does the conclusion depend on the model family?','review'),
('functional_form','relationship','Reviews whether equations impose the right relationship','Do residuals or scenarios suggest wrong functional form?','review'),
('boundary_choice','boundary','Documents what is included and excluded','Could excluded drivers change the conclusion?','review'),
('aggregation_choice','aggregation','Reviews whether averaging hides heterogeneity','Does aggregation conceal subgroup or spatial risk?','review'),
('threshold_regime','regime','Reviews whether system behavior changes near critical thresholds','Could regime shift invalidate baseline structure?','review');

INSERT INTO model_form VALUES
('linear_decline','algebraic','Resource stock declines by a fixed amount each period','Does constant decline hide nonlinear depletion or recovery?'),
('proportional_decline','dynamic','Loss is proportional to current stock','Does proportional loss exaggerate or understate late-stage behavior?'),
('logistic_recovery','dynamic','Stock replenishes toward carrying capacity while extraction continues','Does recovery depend on a plausible carrying capacity?'),
('threshold_shift','piecewise','System behavior changes below a critical stock threshold','Does a regime shift change the decision?');

INSERT INTO structural_component_guide VALUES
('model_family','Choice among modeling paradigms','static versus dynamic','Does model family change the conclusion?'),
('relationship','Mathematical relationship among variables','linear versus nonlinear','Does functional form distort behavior?'),
('boundary','Included and excluded system scope','external policy omitted','Could excluded drivers change outputs?'),
('aggregation','Grouping of heterogeneous elements','averaged subgroups','Does aggregation hide risk?'),
('scale','Resolution of representation','regional versus local','Does scale match the decision?'),
('regime','Behavior under thresholds or stress','threshold shift','Does the system change mode?'),
('governance','Documentation and communication','use-limit statement','Where is single-model authority unwarranted?');
