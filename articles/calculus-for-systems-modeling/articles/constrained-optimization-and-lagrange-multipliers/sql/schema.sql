DROP TABLE IF EXISTS constrained_optimization_assumption_registry;
DROP TABLE IF EXISTS constrained_optimization_cases;

CREATE TABLE constrained_optimization_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO constrained_optimization_assumption_registry VALUES
('objective_definition','Objective definition','Specifies what is being minimized or maximized.','Determines what the optimization treats as success.','Optimization results inherit omissions and value choices in the objective.'),
('constraint_definition','Constraint definition','Defines the feasible set.','Represents resource capacity conservation legal policy or ethical limits.','Hidden constraints can make a formal optimum infeasible in practice.'),
('feasible_region','Feasible region','Identifies allowed states.','Separates implementable choices from unconstrained mathematical directions.','Feasible regions depend on boundary definitions and assumptions.'),
('lagrange_multiplier','Lagrange multiplier','Balances objective and constraint gradients at candidate optima.','Supports local shadow-value and tradeoff interpretation.','Multiplier meaning depends on units scaling and local validity.'),
('constraint_status','Constraint status','Identifies active inactive violated or near-active constraints.','Shows which boundaries shape feasible improvement.','Inactive constraints may become active under uncertainty or scenario change.'),
('second_order_feasibility','Second-order feasibility','Checks curvature along feasible directions.','Helps classify constrained local candidates.','Unconstrained Hessian classification may be misleading.');

CREATE TABLE constrained_optimization_cases (
    x REAL NOT NULL,
    y REAL NOT NULL,
    objective_value REAL NOT NULL,
    constraint_value REAL NOT NULL,
    constraint_target REAL NOT NULL,
    constraint_residual REAL NOT NULL,
    lambda_value REAL NOT NULL,
    gradient_f_x REAL NOT NULL,
    gradient_f_y REAL NOT NULL,
    gradient_g_x REAL NOT NULL,
    gradient_g_y REAL NOT NULL,
    stationarity_residual_norm REAL NOT NULL,
    feasible INTEGER NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO constrained_optimization_cases VALUES
(8,4,96,12,12,0,16,16,16,1,1,0,1,'Multiplier interpretation is local and unit-dependent.'),
(12,6,216,18,18,0,24,24,24,1,1,0,1,'Multiplier interpretation is local and unit-dependent.'),
(16,8,384,24,24,0,32,32,32,1,1,0,1,'Multiplier interpretation is local and unit-dependent.');
