DROP TABLE IF EXISTS approximation_assumption_registry;
DROP TABLE IF EXISTS approximation_error_cases;

CREATE TABLE approximation_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO approximation_assumption_registry VALUES
('approximation_method','Approximation method','Identifies the mathematical simplification used.','Clarifies whether the result comes from truncation discretization linearization or another approximation.','A model result should not be interpreted without knowing the approximation method.'),
('truncation_order','Truncation order','Records where a finite approximation stops.','Identifies which terms steps or mechanisms were retained.','Truncation should be reported with error or remainder logic.'),
('step_size','Step size','Defines the resolution of a numerical approximation.','Controls the local scale of discretization in derivative integral or dynamic workflows.','A step size that is too large may miss important system behavior.'),
('error_measure','Error measure','Defines whether error is absolute relative estimated bounded or empirical.','Connects numerical accuracy to modeling interpretation.','Error should be reported in a scale meaningful for the modeling purpose.'),
('local_validity_region','Local validity region','Defines where the approximation is intended to hold.','Prevents local approximations from becoming global claims.','Large shocks thresholds and regime changes may invalidate local approximations.');

CREATE TABLE approximation_error_cases (
    method TEXT NOT NULL,
    function_name TEXT NOT NULL,
    center REAL NOT NULL,
    x_value REAL NOT NULL,
    approximation_order INTEGER NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO approximation_error_cases VALUES
('Maclaurin truncation','exp(x)',0,0.5,5,''),
('Maclaurin truncation','exp(x)',0,1.0,10,''),
('Maclaurin truncation','exp(x)',0,3.0,10,'Evaluation is far from the expansion center; review local validity.');
