DROP TABLE IF EXISTS continuous_model_governance_registry;
DROP TABLE IF EXISTS continuous_model_risks;

CREATE TABLE continuous_model_governance_registry (
    registry_key TEXT PRIMARY KEY,
    registry_name TEXT NOT NULL,
    analytical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO continuous_model_governance_registry VALUES
('continuity_assumption','Continuity assumption','Documents which variables, rates, or fields are treated as smooth.','Makes the model approximation explicit.','Smooth mathematical output does not prove smooth system behavior.'),
('threshold_check','Threshold check','Tests whether behavior changes near critical values.','Prevents regime changes from being smoothed away.','A model without threshold review may understate fragility.'),
('equilibrium_review','Equilibrium review','Examines whether steady-state analysis hides transition dynamics.','Separates equilibrium existence from path safety and stability.','An equilibrium is a mathematical condition, not a complete interpretation.'),
('aggregation_review','Aggregation review','Checks whether averages hide important heterogeneity.','Protects against misleading aggregate interpretation.','An average can hide local stress, inequality, or bottlenecks.'),
('solver_diagnostic','Solver diagnostic','Records numerical method, tolerance, convergence status, and warnings.','Separates computed output from validated explanation.','A successful solver run does not prove model validity.'),
('claim_boundary','Claim boundary','Defines where the continuous approximation can be responsibly used.','Prevents smooth models from being overextended.','Continuous model claims must be tied to scope, evidence, and diagnostics.');

CREATE TABLE continuous_model_risks (
    record_id TEXT PRIMARY KEY,
    risk_name TEXT NOT NULL,
    risk_pattern TEXT NOT NULL,
    possible_consequence TEXT NOT NULL,
    governance_response TEXT NOT NULL,
    review_status TEXT NOT NULL
);

INSERT INTO continuous_model_risks VALUES
('risk_false_smoothness','false_smoothness','smooth curve hides structural breaks','threshold failure or event dynamics are missed','test for breaks and document discontinuities','review');
INSERT INTO continuous_model_risks VALUES
('risk_threshold','hidden_threshold','critical transition is omitted or smoothed','fragility is understated','run threshold and scenario checks','review');
INSERT INTO continuous_model_risks VALUES
('risk_equilibrium','equilibrium_bias','steady state is overinterpreted','transition costs and delays are hidden','analyze trajectories and stability','review');
INSERT INTO continuous_model_risks VALUES
('risk_aggregation','aggregation_risk','average hides heterogeneity','local stress or inequality is hidden','inspect distributions and subgroups','review');
INSERT INTO continuous_model_risks VALUES
('risk_solver','solver_confidence','successful computation is mistaken for validation','numerical artifact appears as insight','record solver method tolerance convergence and warnings','review');
