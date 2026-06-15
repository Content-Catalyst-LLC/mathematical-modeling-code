DROP TABLE IF EXISTS stability_assumption_registry;
DROP TABLE IF EXISTS stability_audit_cases;

CREATE TABLE stability_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO stability_assumption_registry VALUES
('equilibrium_candidate','Equilibrium candidate','Identifies a state where the modeled rate of change is zero.','Represents a possible balance point boundary state threshold or operating condition.','Equilibrium candidates must be checked against the meaningful domain of the model.'),
('local_stability','Local stability','Describes behavior after small perturbations near equilibrium.','Indicates whether small disturbances tend to shrink grow or remain inconclusive.','Local stability does not guarantee global resilience.'),
('linearization_method','Linearization method','Approximates nonlinear behavior near equilibrium using derivatives or Jacobians.','Supports local interpretation of recovery instability oscillation or saddle behavior.','Linearization may fail when first derivatives vanish or nonlinear terms dominate.'),
('domain_constraints','Domain constraints','Restrict states to meaningful values such as nonnegative or bounded intervals.','Preserve physical ecological social or institutional interpretability.','Mathematically valid equilibria may be invalid outside the system domain.'),
('basin_of_attraction','Basin of attraction','Identifies initial conditions that approach a stable state or attractor.','Supports resilience threshold and recovery interpretation.','Basin boundaries are often uncertain and may depend on unmodeled variables.'),
('numerical_method','Numerical method','Defines how equilibrium and local dynamics are explored computationally.','Supports reproducible simulation initial-condition sweeps and solver review.','Step size and solver choice can create misleading stability behavior.');

CREATE TABLE stability_audit_cases (
    scenario TEXT NOT NULL,
    equilibrium REAL NOT NULL,
    derivative_value REAL NOT NULL,
    stability TEXT NOT NULL,
    domain_min REAL NOT NULL,
    domain_max REAL NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO stability_audit_cases VALUES
('logistic_growth',0.0,0.6,'locally_unstable',0.0,100.0,'Logistic stability assumes fixed carrying capacity and smooth density limitation.'),
('logistic_growth',100.0,-0.6,'locally_stable',0.0,100.0,'Logistic stability assumes fixed carrying capacity and smooth density limitation.'),
('bistable_threshold',0.0,-0.4,'locally_stable',0.0,1.0,'Threshold stability depends on the assumed threshold and domain.'),
('bistable_threshold',0.4,0.24,'locally_unstable',0.0,1.0,'Threshold stability depends on the assumed threshold and domain.'),
('bistable_threshold',1.0,-0.6,'locally_stable',0.0,1.0,'Threshold stability depends on the assumed threshold and domain.');
