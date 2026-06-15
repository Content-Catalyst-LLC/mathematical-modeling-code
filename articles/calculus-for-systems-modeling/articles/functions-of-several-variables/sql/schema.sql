DROP TABLE IF EXISTS multivariable_function_assumption_registry;
DROP TABLE IF EXISTS multivariable_function_cases;

CREATE TABLE multivariable_function_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO multivariable_function_assumption_registry VALUES
('input_definition','Input definition','Defines each variable in the input space.','Clarifies what each input represents in the modeled system.','A multivariable function should not be interpreted without clear input definitions.'),
('domain_region','Domain region','Defines the set of input combinations where the function is defined.','Separates mathematically computable inputs from meaningful system scenarios.','Outputs outside the modeling domain may be invalid even when the formula computes.'),
('feasible_region','Feasible region','Records constraints on allowable input combinations.','Prevents impossible scenarios from being treated as valid model outputs.','Inputs may be mathematically valid but infeasible under physical budgetary or ethical constraints.'),
('interaction_structure','Interaction structure','Identifies whether input effects are additive multiplicative nonlinear or conditional.','Clarifies whether variables act independently or jointly.','Omitted interactions may distort system interpretation.'),
('local_validity','Local validity','Defines where the multivariable relationship is intended to hold.','Prevents local response surfaces from being treated as global system truth.','A function calibrated in one region may not be valid under extrapolation.');

CREATE TABLE multivariable_function_cases (
    x REAL NOT NULL,
    y REAL NOT NULL,
    output REAL NOT NULL,
    feasible INTEGER NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO multivariable_function_cases VALUES
(2,4,18,1,''),
(8,4,48,0,'Input combination is outside the feasible region.'),
(6,3,33,1,'');
