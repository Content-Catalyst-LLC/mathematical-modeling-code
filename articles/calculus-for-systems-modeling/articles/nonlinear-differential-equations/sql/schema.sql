DROP TABLE IF EXISTS nonlinear_assumption_registry;
DROP TABLE IF EXISTS nonlinear_audit_cases;

CREATE TABLE nonlinear_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO nonlinear_assumption_registry VALUES
('nonlinear_rate_law','Nonlinear rate law','Defines how the state enters the derivative through nonlinear terms.','Represents saturation interaction amplification thresholds or changing response.','The nonlinear form should be tied to mechanism evidence or explicit scenario design.'),
('parameter_meaning','Parameter meaning','Controls growth carrying capacity threshold interaction or feedback strength.','Determines how strongly the system responds under the modeled structure.','Parameter uncertainty can strongly alter nonlinear trajectories.'),
('equilibrium_points','Equilibrium points','Identify states where the rate of change is zero.','Support interpretation of balance extinction persistence saturation or regime state.','Equilibria may be unstable outside the meaningful domain or conditional on assumptions.'),
('threshold_definition','Threshold definition','Defines where the rate law changes sign or structure.','Represents activation tipping failure intervention or regime change.','Thresholds should be observed estimated policy-defined or clearly hypothetical.'),
('domain_constraints','Domain constraints','Restrict states to meaningful values such as nonnegative or bounded intervals.','Preserve physical ecological social or institutional interpretability.','Numerical solvers can produce invalid states if constraints are ignored.'),
('numerical_method','Numerical method','Defines how the nonlinear equation is approximated over time.','Supports reproducible simulation and solver review.','Step size and solver choice can create misleading nonlinear behavior.');

CREATE TABLE nonlinear_audit_cases (
    scenario TEXT NOT NULL,
    initial_state REAL NOT NULL,
    parameter_a REAL NOT NULL,
    parameter_b REAL NOT NULL,
    parameter_c REAL NOT NULL,
    time_step REAL NOT NULL,
    steps INTEGER NOT NULL,
    method TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO nonlinear_audit_cases VALUES
('logistic_growth',10.0,0.6,100.0,0.0,0.05,300,'explicit_euler','Logistic growth assumes a fixed carrying capacity and smooth density limitation.'),
('bistable_threshold',0.35,0.4,0.0,0.0,0.05,300,'explicit_euler','Threshold behavior is illustrative and should not be interpreted without evidence for the threshold.');
