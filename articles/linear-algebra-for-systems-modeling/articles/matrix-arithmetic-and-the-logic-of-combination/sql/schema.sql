DROP TABLE IF EXISTS matrix_arithmetic_assumption_registry;
DROP TABLE IF EXISTS matrix_arithmetic_audit_cases;

CREATE TABLE matrix_arithmetic_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO matrix_arithmetic_assumption_registry VALUES
('shape_compatibility','Shape compatibility','Requires matrices to have the same row and column dimensions for addition or subtraction.','Ensures entries can be combined position by position.','Same shape is necessary but not sufficient for meaningful combination.'),
('row_alignment','Row alignment','Requires corresponding rows to index the same modeled entities.','Prevents unrelated observations nodes regions or equations from being combined.','Row order must be documented and checked before arithmetic.'),
('column_alignment','Column alignment','Requires corresponding columns to index the same variables or components.','Prevents unrelated features destinations sectors or state variables from being combined.','Column order and labels must be documented and checked before arithmetic.'),
('unit_compatibility','Unit compatibility','Requires entries to have compatible units or documented transformations.','Supports meaningful addition subtraction scaling and weighting.','Combining dollars percentages counts and probabilities requires careful conversion.'),
('weight_interpretation','Weight interpretation','Defines the meaning of scalar weights in linear combinations.','Connects matrix arithmetic to probabilities priorities sensitivities or policy choices.','Weights should be justified documented and tested for sensitivity.'),
('component_traceability','Component traceability','Preserves links between combined matrices and source matrices.','Allows composite results to be audited decomposed and interpreted.','A combined matrix should not hide its components or transformations.');

CREATE TABLE matrix_arithmetic_audit_cases (
    operation_name TEXT NOT NULL,
    matrix_shape TEXT NOT NULL,
    compatible_shape INTEGER NOT NULL,
    output_entry_sum REAL NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO matrix_arithmetic_audit_cases VALUES
('baseline_plus_weighted_intervention_and_stress','3x3',1,3.95,'Shape compatibility is not enough; rows columns units baselines and effect definitions must align.');
