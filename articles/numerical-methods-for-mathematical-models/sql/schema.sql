-- Numerical methods for mathematical models governance schema.

DROP TABLE IF EXISTS numerical_component_guide;
DROP TABLE IF EXISTS solver_scenario;
DROP TABLE IF EXISTS numerical_method_register;
DROP TABLE IF EXISTS numerical_component_type;

CREATE TABLE numerical_component_type (
    component_type TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    typical_failure TEXT NOT NULL
);

CREATE TABLE numerical_method_register (
    record_id INTEGER PRIMARY KEY,
    record_key TEXT NOT NULL,
    component_type TEXT NOT NULL,
    numerical_structure TEXT NOT NULL,
    interpretation TEXT NOT NULL,
    review_question TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('active', 'review', 'revise', 'archive')),
    FOREIGN KEY (component_type) REFERENCES numerical_component_type(component_type)
);

CREATE TABLE solver_scenario (
    scenario_id INTEGER PRIMARY KEY,
    scenario TEXT NOT NULL,
    initial_stock REAL NOT NULL CHECK (initial_stock >= 0),
    growth_rate REAL NOT NULL CHECK (growth_rate >= 0),
    carrying_capacity REAL NOT NULL CHECK (carrying_capacity > 0),
    extraction REAL NOT NULL CHECK (extraction >= 0),
    horizon REAL NOT NULL CHECK (horizon > 0),
    step_size REAL NOT NULL CHECK (step_size > 0)
);

CREATE TABLE numerical_component_guide (
    component_type TEXT PRIMARY KEY,
    meaning TEXT NOT NULL,
    example TEXT NOT NULL,
    review_question TEXT NOT NULL
);

INSERT INTO numerical_component_type VALUES
('time_step_method','Algorithm for advancing state.','Method is unsuitable for the model.'),
('discretization','Finite representation of time or space.','Results depend on hidden resolution choices.'),
('solver_tolerance','Stopping or accuracy threshold.','Tolerance is too loose for intended use.'),
('convergence_diagnostic','Evidence that refinement stabilizes results.','Convergence is assumed but not checked.'),
('stability_diagnostic','Evidence that errors do not explode.','Numerical instability is mistaken for model behavior.'),
('state_constraint','Allowed state domain.','Constraints hide numerical overshoot.'),
('validation_diagnostic','Credibility check.','Numerical accuracy is confused with model validity.');

INSERT INTO numerical_method_register(record_key, component_type, numerical_structure, interpretation, review_question, status) VALUES
('euler_step','time_step_method','R_next = R + h * f(R)','Euler stepping approximates continuous resource dynamics','Are results stable under smaller step sizes?','review'),
('step_size','discretization','h in {1.0 0.5 0.25 0.1}','Step size controls time discretization','Does the conclusion depend on step size?','review'),
('convergence_diagnostic','convergence_diagnostic','compare_final_stock_across_h','Convergence is assessed by comparing refined approximations','Do results stabilize as h decreases?','active'),
('nonnegative_constraint','state_constraint','R = max(0 R)','Resource stock is constrained to remain nonnegative','Does the constraint hide numerical overshoot?','review'),
('solver_status','validation_diagnostic','residual_and_known_case_checks','Diagnostic evidence supports numerical credibility','Are solver diagnostics preserved with outputs?','review'),
('method_comparison','stability_diagnostic','euler_vs_refined_euler','Alternative approximations should be compared','Does method choice materially affect the conclusion?','review');

INSERT INTO solver_scenario(scenario, initial_stock, growth_rate, carrying_capacity, extraction, horizon, step_size) VALUES
('resource_dynamics',70.0,0.18,100.0,6.0,50.0,1.0),
('resource_dynamics',70.0,0.18,100.0,6.0,50.0,0.5),
('resource_dynamics',70.0,0.18,100.0,6.0,50.0,0.25),
('resource_dynamics',70.0,0.18,100.0,6.0,50.0,0.1);

INSERT INTO numerical_component_guide VALUES
('time_step_method','Algorithm for advancing state','Euler method','Is the method suitable?'),
('discretization','Finite representation of time or space','step size h','Are results sensitive to resolution?'),
('solver_tolerance','Stopping or accuracy threshold','residual tolerance','Is tolerance tight enough?'),
('convergence_diagnostic','Evidence that refinement stabilizes results','step-size comparison','Do outputs converge?'),
('stability_diagnostic','Evidence that errors do not explode','perturbation test','Is the method stable?'),
('state_constraint','Allowed state domain','R nonnegative','Does constraint hide numerical artifacts?'),
('validation_diagnostic','Credibility check','known-case comparison','Is output valid for intended use?');
