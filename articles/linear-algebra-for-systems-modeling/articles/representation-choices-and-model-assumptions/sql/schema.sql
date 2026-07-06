DROP TABLE IF EXISTS representation_governance_registry;
DROP TABLE IF EXISTS representation_assumption_audit_cases;

CREATE TABLE representation_governance_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    modeling_role TEXT NOT NULL,
    representation_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO representation_governance_registry VALUES
('system_boundary','System boundary','Defines what is inside or outside the model.','Determines which rows columns relationships states or entities can appear in the matrix.','Excluded structure cannot be recovered by later computation unless the representation changes.'),
('row_column_meaning','Row and column meaning','Defines what rows and columns stand for.','Gives matrix dimensions substantive interpretation.','Rows and columns should not be treated as self-explanatory.'),
('value_meaning','Value meaning','Defines what matrix entries measure.','Connects numeric entries to relationships flows probabilities distances or coefficients.','The same number can mean different things under different representation rules.'),
('zero_meaning','Zero meaning','Defines whether zero means absence measurement missingness thresholding or non-applicability.','Shapes sparsity distance rank and interpretation.','Encoding missingness as zero can create false structure.'),
('scale_choice','Scale choice','Defines raw units standardization normalization log transformation or other scaling rules.','Affects comparability conditioning geometry and interpretation.','Scaling changes what distances coefficients and components mean.'),
('aggregation_resolution','Aggregation and resolution','Defines the level at which entities time space or categories are represented.','Controls detail sparsity noise and interpretability.','Aggregation can hide local variation and distributional structure.'),
('encoding_rule','Encoding rule','Defines how categorical qualitative temporal spatial or relational information becomes numeric.','Makes information usable in linear algebra.','Encoding can impose false ordering distance or similarity.'),
('interpretation_boundary','Interpretation boundary','Defines what conclusions the representation can and cannot support.','Prevents computational results from being overclaimed.','A correct computation can still exceed the evidence allowed by the representation.');

CREATE TABLE representation_assumption_audit_cases (
    workflow_name TEXT NOT NULL,
    matrix_shape TEXT NOT NULL,
    row_meaning TEXT NOT NULL,
    column_meaning TEXT NOT NULL,
    value_meaning TEXT NOT NULL,
    zero_meaning TEXT NOT NULL,
    missing_value_rule TEXT NOT NULL,
    raw_column_norm_1 REAL NOT NULL,
    raw_column_norm_2 REAL NOT NULL,
    standardized_column_norm_1 REAL NOT NULL,
    standardized_column_norm_2 REAL NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO representation_assumption_audit_cases VALUES
('representation_assumption_audit','3x2','infrastructure_zones','annual_demand_and_outage_exposure','mixed_units_before_standardization','zero_would_mean_measured_absence_not_missingness','missing_values_must_not_be_encoded_as_zero_without_flag',2345.207880,0.174929,1.414214,1.414214,'Representation choices define what the model can compare reveal and hide.');
