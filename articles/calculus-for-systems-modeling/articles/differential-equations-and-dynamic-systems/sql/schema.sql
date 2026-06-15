DROP TABLE IF EXISTS differential_equation_assumption_registry;
DROP TABLE IF EXISTS dynamic_system_audit_cases;

CREATE TABLE differential_equation_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO differential_equation_assumption_registry VALUES
('state_variable_definition','State variable definition','Defines the quantity whose change is modeled.','Determines what the dynamic system actually tracks.','Unclear state variables make trajectories uninterpretable.'),
('rate_law','Rate law','Defines how the derivative depends on state time inputs or parameters.','Represents the mechanism of change.','A convenient equation is not necessarily a credible mechanism.'),
('initial_condition','Initial condition','Sets the starting state for trajectory generation.','Determines where the modeled system begins.','Different initial states may produce different outcomes.'),
('boundary_condition','Boundary condition','Defines behavior at the edge of a spatial domain.','Controls interaction with surroundings.','Unrealistic boundaries can distort spatial behavior.'),
('parameter_values','Parameter values','Control growth decay coupling forcing and sensitivity.','Represent empirical estimates assumptions or scenario settings.','Uncertain parameters should be tested for sensitivity.'),
('numerical_method','Numerical method','Defines how the continuous equation is approximated.','Shapes the computed trajectory.','Step size stiffness and solver tolerance can change results.'),
('validity_scope','Validity scope','Defines where the equation is intended to apply.','Prevents overextending the model beyond assumptions.','Dynamic equations can mislead when used outside their domain.');

CREATE TABLE dynamic_system_audit_cases (
    scenario TEXT NOT NULL,
    model_type TEXT NOT NULL,
    initial_state REAL NOT NULL,
    growth_rate REAL NOT NULL,
    carrying_capacity REAL,
    time_step REAL NOT NULL,
    steps INTEGER NOT NULL,
    method TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO dynamic_system_audit_cases VALUES
('exponential_growth','dx_dt_equals_r_x',10.0,0.35,NULL,0.1,100,'explicit_euler','Exponential growth assumes no capacity constraint.'),
('logistic_growth','dx_dt_equals_r_x_one_minus_x_over_K',10.0,0.35,100.0,0.1,100,'explicit_euler','Logistic growth assumes a fixed carrying capacity.');
