DROP TABLE IF EXISTS implicit_relationship_registry;

CREATE TABLE implicit_relationship_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO implicit_relationship_registry VALUES
('constraint_equation','Constraint equation','An implicit relationship is written as F(x,y)=0 or F(x,p)=0.','Identifies the relationship that must remain satisfied.','The derivative is meaningful only relative to the stated constraint.'),
('regularity_condition','Regularity condition','Local solvability requires a nonzero partial derivative or invertible Jacobian block.','Supports interpretation of one variable as locally adjusting to another.','If the condition fails, the derivative may be undefined, unstable, or branch-dependent.'),
('coadjustment_rate','Co-adjustment rate','For F(x,y)=0, dy/dx=-F_x/F_y when F_y is nonzero.','Shows how variables must move together to preserve the relationship.','Co-adjustment is not the same as independent causal response.'),
('equilibrium_sensitivity','Equilibrium sensitivity','For G(x,p)=0, dx/dp=-G_p/G_x when G_x is nonzero.','Shows how an equilibrium shifts when a parameter changes.','Sensitivity can become unstable near singular or bifurcation points.'),
('jacobian_conditioning','Jacobian conditioning','Vector systems require solving F_x S=-F_p.','Supports multivariable coupled-system sensitivity analysis.','Ill-conditioned Jacobians can make numerical sensitivity unreliable.');
