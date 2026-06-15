DROP TABLE IF EXISTS coupled_system_assumption_registry;
DROP TABLE IF EXISTS coupled_system_audit_cases;

CREATE TABLE coupled_system_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO coupled_system_assumption_registry VALUES
('state_vector_definition','State vector definition','Defines all state variables governed by the system.','Determines what the model treats as dynamically relevant.','Omitted state variables can distort coupled behavior.'),
('coupling_terms','Coupling terms','Represent how one state affects another state rate.','Encode interaction transfer feedback contagion or competition.','Coupling terms should be tied to mechanism data or explicit scenario logic.'),
('initial_conditions','Initial conditions','Assign starting values to all state variables.','Determine the trajectory through state space.','Different initial states can produce different qualitative outcomes.'),
('parameter_values','Parameter values','Control growth interaction transfer decay and recovery rates.','Define the strength and direction of system interactions.','Parameter uncertainty can strongly affect coupled dynamics.'),
('equilibrium_analysis','Equilibrium analysis','Identifies states where all derivatives are zero.','Supports interpretation of steady states coexistence and balance points.','Equilibria are conditional on model structure and parameter values.'),
('numerical_method','Numerical method','Defines how the coupled system is approximated over time.','Supports reproducible simulation and solver review.','Step size and solver choice can distort oscillation stability and domain constraints.');

CREATE TABLE coupled_system_audit_cases (
    scenario TEXT NOT NULL,
    prey0 REAL NOT NULL,
    predator0 REAL NOT NULL,
    alpha REAL NOT NULL,
    beta REAL NOT NULL,
    delta REAL NOT NULL,
    gamma REAL NOT NULL,
    time_step REAL NOT NULL,
    steps INTEGER NOT NULL,
    method TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO coupled_system_audit_cases VALUES
('predator_prey_coupled_system',40.0,9.0,0.7,0.05,0.02,0.5,0.01,2000,'explicit_euler','Predator-prey terms are illustrative and assume continuous well-mixed interaction.');
