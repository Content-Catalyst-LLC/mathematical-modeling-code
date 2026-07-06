DROP TABLE IF EXISTS dimensionality_reduction_governance_registry;
DROP TABLE IF EXISTS feature_matrix_metadata;
DROP TABLE IF EXISTS dimensionality_reduction_audit_cases;

CREATE TABLE dimensionality_reduction_governance_registry (
    governance_key TEXT PRIMARY KEY,
    governance_name TEXT NOT NULL,
    modeling_role TEXT NOT NULL,
    review_requirement TEXT NOT NULL,
    responsible_use_warning TEXT NOT NULL
);

INSERT INTO dimensionality_reduction_governance_registry VALUES
('observation_definition','Observation definition','Defines what rows of the feature matrix represent.','Document whether observations are people assets documents regions time periods sensors cases simulations or systems.','Rows may carry ethical institutional or domain-specific meaning that compression can obscure.'),
('feature_definition','Feature definition','Defines what columns measure or encode.','Record units measurement sources proxies missingness transformations and feature provenance.','Features can encode noise bias proxy relationships or historical artifacts.'),
('preprocessing','Preprocessing','Defines centering scaling imputation transformation filtering and outlier handling.','Document all preprocessing parameters and ensure they are fit only on training data when used in predictive workflows.','Preprocessing choices can determine which features dominate the reduced representation.'),
('component_selection','Component selection','Defines how many dimensions are retained.','Record explained variance reconstruction error stability evidence downstream validation and domain justification.','Variance thresholds alone can discard rare local minority or high-stakes structure.'),
('reconstruction_review','Reconstruction review','Measures what is lost by the low-dimensional approximation.','Inspect total per-feature per-observation subgroup and task-specific reconstruction error.','Low average error can hide concentrated loss for important cases.'),
('leakage_control','Leakage control','Prevents validation data from influencing preprocessing or component fitting.','Fit scaling and dimensionality reduction inside training folds or training data only.','Leakage can inflate model performance and make validation unreliable.'),
('interpretability_review','Interpretability review','Defines how component scores loadings clusters and visual patterns may be described.','Review loadings domain evidence stability and whether labels are justified.','Components are mathematical mixtures not automatically causal factors or natural categories.'),
('decision_boundary','Decision boundary','Defines what the reduced representation can and cannot support.','Attach preprocessing choices component count uncertainty notes validation status and stop-use conditions to outputs.','Dimensionality reduction should support accountable analysis not replace domain review.');

CREATE TABLE feature_matrix_metadata (
    feature_name TEXT PRIMARY KEY,
    measurement_role TEXT NOT NULL,
    preprocessing_note TEXT NOT NULL,
    governance_warning TEXT NOT NULL
);

INSERT INTO feature_matrix_metadata VALUES
('load','synthetic infrastructure load feature','center and scale before PCA','High-variance features can dominate without scaling.'),
('temperature','synthetic thermal condition feature','center and scale before PCA','Feature may encode seasonal or contextual effects.'),
('vibration','synthetic vibration signal feature','center and scale before PCA','Low-magnitude features can still carry failure signals.'),
('pressure','synthetic pressure feature','center and scale before PCA','Direction of association may differ from other features.'),
('latency','synthetic performance-delay feature','center and scale before PCA','Dominant components are not automatically causal explanations.');

CREATE TABLE dimensionality_reduction_audit_cases (
    workflow_name TEXT NOT NULL,
    scenario_name TEXT NOT NULL,
    observation_count INTEGER NOT NULL,
    feature_count INTEGER NOT NULL,
    retained_components INTEGER NOT NULL,
    cumulative_explained_variance REAL NOT NULL,
    reconstruction_rmse REAL NOT NULL,
    dominant_component_feature TEXT NOT NULL,
    preprocessing_summary TEXT NOT NULL,
    validation_warning TEXT NOT NULL,
    interpretation_warning TEXT NOT NULL
);

INSERT INTO dimensionality_reduction_audit_cases VALUES
('dimensionality_reduction_audit','synthetic_high_dimensional_sensor_feature_matrix',8,5,2,0.991,0.086,'latency','Features were centered and standardized before PCA.','Component selection should be checked against reconstruction error stability subgroup error rare-pattern preservation and downstream task performance.','Principal components are mathematical directions of variation not automatically causal factors natural categories or decision-ready explanations.');
