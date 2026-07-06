DROP TABLE IF EXISTS machine_learning_pipeline_governance_registry;
DROP TABLE IF EXISTS ml_pipeline_feature_metadata;
DROP TABLE IF EXISTS machine_learning_linear_structure_audit_cases;

CREATE TABLE machine_learning_pipeline_governance_registry (
    governance_key TEXT PRIMARY KEY,
    governance_name TEXT NOT NULL,
    modeling_role TEXT NOT NULL,
    review_requirement TEXT NOT NULL,
    responsible_use_warning TEXT NOT NULL
);

INSERT INTO machine_learning_pipeline_governance_registry VALUES
('observation_definition','Observation definition','Defines what rows of the feature matrix represent.','Document sampling process inclusion rules time period unit of analysis missing records and measurement context.','Rows may reflect biased sampling institutional visibility exclusion or uneven data collection.'),
('feature_definition','Feature definition','Defines what each model input column measures or encodes.','Record units provenance transformations proxies missingness and known limitations.','Features can encode proxy variables historical bias measurement artifacts and institutional decisions.'),
('target_definition','Target definition','Defines the outcome or label the model learns to predict.','Document label source timing measurement process subjectivity delay and relationship to the decision.','A predictive target is not automatically a valid decision target.'),
('preprocessing','Preprocessing','Defines transformations applied before modeling.','Document scaling centering imputation encoding normalization projection feature selection and fitted parameters.','Preprocessing changes feature geometry and can leak information if fit outside the training process.'),
('leakage_control','Leakage control','Prevents validation or test data from influencing training.','Fit preprocessing feature selection dimensionality reduction model parameters and thresholds inside training or validation workflows only.','Leakage can make model performance appear much better than it will be in deployment.'),
('baseline_model','Baseline model','Defines the reference model used to judge added complexity.','Train transparent baselines and compare complex models against them using the same evaluation protocol.','Complexity should not be added without evidence that it improves validated decision-relevant performance.'),
('evaluation','Evaluation','Defines how predictions are assessed.','Report overall metrics residuals calibration threshold sensitivity subgroup error rare-event performance and temporal validation.','Average metrics can hide concentrated failure unequal error and decision harm.'),
('monitoring','Monitoring and drift','Defines how deployment behavior is checked over time.','Monitor feature drift label shift concept drift embedding drift residual drift data pipeline changes and retraining triggers.','A valid training-time model can become invalid when data behavior policy or the environment changes.'),
('decision_boundary','Decision boundary','Defines what the model can and cannot support.','Attach documentation uncertainty validation status threshold rationale oversight appeals and stop-use conditions to outputs.','Machine learning predictions should support accountable judgment not replace responsibility.');

CREATE TABLE ml_pipeline_feature_metadata (
    feature_name TEXT PRIMARY KEY,
    measurement_role TEXT NOT NULL,
    preprocessing_note TEXT NOT NULL,
    governance_warning TEXT NOT NULL
);

INSERT INTO ml_pipeline_feature_metadata VALUES
('asset_age','synthetic asset age feature','scaled using training rows only','Age may proxy maintenance history, investment pattern, or measurement visibility.'),
('load_index','synthetic demand or stress feature','scaled using training rows only','Load measurements may be uneven, seasonal, or context-dependent.'),
('inspection_gap','synthetic interval since inspection','scaled using training rows only','Inspection frequency may reflect institutional priorities rather than asset condition alone.'),
('temperature_stress','synthetic environmental stress feature','scaled using training rows only','Environmental features can interact with geography, infrastructure quality, and vulnerability.');

CREATE TABLE machine_learning_linear_structure_audit_cases (
    workflow_name TEXT NOT NULL,
    scenario_name TEXT NOT NULL,
    observation_count INTEGER NOT NULL,
    feature_count INTEGER NOT NULL,
    train_count INTEGER NOT NULL,
    test_count INTEGER NOT NULL,
    model_family TEXT NOT NULL,
    regularization_strength REAL NOT NULL,
    test_rmse REAL NOT NULL,
    max_absolute_residual REAL NOT NULL,
    largest_weight_feature TEXT NOT NULL,
    preprocessing_summary TEXT NOT NULL,
    leakage_warning TEXT NOT NULL,
    interpretation_warning TEXT NOT NULL
);

INSERT INTO machine_learning_linear_structure_audit_cases VALUES
('machine_learning_linear_structure_audit','synthetic_infrastructure_risk_pipeline',10,4,7,3,'ridge_regression_linear_baseline',0.25,0.041,0.061,'inspection_gap','Training means and scales were fit on training rows only and then applied to test rows.','Full-data preprocessing can leak evaluation information into the model.','Coefficients and predictions are not automatic causal explanations or decision rules.');
