DROP TABLE IF EXISTS matrix_assumption_registry;
DROP TABLE IF EXISTS matrix_structure_audit_cases;

CREATE TABLE matrix_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO matrix_assumption_registry VALUES
('matrix_role','Matrix role','Classifies the matrix as data, coefficient, transition, adjacency, flow, or other structure.','Determines how rows, columns, entries, and operations should be interpreted.','The same numerical matrix can mean different things under different roles.'),
('row_meaning','Row meaning','Defines what each row indexes.','Controls whether rows represent observations, equations, nodes, sectors, states, or constraints.','Changing row order or row meaning can invalidate joins, multiplication, and interpretation.'),
('column_meaning','Column meaning','Defines what each column indexes.','Controls whether columns represent variables, features, unknowns, sources, destinations, or components.','Column misalignment can attach values to the wrong system quantities.'),
('entry_meaning','Entry meaning','Defines what each matrix entry represents.','Determines whether values are measurements, coefficients, probabilities, links, flows, or estimates.','Entries cannot be interpreted responsibly without row and column definitions.'),
('orientation_rule','Orientation rule','Defines whether rows or columns represent sources, destinations, current states, future states, observations, or variables.','Controls valid multiplication and interpretation of outputs.','Transposed matrices can produce mathematically valid but substantively wrong results.'),
('unit_and_scale','Unit and scale','Defines units, normalization, standardization, and scaling conventions.','Controls comparison, aggregation, distance, rank, conditioning, and optimization behavior.','Mixed units and hidden scaling choices can distort matrix computations.'),
('zero_missingness','Zero and missingness','Defines whether zero means absence, no effect, baseline, or missing data.','Controls sparsity interpretation and data-quality review.','Confusing zeros with missing values can seriously distort system interpretation.');

CREATE TABLE matrix_structure_audit_cases (
    matrix_name TEXT NOT NULL,
    matrix_role TEXT NOT NULL,
    row_count INTEGER NOT NULL,
    column_count INTEGER NOT NULL,
    nonzero_entries INTEGER NOT NULL,
    sparsity_ratio REAL NOT NULL,
    symmetric INTEGER NOT NULL,
    rank_value INTEGER NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO matrix_structure_audit_cases VALUES
('infrastructure_interdependency_matrix','weighted adjacency matrix',4,4,8,0.5,1,4,'Symmetry suggests reciprocal relationships in this example but should not be assumed.');
