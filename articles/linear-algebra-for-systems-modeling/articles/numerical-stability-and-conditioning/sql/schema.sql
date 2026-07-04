DROP TABLE IF EXISTS numerical_stability_governance_registry;
DROP TABLE IF EXISTS stability_conditioning_audit_cases;

CREATE TABLE numerical_stability_governance_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    computational_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO numerical_stability_governance_registry VALUES
('floating_point_precision','Floating-point precision','Defines how real numbers are approximated by finite precision arithmetic.','Controls rounding behavior tolerance needs and reproducibility.','Computed precision should not be mistaken for real-world certainty.'),
('conditioning','Conditioning','Measures sensitivity of the mathematical problem to input perturbations.','Determines whether small data changes can strongly alter outputs.','Ill-conditioned outputs require sensitivity testing and cautious interpretation.'),
('condition_number','Condition number','Quantifies relative sensitivity using a matrix norm and inverse behavior.','Provides a diagnostic for numerical fragility.','High condition numbers can make small residuals misleading.'),
('residual_norm','Residual norm','Measures how well a computed solution satisfies the original equation.','Checks solver output against the modeled system.','A small residual alone does not guarantee small forward error.'),
('solver_choice','Solver choice','Defines the algorithm used to solve factor approximate or iterate.','Shapes numerical stability runtime and diagnostic behavior.','Solver choice should match matrix structure conditioning sparsity and accuracy needs.'),
('scaling','Scaling','Defines row column variable unit or feature transformations.','Can improve numerical behavior while changing interpretive coordinates.','Scaling choices should be recorded and interpreted in relation to original units.'),
('perturbation_testing','Perturbation testing','Tests output sensitivity under small input or coefficient changes.','Connects numerical sensitivity to modeling uncertainty.','Outputs that shift dramatically under small perturbations should not be overinterpreted.'),
('responsible_use','Responsible use','Defines how numerical limits uncertainty diagnostics and model assumptions are communicated.','Prevents computed output from being treated as stronger evidence than it is.','Numerical diagnostics should accompany consequential model results.');

CREATE TABLE stability_conditioning_audit_cases (
    model_name TEXT NOT NULL,
    matrix_case TEXT NOT NULL,
    matrix_shape TEXT NOT NULL,
    determinant REAL NOT NULL,
    condition_number_proxy REAL NOT NULL,
    solution_norm REAL NOT NULL,
    residual_norm REAL NOT NULL,
    relative_residual REAL NOT NULL,
    perturbation_size REAL NOT NULL,
    perturbed_solution_change REAL NOT NULL,
    stability_status TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO stability_conditioning_audit_cases VALUES
('numerical_stability_conditioning_audit','well_conditioned_system','2x2',5.75,2.10,0.34,0.0,0.0,0.00001,0.000004,'stable_under_demo_threshold','Residuals should be interpreted alongside conditioning scaling perturbation sensitivity solver method precision and model purpose.'),
('numerical_stability_conditioning_audit','ill_conditioned_system','2x2',0.00000001,399920000.0,50000000.0,0.0,0.0,0.00001,2000.0,'review_required_ill_conditioned','Residuals should be interpreted alongside conditioning scaling perturbation sensitivity solver method precision and model purpose.');
