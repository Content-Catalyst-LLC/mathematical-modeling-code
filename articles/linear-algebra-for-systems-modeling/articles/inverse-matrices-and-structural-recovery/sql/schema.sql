DROP TABLE IF EXISTS inverse_recovery_assumption_registry;
DROP TABLE IF EXISTS inverse_recovery_audit_cases;

CREATE TABLE inverse_recovery_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO inverse_recovery_assumption_registry VALUES
('inverse_matrix','Inverse matrix','A two-sided matrix inverse satisfying A inverse times A equals the identity.','Supports exact recovery of inputs from outputs when the transformation is invertible.','An inverse exists only for square full-rank matrices.'),
('structural_recovery','Structural recovery','Uses the inverse transformation to reconstruct inputs from outputs.','Represents a strong claim that modeled outputs preserve enough information for recovery.','Recovery claims require conditioning data quality and substantive interpretation review.'),
('trivial_null_space','Trivial null space','Only the zero vector maps to zero.','Means no nonzero input direction disappears under the transformation.','A nontrivial null space prevents unique recovery.'),
('condition_number','Condition number','Measures sensitivity of inverse recovery to perturbations.','Shows whether algebraic recovery is numerically stable.','Large condition numbers make recovery fragile even when an inverse exists.'),
('explicit_inverse','Explicit inverse','Computes A inverse directly.','Useful for interpretation and small examples.','Numerical workflows usually prefer solving systems directly with factorizations.'),
('pseudoinverse','Pseudoinverse','Generalizes inverse-like recovery to rectangular or rank-deficient systems.','Supports approximate least-squares or minimum-norm recovery.','Pseudoinverse solutions reflect criteria and assumptions not exact reversal.');

CREATE TABLE inverse_recovery_audit_cases (
    system_name TEXT NOT NULL,
    matrix_size INTEGER NOT NULL,
    determinant REAL NOT NULL,
    invertible INTEGER NOT NULL,
    rank INTEGER NOT NULL,
    nullity INTEGER NOT NULL,
    recovered_solution TEXT NOT NULL,
    residual_norm REAL NOT NULL,
    tolerance REAL NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO inverse_recovery_audit_cases VALUES
('three_constraint_structural_recovery_system',3,2.0,1,3,0,'55.000000,45.000000,35.000000',0.0,0.0000000001,'Inverse recovery is algebraic; practical recovery requires conditioning and model review.');
