DROP TABLE IF EXISTS rank_nullity_assumption_registry;
DROP TABLE IF EXISTS rank_nullity_audit_cases;

CREATE TABLE rank_nullity_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO rank_nullity_assumption_registry VALUES
('rank','Rank','Measures the dimension of independent row or column structure.','Shows the effective number of independent constraints features or output directions.','Rank is not the same as model adequacy or truth.'),
('nullity','Nullity','Measures the dimension of the null space.','Shows how many independent freedom directions remain uncontrolled by the matrix.','Nullity may indicate useful flexibility missing information or non-identifiability.'),
('rank_nullity','Rank-nullity theorem','States that rank plus nullity equals the number of columns.','Connects independent structure with remaining freedom in the model.','The theorem is formal; interpretation depends on row and column meanings.'),
('row_dependence','Row dependence','Indicates equations that are linear combinations of other equations.','Signals redundant repeated or structurally linked constraints.','Dependence may be meaningful or problematic depending on purpose.'),
('column_dependence','Column dependence','Indicates variables or features that are linear combinations of others.','Signals non-identifiability or overlapping variable effects.','Dependent columns can make separate interpretation unreliable.'),
('numerical_rank','Numerical rank','Classifies rank under finite precision and tolerance rules.','Supports applied computation with noisy scaled or approximate data.','Tolerance choices should be documented and sensitivity tested.');

CREATE TABLE rank_nullity_audit_cases (
    system_name TEXT NOT NULL,
    row_count INTEGER NOT NULL,
    column_count INTEGER NOT NULL,
    rank INTEGER NOT NULL,
    nullity INTEGER NOT NULL,
    rank_deficient INTEGER NOT NULL,
    pivot_columns TEXT NOT NULL,
    free_columns TEXT NOT NULL,
    tolerance REAL NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO rank_nullity_audit_cases VALUES
('three_constraint_resource_balance_matrix',3,3,3,0,0,'0,1,2','none',0.0000000001,'Rank and nullity reveal structure but interpretation depends on model meaning.');
