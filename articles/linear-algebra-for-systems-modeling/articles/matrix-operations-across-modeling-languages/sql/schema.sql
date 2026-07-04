DROP TABLE IF EXISTS matrix_operation_governance_registry;
DROP TABLE IF EXISTS cross_language_matrix_audit_cases;

CREATE TABLE matrix_operation_governance_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    implementation_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO matrix_operation_governance_registry VALUES
('mathematical_intent','Mathematical intent','Defines the linear algebra operation being implemented.','Links code syntax to the intended mathematical expression.','Code should be reviewed against the mathematical operation not only successful execution.'),
('shape_discipline','Shape discipline','Defines matrix and vector dimensions before and after operations.','Prevents silent broadcasting recycling or orientation errors.','Shape checks should be recorded for every major operation.'),
('indexing_convention','Indexing convention','Defines whether positions are zero-based one-based or label-based.','Prevents off-by-one errors across languages.','Index mapping should be explicit when moving between Python R Julia SQL and lower-level code.'),
('operator_semantics','Operator semantics','Distinguishes matrix multiplication elementwise multiplication dot products and broadcasting.','Prevents syntactic translation from changing the model.','The same symbol can mean different operations in different languages.'),
('storage_format','Storage format','Defines dense sparse array tensor table or matrix-free representation.','Controls memory speed solver choice and metadata preservation.','Storage changes can alter performance and sometimes interpretation.'),
('numerical_diagnostics','Numerical diagnostics','Tracks residuals condition numbers rank determinant and tolerance checks.','Determines whether computed results are reliable enough to interpret.','A returned value should not be trusted without diagnostics.'),
('interoperability','Interoperability','Defines how matrix data metadata schemas and outputs move across languages.','Preserves row IDs column IDs units precision missingness and assumptions.','Data exchange can silently lose the meaning needed for responsible modeling.'),
('responsible_use','Responsible use','Defines how implementation assumptions and limitations are communicated.','Prevents code portability from being mistaken for model validity.','Cross-language agreement supports confidence only when assumptions and diagnostics are documented.');

CREATE TABLE cross_language_matrix_audit_cases (
    model_name TEXT NOT NULL,
    language TEXT NOT NULL,
    matrix_shape TEXT NOT NULL,
    vector_shape TEXT NOT NULL,
    indexing_convention TEXT NOT NULL,
    matrix_multiplication_operator TEXT NOT NULL,
    elementwise_operator TEXT NOT NULL,
    solve_method TEXT NOT NULL,
    condition_number REAL NOT NULL,
    matrix_vector_product_norm REAL NOT NULL,
    matrix_matrix_product_trace REAL NOT NULL,
    solve_residual_norm REAL NOT NULL,
    determinant REAL NOT NULL,
    validation_status TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO cross_language_matrix_audit_cases VALUES
('cross_language_matrix_operation_audit','sql_governance_record','3x3','3','label_or_query_order_dependent','aggregation_over_indexes','rowwise_expression','not_native_for_heavy_solves',2.25,10.42,30.125,0.0,26.625,'requires_external_numeric_validation','SQL can govern matrix construction and audit semantics but is not usually the right layer for heavy numerical linear algebra.');
