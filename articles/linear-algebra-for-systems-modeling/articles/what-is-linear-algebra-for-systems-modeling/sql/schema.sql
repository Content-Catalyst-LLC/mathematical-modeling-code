DROP TABLE IF EXISTS linear_algebra_assumption_registry;
DROP TABLE IF EXISTS matrix_audit_cases;

CREATE TABLE linear_algebra_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO linear_algebra_assumption_registry VALUES
('vector_definition','Vector definition','Defines the ordered components of a system state.','Controls which quantities are represented and compared.','Vector entries should include units, scale, ordering, and meaning.'),
('matrix_meaning','Matrix meaning','Defines what matrix entries represent.','Distinguishes coefficients, flows, probabilities, weights, links, and transformations.','A valid matrix operation can still have an invalid systems interpretation.'),
('scaling_and_units','Scaling and units','Controls how quantities are compared within vector and matrix operations.','Shapes distance, similarity, decomposition, conditioning, and optimization results.','Unscaled or incompatible units can dominate outputs.'),
('rank_and_dependency','Rank and dependency','Identifies independent structure and redundancy.','Supports solvability, degrees of freedom, constraint review, and model diagnosis.','Low rank may reflect true structure, omitted variables, or measurement artifacts.'),
('eigenvalue_interpretation','Eigenvalue interpretation','Connects transformation behavior to scaling along preserved directions.','Supports stability, long-run behavior, amplification, decay, and dominant-mode analysis.','Eigenvalue claims depend on the model form, scaling, and whether linear dynamics are appropriate.'),
('decomposition_review','Decomposition review','Documents factorization, dimensionality reduction, and component interpretation.','Clarifies what structure is preserved, compressed, or discarded.','Principal components or singular vectors should not be overinterpreted as real-world causes.');

CREATE TABLE matrix_audit_cases (
    model_name TEXT NOT NULL,
    rows INTEGER NOT NULL,
    columns INTEGER NOT NULL,
    matrix_meaning TEXT NOT NULL,
    interpretation_warning TEXT NOT NULL
);

INSERT INTO matrix_audit_cases VALUES
('two_component_transition_model',2,2,'transition-like matrix connecting two system components across a modeling step','Matrix interpretation depends on entry meaning, scaling, and whether linearity is appropriate.');
