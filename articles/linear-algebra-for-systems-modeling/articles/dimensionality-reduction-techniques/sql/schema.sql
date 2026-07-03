DROP TABLE IF EXISTS dimensionality_reduction_governance_registry;
DROP TABLE IF EXISTS dimensionality_reduction_audit_cases;

CREATE TABLE dimensionality_reduction_governance_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO dimensionality_reduction_governance_registry VALUES
('original_matrix','Original matrix','Defines observations variables entries units and missing-data handling.','Determines what structure can be preserved or lost during reduction.','Reduction is only as meaningful as the original matrix construction.'),
('preprocessing','Preprocessing','Defines centering scaling normalization transformations and weighting.','Determines which patterns dominate the reduced representation.','Preprocessing choices can substantially change reduced coordinates.'),
('reduction_method','Reduction method','Defines the mathematical transformation from original space to reduced space.','Determines whether variance distance neighborhoods reconstruction or another target is preserved.','Different methods preserve different structures and should not be interpreted interchangeably.'),
('target_dimension','Target dimension','Defines the number of reduced coordinates retained.','Controls compression reconstruction error interpretability and downstream performance.','The reduced dimension should be justified and sensitivity-tested.'),
('preservation_target','Preservation target','Defines what the reduction is intended to preserve.','Connects method choice to the systems question.','Variance distance neighborhoods and prediction performance are different objectives.'),
('information_loss','Information loss','Measures reconstruction error distortion residuals or lost structure.','Supports review of what the reduced representation fails to capture.','Low aggregate error can hide localized or high-consequence loss.'),
('randomness_and_parameters','Randomness and parameters','Defines seeds tolerances neighborhood sizes perplexity minimum distance or solver settings.','Supports reproducibility and sensitivity review.','Different parameter choices can change the reduced representation.'),
('responsible_interpretation','Responsible interpretation','Defines how reduced coordinates are explained and used.','Prevents reduced spaces from being treated as automatic causes or categories.','Reduced coordinates are model artifacts and require validation.');

CREATE TABLE dimensionality_reduction_audit_cases (
    model_name TEXT NOT NULL,
    observations INTEGER NOT NULL,
    original_dimensions INTEGER NOT NULL,
    reduced_dimensions INTEGER NOT NULL,
    method TEXT NOT NULL,
    preprocessing TEXT NOT NULL,
    preservation_target TEXT NOT NULL,
    explained_variance_retained REAL NOT NULL,
    relative_reconstruction_error REAL NOT NULL,
    mean_pairwise_distance_distortion REAL NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO dimensionality_reduction_audit_cases VALUES
('synthetic_dimensionality_reduction_audit',8,6,2,'svd_based_pca_projection','centered_and_standardized','maximum_variance_under_linear_projection',0.982,0.134,0.286,'Reduced coordinates are model artifacts not automatic causes categories or complete system truths.');
