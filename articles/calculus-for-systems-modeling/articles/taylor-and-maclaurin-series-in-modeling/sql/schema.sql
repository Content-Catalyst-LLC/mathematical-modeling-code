DROP TABLE IF EXISTS taylor_approximation_assumption_registry;
DROP TABLE IF EXISTS taylor_approximation_cases;

CREATE TABLE taylor_approximation_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO taylor_approximation_assumption_registry VALUES
('expansion_center','Expansion center','Defines the point where derivative information is taken.','Identifies the local reference state for interpretation.','A Taylor approximation should not be interpreted without knowing its center.'),
('approximation_order','Approximation order','Records the highest retained polynomial degree.','Shows which derivative information was included or omitted.','A first-order approximation may miss important curvature or nonlinear response.'),
('derivative_provenance','Derivative provenance','Documents how derivative values or coefficients were obtained.','Separates symbolic numerical estimated and assumed derivative information.','Derivative coefficients without provenance are difficult to audit.'),
('remainder_logic','Remainder logic','Describes the omitted terms or error estimate.','Supports responsible interpretation of finite Taylor polynomials.','A Taylor polynomial should not be trusted without error or validity review.'),
('local_validity','Local validity','Defines the region where the approximation is intended to apply.','Prevents local polynomial behavior from being treated as global system truth.','Large shocks thresholds and regime changes may invalidate local approximation.'),
('calculator_interface','Calculator interface','Provides reusable command-line computational logic.','Prepares calculator functions for future website interfaces.','Calculator outputs require interpretation and assumption review.');

CREATE TABLE taylor_approximation_cases (
    function_name TEXT NOT NULL,
    center REAL NOT NULL,
    x_value REAL NOT NULL,
    approximation_order INTEGER NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO taylor_approximation_cases VALUES
('exp(x)',0,0.5,5,''),
('exp(x)',0,3.0,10,'Evaluation is far from the Maclaurin center; review truncation error carefully.'),
('sin(x)',0,1.0,5,'');
