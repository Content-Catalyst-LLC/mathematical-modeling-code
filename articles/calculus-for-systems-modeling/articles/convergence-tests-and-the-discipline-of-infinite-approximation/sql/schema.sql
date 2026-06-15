DROP TABLE IF EXISTS convergence_test_assumption_registry;
DROP TABLE IF EXISTS convergence_test_audit_records;

CREATE TABLE convergence_test_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO convergence_test_assumption_registry VALUES
('test_selected','Test selected','Identifies which convergence test or bounding argument is used.','Makes the infinite-approximation claim auditable.','A convergence claim without a named test or bound is weak.'),
('test_conditions','Test conditions','Documents the assumptions required by the selected test.','Prevents tests from being applied outside their valid structure.','A correct test used under false conditions gives misleading confidence.'),
('partial_sum','Partial sum','Records the finite computation actually performed.','Separates computed finite totals from infinite limiting claims.','A partial sum is not the same as an infinite series.'),
('remainder_estimate','Remainder estimate','Documents the omitted tail or error bound after truncation.','Supports responsible finite approximation.','A small last term does not always bound the full tail.'),
('inconclusive_result','Inconclusive result','Records when a test fails to classify convergence.','Prevents unsupported conclusions after an inconclusive test.','An inconclusive test should lead to another test or a limited claim.');

CREATE TABLE convergence_test_audit_records (
    series_name TEXT PRIMARY KEY,
    test_used TEXT NOT NULL,
    n_terms INTEGER NOT NULL,
    partial_sum REAL NOT NULL,
    last_term REAL NOT NULL,
    test_result TEXT NOT NULL,
    estimated_error REAL,
    stopping_rule TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO convergence_test_audit_records VALUES
('geometric_r_0.6','geometric-series test',25,24.999574,0.000284,'converges by geometric-series test',0.000426,'fixed term count with geometric tail check',''),
('geometric_r_1.05','geometric-series test',25,477.270547,32.251002,'diverges or lacks geometric convergence',NULL,'fixed term count with geometric tail check','ratio magnitude is not below one'),
('harmonic','p-series test with p=1',10000,9.787606,0.0001,'diverges',NULL,'fixed term count; no finite infinite-total claim','terms approach zero but the series diverges');
