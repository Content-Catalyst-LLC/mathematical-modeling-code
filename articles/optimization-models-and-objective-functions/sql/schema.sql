-- Optimization models and objective functions governance schema.

DROP TABLE IF EXISTS optimization_component_guide;
DROP TABLE IF EXISTS optimization_scenario;
DROP TABLE IF EXISTS program;
DROP TABLE IF EXISTS optimization_model_register;
DROP TABLE IF EXISTS optimization_component_type;

CREATE TABLE optimization_component_type (
    component_type TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    typical_failure TEXT NOT NULL
);

CREATE TABLE optimization_model_register (
    record_id INTEGER PRIMARY KEY,
    record_key TEXT NOT NULL,
    component_type TEXT NOT NULL,
    expression TEXT NOT NULL,
    interpretation TEXT NOT NULL,
    review_question TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('active', 'review', 'revise', 'archive')),
    FOREIGN KEY (component_type) REFERENCES optimization_component_type(component_type)
);

CREATE TABLE program (
    program TEXT PRIMARY KEY,
    benefit_per_unit REAL NOT NULL,
    cost_per_unit REAL NOT NULL CHECK (cost_per_unit > 0),
    lower_bound INTEGER NOT NULL CHECK (lower_bound >= 0),
    upper_bound INTEGER NOT NULL CHECK (upper_bound >= lower_bound)
);

CREATE TABLE optimization_scenario (
    scenario TEXT PRIMARY KEY,
    budget REAL NOT NULL CHECK (budget >= 0),
    equity_floor INTEGER NOT NULL CHECK (equity_floor >= 0),
    description TEXT
);

CREATE TABLE optimization_component_guide (
    component_type TEXT PRIMARY KEY,
    meaning TEXT NOT NULL,
    example TEXT NOT NULL,
    review_question TEXT NOT NULL
);

INSERT INTO optimization_component_type VALUES
('decision_variable','Quantity the model can choose.','Variable is not actually controllable.'),
('objective_function','Formal goal to optimize.','Objective omits important values or harms.'),
('constraint','Restriction on feasible choices.','Constraint is missing, incomplete, or unjustified.'),
('parameter','Fixed or estimated value.','Uncertainty is ignored.'),
('feasible_region','Set of allowable choices.','Mathematical feasibility differs from real feasibility.'),
('solver_setting','Algorithm or tolerance.','Solver status or tolerance is not reviewed.'),
('validation_diagnostic','Review of model credibility.','Sensitivity and implementation checks are missing.');

INSERT INTO optimization_model_register(record_key, component_type, expression, interpretation, review_question, status) VALUES
('decision_variables','decision_variable','x_i','Allocation to program i','Are these quantities actually controllable?','active'),
('objective_function','objective_function','maximize sum_i benefit_i * x_i','The model maximizes estimated total benefit','Does total benefit hide distributional concerns?','review'),
('budget_constraint','constraint','sum_i cost_i * x_i <= B','Total cost cannot exceed budget','Are all costs included?','review'),
('equity_floor','constraint','x_i >= equity_floor','Each program receives at least a minimum allocation','Is the floor ethically and operationally justified?','review'),
('upper_bound','constraint','x_i <= u_i','Each program has maximum absorption capacity','Is capacity based on evidence?','review'),
('solver_method','solver_setting','enumeration','Small integer model solved by exhaustive feasible-choice enumeration','Is enumeration appropriate for this model scale?','active');

INSERT INTO program VALUES
('housing',11,7,0,8),
('health',13,8,0,8),
('transport',8,5,0,8),
('resilience',10,6,0,8);

INSERT INTO optimization_scenario VALUES
('baseline',75,1,'Baseline budget with low equity floor'),
('tight_budget',55,1,'Reduced budget scenario'),
('higher_floor',75,3,'Higher minimum allocation scenario');

INSERT INTO optimization_component_guide VALUES
('decision_variable','Quantity the model can choose','x_i','Is it actually controllable?'),
('objective_function','Formal goal to optimize','maximize benefit','What does this objective omit?'),
('constraint','Restriction on feasible choices','budget <= B','Is the constraint complete and justified?'),
('parameter','Fixed or estimated value','cost_i','How uncertain is it?'),
('feasible_region','Set of allowable choices','F','Does feasibility match real implementation?'),
('solver_setting','Algorithm or tolerance','enumeration or MILP','Is the solver appropriate?'),
('validation_diagnostic','Review of model credibility','sensitivity report','Does the solution remain stable?');
