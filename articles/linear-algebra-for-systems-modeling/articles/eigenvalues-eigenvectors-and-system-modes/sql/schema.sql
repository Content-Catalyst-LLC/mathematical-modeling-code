DROP TABLE IF EXISTS eigenstructure_assumption_registry;
DROP TABLE IF EXISTS eigenstructure_audit_cases;

CREATE TABLE eigenstructure_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO eigenstructure_assumption_registry VALUES
('matrix_definition','Matrix definition','Defines the transformation whose eigenstructure is analyzed.','Determines what system behavior the modes can represent.','Eigenmodes inherit meaning from matrix construction units and weights.'),
('eigenvalue','Eigenvalue','Scaling factor along an eigenvector direction.','Represents growth decay persistence reversal or oscillatory structure.','Eigenvalue meaning depends on time scale model type and transformation definition.'),
('eigenvector','Eigenvector','Invariant direction of a linear transformation.','Represents a system mode or pattern that evolves by scaling.','Eigenvectors are not automatically causal mechanisms.'),
('spectral_radius','Spectral radius','Largest eigenvalue magnitude.','Often controls asymptotic behavior in repeated linear systems.','Nonnormal matrices may have important transient behavior not captured by eigenvalues alone.'),
('dominant_mode','Dominant mode','Mode associated with the largest eigenvalue magnitude.','May dominate long-run behavior under suitable assumptions.','Dominance depends on initial conditions spectral gap and model validity.'),
('eigenpair_residual','Eigenpair residual','Measures how well Av equals lambda v numerically.','Supports auditability of computed eigenvalues and eigenvectors.','Small numerical residual does not guarantee substantive interpretation.');

CREATE TABLE eigenstructure_audit_cases (
    system_name TEXT NOT NULL,
    matrix_entries TEXT NOT NULL,
    trace REAL NOT NULL,
    determinant REAL NOT NULL,
    eigenvalue_1 REAL NOT NULL,
    eigenvalue_2 REAL NOT NULL,
    spectral_radius REAL NOT NULL,
    dominant_eigenvalue REAL NOT NULL,
    stability_classification TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO eigenstructure_audit_cases VALUES
('two_sector_mode_audit','0.820000,0.120000;0.180000,0.760000',1.58,0.6016,0.94,0.64,0.94,0.94,'asymptotically_damped_discrete_time','Eigenvalues describe modes of the specified matrix not automatic causal mechanisms.');
