DROP TABLE IF EXISTS linear_first_order_assumption_registry;
DROP TABLE IF EXISTS linear_first_order_audit_cases;

CREATE TABLE linear_first_order_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO linear_first_order_assumption_registry VALUES
('state_variable_definition','State variable definition','Defines the quantity governed by the differential equation.','Determines what the model tracks through time.','Unclear state definitions make trajectories uninterpretable.'),
('linear_state_dependence','Linear state dependence','Requires the state variable to enter linearly.','Represents proportional loss damping decay or adjustment.','The proportional-loss assumption may fail near thresholds or saturation.'),
('forcing_term','Forcing term','Represents input or external pressure in the equation.','Models inflow emissions intervention demand or replenishment.','Forcing terms should be measured estimated or clearly labeled as scenarios.'),
('initial_condition','Initial condition','Selects one trajectory from the solution family.','Anchors the scenario to a starting state.','Different starting states can produce different transient behavior.'),
('equilibrium_interpretation','Equilibrium interpretation','Identifies the balance point when input and loss are constant.','Supports long-run systems interpretation.','Equilibrium may change if input loss policy or context changes.'),
('numerical_method','Numerical method','Defines how continuous dynamics are approximated.','Supports reproducible simulation and solver review.','Step size can affect numerical error and apparent stability.');

CREATE TABLE linear_first_order_audit_cases (
    scenario TEXT NOT NULL,
    initial_state REAL NOT NULL,
    input_rate REAL NOT NULL,
    loss_rate REAL NOT NULL,
    equilibrium REAL NOT NULL,
    time_step REAL NOT NULL,
    steps INTEGER NOT NULL,
    method TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO linear_first_order_audit_cases VALUES
('input_loss_balance',20.0,12.0,0.4,30.0,0.1,100,'analytical_vs_explicit_euler','Assumes constant input and proportional loss.');
