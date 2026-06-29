DROP TABLE IF EXISTS stability_assumption_registry;
DROP TABLE IF EXISTS stability_analysis_audit_cases;

CREATE TABLE stability_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO stability_assumption_registry VALUES
('time_model','Time model','Distinguishes discrete-time updates from continuous-time generators.','Determines which eigenvalue stability rule applies.','Do not apply discrete-time and continuous-time stability tests interchangeably.'),
('spectral_radius','Spectral radius','Largest eigenvalue magnitude.','Supports discrete-time asymptotic stability classification.','Nonnormal transient growth and forcing terms may complicate interpretation.'),
('real_part','Eigenvalue real part','Determines continuous-time exponential growth or decay.','Supports continuous-time local stability analysis.','Boundary cases require deeper review.'),
('local_linearization','Local linearization','Uses a Jacobian matrix near equilibrium.','Supports local stability claims around a reference state.','Local stability does not automatically imply global stability.'),
('dominant_mode','Dominant mode','Mode with largest growth or slowest decay signal.','Can shape long-run or near-boundary behavior.','Initial conditions spectral gaps and conditioning affect interpretation.'),
('transient_growth','Transient growth','Short-run amplification can occur even under asymptotic stability.','Important for systems where temporary amplification is consequential.','Eigenvalue-only analysis may be incomplete for nonnormal matrices.');

CREATE TABLE stability_analysis_audit_cases (
    system_name TEXT NOT NULL,
    matrix_entries TEXT NOT NULL,
    eigenvalue_1 REAL NOT NULL,
    eigenvalue_2 REAL NOT NULL,
    spectral_radius REAL NOT NULL,
    largest_real_part REAL NOT NULL,
    discrete_time_classification TEXT NOT NULL,
    continuous_time_classification TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO stability_analysis_audit_cases VALUES
('two_mode_stability_audit','0.820000,0.120000;0.180000,0.760000',0.94,0.64,0.94,0.94,'asymptotically_stable_discrete_time','unstable_continuous_time','Discrete-time and continuous-time rules are not interchangeable.');
