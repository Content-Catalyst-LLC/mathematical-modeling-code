DROP TABLE IF EXISTS least_squares_assumption_registry;
DROP TABLE IF EXISTS least_squares_audit_cases;

CREATE TABLE least_squares_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO least_squares_assumption_registry VALUES
('overdetermined_system','Overdetermined system','A linear system with more equations than unknowns.','Represents many observations measurements or constraints used to estimate fewer unknowns.','Extra equations may improve evidence or expose inconsistency.'),
('residual','Residual','The difference between observed and fitted values.','Shows what the model fails to satisfy or explain.','Residual patterns should be reviewed not merely minimized.'),
('least_squares_objective','Least-squares objective','Minimizes the squared Euclidean norm of residuals.','Chooses the best squared-error approximation under the model.','Squared-error loss may not match every decision or error structure.'),
('projection','Projection','Maps the observed vector to the closest point in the column space.','Shows the closest output the model can produce.','Distance depends on scaling weighting and norm choice.'),
('normal_equations','Normal equations','The system A transpose A x equals A transpose b.','Connects least squares to residual orthogonality.','Normal equations may worsen conditioning in numerical workflows.'),
('qr_or_svd','QR or SVD solver','Factorization-based methods for stable least-squares computation.','Support rank conditioning and residual diagnostics.','Solver choice should be documented for reproducibility.');

CREATE TABLE least_squares_audit_cases (
    system_name TEXT NOT NULL,
    row_count INTEGER NOT NULL,
    column_count INTEGER NOT NULL,
    overdetermined INTEGER NOT NULL,
    rank INTEGER NOT NULL,
    solution TEXT NOT NULL,
    fitted_values TEXT NOT NULL,
    residuals TEXT NOT NULL,
    residual_norm REAL NOT NULL,
    solver_method TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO least_squares_audit_cases VALUES
('four_observation_linear_calibration',4,2,1,2,'0.850000,1.040000','1.890000,2.930000,3.970000,5.010000','0.110000,-0.030000,0.130000,0.090000',0.191311,'normal equations teaching example','Least squares minimizes residuals but model meaning requires review.');
