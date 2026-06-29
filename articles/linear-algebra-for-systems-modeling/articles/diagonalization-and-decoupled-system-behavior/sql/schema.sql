DROP TABLE IF EXISTS diagonalization_assumption_registry;
DROP TABLE IF EXISTS diagonalization_audit_cases;

CREATE TABLE diagonalization_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO diagonalization_assumption_registry VALUES
('matrix_definition','Matrix definition','Defines the transformation being diagonalized.','Determines what system behavior the modes can represent.','Diagonalization inherits meaning from matrix construction units weights and time step.'),
('eigenvector_basis','Eigenvector basis','Provides the independent vectors needed for diagonalization.','Defines modal coordinates for the system.','A matrix with too few independent eigenvectors cannot be fully decoupled this way.'),
('diagonal_matrix','Diagonal matrix','Stores eigenvalues as independent mode scalings.','Shows how each mode grows decays persists reverses or disappears.','Diagonal behavior is a coordinate representation not automatic real-world independence.'),
('matrix_powers','Matrix powers','Uses A^t = P D^t P^{-1} when diagonalization applies.','Supports repeated dynamics and long-run behavior analysis.','Initial conditions and spectral gaps affect which modes appear or dominate.'),
('condition_number','Eigenvector matrix conditioning','Measures sensitivity of modal coordinates.','Shows whether decoupled modal analysis may be numerically fragile.','Large condition numbers require caution or alternative decompositions.'),
('reconstruction_error','Reconstruction error','Measures how closely P D P^{-1} reproduces A.','Supports auditability of computed diagonalization.','Small reconstruction error does not guarantee substantive interpretation.');

CREATE TABLE diagonalization_audit_cases (
    system_name TEXT NOT NULL,
    matrix_entries TEXT NOT NULL,
    eigenvector_matrix TEXT NOT NULL,
    diagonal_matrix TEXT NOT NULL,
    reconstruction_error_frobenius REAL NOT NULL,
    spectral_radius REAL NOT NULL,
    dominant_eigenvalue REAL NOT NULL,
    stability_classification TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO diagonalization_audit_cases VALUES
('two_mode_diagonalization_audit','0.796667,0.123333;0.246667,0.673333','1.000000,1.000000;1.000000,-2.000000','0.920000,0.000000;0.000000,0.550000',0.0,0.92,0.92,'all_modes_decay_discrete_time','Diagonalization decouples representation not necessarily real system.');
