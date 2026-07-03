DROP TABLE IF EXISTS machine_learning_governance_registry;
DROP TABLE IF EXISTS ml_linear_algebra_audit_cases;

CREATE TABLE machine_learning_governance_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO machine_learning_governance_registry VALUES
('feature_matrix','Feature matrix','Defines observations features units preprocessing and matrix shape.','Determines what the model can learn from the system.','A model cannot recover structure absent or misrepresented in the feature matrix.'),
('label_definition','Label definition','Defines target vector or target matrix used for supervised learning.','Determines what the model is trained to approximate.','Labels may be noisy proxies rather than valid measures of the intended concept.'),
('preprocessing','Preprocessing','Defines centering scaling encoding imputation transformation and filtering.','Shapes geometry distances coefficients gradients and model stability.','Preprocessing choices can change learned patterns and should be documented.'),
('model_class','Model class','Defines functional form and parameter structure.','Controls what relationships can be represented.','Model complexity should match data task and validation evidence.'),
('loss_function','Loss function','Defines what prediction error or objective is optimized.','Determines what the model treats as success.','Changing the loss changes the meaning of learning.'),
('regularization','Regularization','Constrains parameter magnitude sparsity rank or complexity.','Improves stability and can reduce overfitting.','Regularization strength should be validated rather than chosen casually.'),
('validation_design','Validation design','Defines train-test splits cross-validation time splits metrics and residual review.','Evaluates whether the model generalizes beyond training data.','Training performance is not deployment evidence.'),
('responsible_interpretation','Responsible interpretation','Defines how model outputs weights components embeddings and scores are explained.','Prevents learned patterns from being overstated as causes truths or policy certainty.','Model outputs should be interpreted with uncertainty context and accountability.');

CREATE TABLE ml_linear_algebra_audit_cases (
    model_name TEXT NOT NULL,
    observations INTEGER NOT NULL,
    features INTEGER NOT NULL,
    method TEXT NOT NULL,
    preprocessing TEXT NOT NULL,
    regularization_strength REAL NOT NULL,
    feature_matrix_condition_number REAL NOT NULL,
    gram_matrix_condition_number REAL NOT NULL,
    numerical_rank INTEGER NOT NULL,
    ridge_weight_norm REAL NOT NULL,
    training_rmse REAL NOT NULL,
    maximum_absolute_residual REAL NOT NULL,
    first_two_component_energy REAL NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO ml_linear_algebra_audit_cases VALUES
('synthetic_machine_learning_linear_algebra_audit',10,5,'standardized_ridge_regression_with_svd_diagnostics','centered_and_standardized_features_centered_target',0.75,18.4,339.2,5,8.7,1.9,3.8,0.94,'Training error is not generalization evidence and learned weights are not automatic causes.');
