-- Overfitting, underfitting, and generalization governance schema.

DROP TABLE IF EXISTS generalization_component_guide;
DROP TABLE IF EXISTS generalization_model;
DROP TABLE IF EXISTS generalization_register;
DROP TABLE IF EXISTS generalization_layer_type;

CREATE TABLE generalization_layer_type (
    generalization_layer TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    typical_failure TEXT NOT NULL
);

CREATE TABLE generalization_register (
    record_id INTEGER PRIMARY KEY,
    record_key TEXT NOT NULL,
    generalization_layer TEXT NOT NULL,
    modeling_role TEXT NOT NULL,
    review_question TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('active', 'review', 'revise', 'archive')),
    FOREIGN KEY (generalization_layer) REFERENCES generalization_layer_type(generalization_layer)
);

CREATE TABLE generalization_model (
    model_id TEXT PRIMARY KEY,
    model_family TEXT NOT NULL,
    training_rmse REAL NOT NULL,
    validation_rmse REAL NOT NULL,
    parameter_count INTEGER NOT NULL,
    complexity_score REAL NOT NULL,
    interpretability_score REAL NOT NULL
);

CREATE TABLE generalization_component_guide (
    generalization_layer TEXT PRIMARY KEY,
    meaning TEXT NOT NULL,
    example TEXT NOT NULL,
    review_question TEXT NOT NULL
);

INSERT INTO generalization_layer_type VALUES
('evidence','Separation of fitting and assessment evidence.','Training and validation data are not separated.'),
('diagnostics','Overfitting, underfitting, and residual diagnostics.','Fit looks strong but does not transfer.'),
('parsimony','Complexity and flexibility review.','Flexible model learns noise.'),
('regularization','Constraints that improve transfer.','Model is too unconstrained.'),
('scope','Use context and distribution shift.','Model is applied outside assessed conditions.'),
('decision_support','Threshold and decision relevance.','Average performance hides consequential failure.'),
('governance','Use limits, monitoring, and revalidation.','Generalization is overclaimed.');

INSERT INTO generalization_register(record_key, generalization_layer, modeling_role, review_question, status) VALUES
('training_validation_split','evidence','Separates fitting evidence from generalization evidence','Are training and validation data separated correctly?','active'),
('overfit_gap','diagnostics','Compares validation error against training error','Is the model learning noise rather than transferable structure?','review'),
('underfit_check','diagnostics','Flags models with high training and validation error','Is the model too simple for the system?','review'),
('complexity_review','parsimony','Reviews whether flexibility is justified','Does added complexity improve validation performance enough?','review'),
('distribution_shift','scope','Reviews whether use conditions differ from fitting conditions','Could changing systems weaken generalization?','review'),
('decision_threshold','decision_support','Connects generalization evidence to decision consequences','Does the model perform near consequential thresholds?','review');

INSERT INTO generalization_model VALUES
('constant_baseline','baseline',3.40,3.55,0,0.05,0.95),
('linear_trend','statistical',1.95,2.10,2,0.25,0.88),
('logistic_growth','mechanistic',1.20,1.38,3,0.45,0.78),
('regularized_curve','regularized',0.95,1.44,5,0.62,0.66),
('high_flex_curve','flexible',0.28,2.85,10,0.95,0.30);

INSERT INTO generalization_component_guide VALUES
('evidence','Separation of fitting and assessment evidence','training validation split','Is evidence separation clean?'),
('diagnostics','Error patterns showing overfit or underfit behavior','overfit gap','Does performance transfer?'),
('parsimony','Complexity and flexibility review','parameter count','Is complexity justified?'),
('regularization','Constraints that reduce overfitting','penalty term','Does constraint improve transfer?'),
('scope','Use conditions and distribution shift','time split','Do conditions change?'),
('decision_support','Fitness for decision thresholds','threshold validation','Does failure matter for action?'),
('governance','Use limits and monitoring','revalidation plan','Where should transfer not be assumed?');
