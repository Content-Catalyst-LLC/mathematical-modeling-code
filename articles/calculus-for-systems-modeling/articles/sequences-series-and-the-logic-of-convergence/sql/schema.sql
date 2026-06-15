DROP TABLE IF EXISTS convergence_assumption_registry;
DROP TABLE IF EXISTS series_audit_records;

CREATE TABLE convergence_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO convergence_assumption_registry VALUES
('sequence_definition','Sequence definition','Defines the ordered values being analyzed.','Clarifies whether values represent states, estimates, terms, errors, or iterations.','A convergence claim is not auditable unless the sequence is defined.'),
('partial_sum_definition','Partial sum definition','Defines finite cumulative totals before the infinite limit.','Keeps computed finite sums separate from infinite-series claims.','A partial sum should not be reported as an infinite total without convergence evidence.'),
('stopping_rule','Stopping rule','Explains why the computation ended.','Documents whether stopping was based on term count, tolerance, error bound, or runtime.','A stopped computation is not necessarily a converged computation.'),
('remainder_bound','Remainder bound','Estimates the uncomputed tail contribution.','Supports responsible interpretation of finite approximations.','Small latest term does not always imply small remainder.'),
('absolute_convergence','Absolute convergence','Checks whether the magnitudes of terms form a convergent series.','Distinguishes bounded total magnitude from net cancellation.','Conditional convergence can hide large gross activity.');

CREATE TABLE series_audit_records (
    series_name TEXT PRIMARY KEY,
    n_terms INTEGER NOT NULL,
    last_term REAL NOT NULL,
    partial_sum REAL NOT NULL,
    convergence_classification TEXT NOT NULL,
    stopping_rule TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO series_audit_records VALUES
('geometric_r_0.6',25,0.000284,24.999574,'convergent geometric series','fixed term count with analytic tail check',''),
('geometric_r_1.05',25,32.251002,477.270547,'divergent or inconclusive','fixed term count with analytic tail check','geometric ratio does not support convergence'),
('harmonic',10000,0.000100,9.787606,'divergent despite terms approaching zero','fixed term count; no finite limiting total','small last term does not imply finite accumulated total');
