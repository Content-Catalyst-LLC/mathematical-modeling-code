DROP TABLE IF EXISTS span_basis_assumption_registry;
DROP TABLE IF EXISTS span_basis_audit_cases;

CREATE TABLE span_basis_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO span_basis_assumption_registry VALUES
('span_claim','Span claim','States what vectors can generate through linear combination.','Defines which states, interventions, scenarios, or changes are representable.','A span claim is only meaningful relative to the chosen representation.'),
('coefficient_meaning','Coefficient meaning','Defines how linear-combination weights are interpreted.','Controls whether combinations represent proportions, intensities, coordinates, or abstract parameters.','Unconstrained mathematical coefficients may not be feasible or meaningful.'),
('linear_independence','Linear independence','Determines whether vectors contribute distinct directions.','Identifies whether indicators, features, interventions, or scenarios add new structure.','Mathematical independence does not prove substantive independence.'),
('linear_dependence','Linear dependence','Identifies redundancy among vectors.','Flags duplicated indicators, collinear features, redundant constraints, or repeated policy directions.','Redundancy may be useful for validation, but should not be silently overcounted.'),
('basis_choice','Basis choice','Defines a nonredundant spanning set for the representation.','Controls coordinates, interpretability, model reduction, and transformation logic.','A computationally convenient basis may not be substantively transparent.'),
('rank_tolerance','Rank tolerance','Defines numerical threshold used to distinguish independence from dependence.','Controls rank diagnostics and near-dependence warnings.','Numerical rank can be sensitive to scaling, noise, and tolerance choices.');

CREATE TABLE span_basis_audit_cases (
    vector_set_name TEXT NOT NULL,
    ambient_dimension INTEGER NOT NULL,
    vector_count INTEGER NOT NULL,
    rank_value INTEGER NOT NULL,
    spans_ambient_space INTEGER NOT NULL,
    linearly_independent INTEGER NOT NULL,
    is_basis_for_ambient_space INTEGER NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO span_basis_audit_cases VALUES
('candidate_system_basis',3,3,3,1,1,1,'A basis for the mathematical representation is not automatically an adequate basis for the real system.');
