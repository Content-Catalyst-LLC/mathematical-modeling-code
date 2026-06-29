DROP TABLE IF EXISTS state_space_geometry_assumption_registry;
DROP TABLE IF EXISTS state_space_geometry_audit_cases;

CREATE TABLE state_space_geometry_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO state_space_geometry_assumption_registry VALUES
('inner_product','Inner product','Defines alignment angle orthogonality and derived length.','Determines how state directions are compared.','Changing weights units or scaling can change geometric conclusions.'),
('norm','Norm','Measures vector magnitude.','Measures state size residual magnitude error or change.','Different norms emphasize different kinds of deviation.'),
('distance','Distance','Applies a norm to the difference between states.','Measures separation between scenarios observations or simulations.','Distance is meaningful only when state coordinates are comparable.'),
('weighted_geometry','Weighted geometry','Uses a positive definite matrix to weight directions.','Represents risk cost energy uncertainty priority or reliability.','Weights must be justified and documented.'),
('normalization','Normalization','Transforms coordinates to comparable scales.','Reduces unit dominance in distance calculations.','Normalized outputs must be translated back into domain terms.'),
('covariance_distance','Covariance-aware distance','Uses covariance structure to measure unusual deviation.','Accounts for variance and correlation among state variables.','Requires reliable covariance estimation and review.');

CREATE TABLE state_space_geometry_audit_cases (
    system_name TEXT NOT NULL,
    state_a TEXT NOT NULL,
    state_b TEXT NOT NULL,
    difference_vector TEXT NOT NULL,
    dot_product REAL NOT NULL,
    cosine_similarity REAL NOT NULL,
    weighted_inner_product REAL NOT NULL,
    norm_1 REAL NOT NULL,
    norm_2 REAL NOT NULL,
    norm_inf REAL NOT NULL,
    euclidean_distance REAL NOT NULL,
    weighted_distance REAL NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO state_space_geometry_audit_cases VALUES
('three_indicator_state_space_geometry_audit','12.000000,4.000000,0.800000','10.000000,5.500000,1.100000','2.000000,-1.500000,-0.300000',142.88,0.988725,133.04,3.8,2.517936,2.0,2.517936,2.33538,'Distance depends on units scaling norm choice and weights.');
