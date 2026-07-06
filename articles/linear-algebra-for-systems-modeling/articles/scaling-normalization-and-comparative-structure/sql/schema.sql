DROP TABLE IF EXISTS scaling_governance_registry;
DROP TABLE IF EXISTS scaling_normalization_audit_cases;

CREATE TABLE scaling_governance_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    modeling_role TEXT NOT NULL,
    transformation_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO scaling_governance_registry VALUES
('raw_units','Raw units','Preserves original measurement meaning.','Keeps values in domain units such as dollars tons kilometers rates or probabilities.','Raw magnitudes can dominate computation when units differ widely.'),
('centering','Centering','Represents values as deviations from a baseline.','Subtracts means or reference values before variance covariance PCA or regression analysis.','Centering removes absolute level from the transformed representation.'),
('standardization','Standardization','Makes variables comparable by relative variation.','Subtracts mean and divides by standard deviation.','Standardization changes interpretation from original units to standard-deviation units.'),
('minmax_normalization','Min-max normalization','Represents values by location within an observed range.','Maps values to a bounded interval such as zero to one.','Outliers and changing ranges can shift normalized values.'),
('vector_normalization','Vector normalization','Compares direction or profile rather than magnitude.','Divides vectors by their norms.','Total size is removed from the comparison.'),
('row_normalization','Row normalization','Represents each row as a distribution share or probability profile.','Divides row entries by row totals or row norms.','Row totals disappear unless preserved separately.'),
('column_normalization','Column normalization','Balances feature influence across columns.','Scales columns by variance norm range or domain constant.','Feature magnitudes may no longer reflect real-world size.'),
('condition_scaling','Conditioning-oriented scaling','Improves numerical balance and solver behavior.','Uses diagonal scaling equilibration nondimensionalization or preconditioning.','Scaled numerical results must be interpreted or transformed back carefully.'),
('scale_sensitivity','Scale sensitivity','Tests whether conclusions depend on scaling choices.','Compares outputs across raw centered standardized normalized and domain-scaled matrices.','Scale-sensitive conclusions require explicit interpretation warnings.');

CREATE TABLE scaling_normalization_audit_cases (
    workflow_name TEXT NOT NULL,
    matrix_shape TEXT NOT NULL,
    row_meaning TEXT NOT NULL,
    column_meaning TEXT NOT NULL,
    raw_column_norm_1 REAL NOT NULL,
    raw_column_norm_2 REAL NOT NULL,
    standardized_column_norm_1 REAL NOT NULL,
    standardized_column_norm_2 REAL NOT NULL,
    first_row_sum_after_row_normalization REAL NOT NULL,
    first_row_norm_after_unit_normalization REAL NOT NULL,
    raw_condition_proxy REAL NOT NULL,
    standardized_condition_proxy REAL NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO scaling_normalization_audit_cases VALUES
('scaling_normalization_audit','3x2','infrastructure_zones','annual_demand_and_outage_exposure',2345.207880,0.174929,1.414214,1.414214,1.0,1.0,13406.312329,1.0,'Scaling and normalization change what comparison means.');
