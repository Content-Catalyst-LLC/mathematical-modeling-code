DROP TABLE IF EXISTS power_series_assumption_registry;
CREATE TABLE power_series_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO power_series_assumption_registry VALUES
('expansion_center','Expansion center','Defines the point around which powers are measured.','Identifies the local operating condition for interpretation.','A power-series approximation should not be interpreted without knowing its center.'),
('radius_of_convergence','Radius of convergence','Defines where the infinite series converges around the center.','Sets a mathematical boundary for functional representation.','Computing outside the convergence radius does not justify interpretation.'),
('coefficient_rule','Coefficient rule','Explains how coefficients are generated.','Distinguishes Taylor-derived coefficients from fitted or assumed coefficients.','Coefficients without provenance are difficult to audit.'),
('truncation_order','Truncation order','Records how many terms are retained in the finite approximation.','Separates the computed polynomial from the infinite representation.','A finite truncation is not the same as the full function.'),
('remainder_logic','Remainder logic','Documents the omitted terms or error estimate.','Supports responsible use of finite polynomial approximations.','A polynomial approximation should not be trusted without error or validity review.'),
('calculator_interface','Calculator interface','Provides reusable command-line computational logic.','Prepares calculator functions for future website interfaces.','Calculator outputs require interpretation and assumption review.');
