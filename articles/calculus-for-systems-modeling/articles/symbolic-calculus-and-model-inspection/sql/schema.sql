DROP TABLE IF EXISTS symbolic_model_inspection_registry;
DROP TABLE IF EXISTS symbolic_expression_records;

CREATE TABLE symbolic_model_inspection_registry (
    inspection_key TEXT PRIMARY KEY,
    inspection_name TEXT NOT NULL,
    symbolic_operation TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO symbolic_model_inspection_registry VALUES
('original_expression','Original expression','Record the model expression before transformation.','Preserves the structure being inspected.','Do not overwrite original expressions with simplified forms.'),
('domain_assumptions','Domain assumptions','Record valid variable and parameter ranges.','Prevents expressions from being interpreted outside their model scope.','Simplification can become misleading if domains are not documented.'),
('derivative_check','Derivative check','Compute symbolic derivatives.','Reveals marginal effects, sensitivities, and local feedback.','Derivative signs depend on parameter regimes and domains.'),
('limit_check','Limit check','Evaluate boundary and asymptotic behavior.','Reveals singularities, thresholds, and long-run implications.','Limits should be interpreted within model assumptions.'),
('equilibrium_check','Equilibrium check','Solve rate expressions equal to zero.','Identifies candidate steady states.','Equilibria require stability and domain review.'),
('jacobian_check','Jacobian check','Compute first partial derivative matrix.','Inspects local coupling and stability in multivariable systems.','Local linearization does not replace nonlinear analysis.');

CREATE TABLE symbolic_expression_records (
    item TEXT PRIMARY KEY,
    expression TEXT NOT NULL,
    interpretation TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO symbolic_expression_records VALUES
('rate_expression','r*x*(1 - x/K)','Logistic growth rate expression.','Assumes documented domain conditions including K not equal to zero.'),
('first_derivative','r - 2*r*x/K','Marginal growth effect declines as x increases.','Derivative interpretation depends on positive-domain assumptions.'),
('second_derivative','-2*r/K','Curvature is negative when r and K are positive.','Curvature describes model structure, not empirical validity.'),
('equilibria','x = 0 or x = K','Equilibria occur where the rate expression equals zero.','Equilibria require domain and stability review.'),
('limit_at_capacity','0','Growth rate approaches zero as x approaches carrying capacity.','Boundary behavior should be checked against modeled assumptions.');
