DROP TABLE IF EXISTS simulation_governance_registry;
DROP TABLE IF EXISTS high_dimensional_simulation_audit_cases;

CREATE TABLE simulation_governance_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO simulation_governance_registry VALUES
('state_vector','State vector','Defines modeled variables dimension units and system state representation.','Determines what the simulation can track over time.','Excluded variables and poor scaling can distort simulated behavior.'),
('transition_rule','Transition rule','Defines how the system moves from one state to the next.','Encodes modeled dynamics interactions feedback and external inputs.','Transition assumptions should be validated against mechanisms and evidence.'),
('parameter_space','Parameter space','Defines parameter values ranges and scenario assumptions.','Controls how alternative futures or system conditions are explored.','Weak parameter ranges can create misleading scenario confidence.'),
('uncertainty_model','Uncertainty model','Defines random inputs shock distributions covariance and sampling process.','Determines how uncertainty propagates through the simulation.','Distribution and covariance assumptions should be documented and tested.'),
('ensemble_design','Ensemble design','Defines number of runs random seeds scenarios and summary statistics.','Supports uncertainty ranges risk estimates and robustness review.','A single trajectory should not be overinterpreted as a forecast.'),
('dimensionality_management','Dimensionality management','Defines sparsity projection low-rank approximation or reduced-order modeling.','Controls computation and interpretability in large state spaces.','Compression may remove weak signals rare events or local structure.'),
('validation_design','Validation design','Defines calibration holdout tests numerical checks and comparison with observed behavior.','Evaluates whether simulation outputs are credible for the intended use.','Validation is partial evidence not proof of future accuracy.'),
('responsible_use','Responsible use','Defines how assumptions uncertainty sensitivity limitations and decision consequences are communicated.','Prevents simulated outcomes from being overstated as predictions or certainty.','Simulation should support structured reasoning not replace judgment.');

CREATE TABLE high_dimensional_simulation_audit_cases (
    model_name TEXT NOT NULL,
    state_dimension INTEGER NOT NULL,
    time_steps INTEGER NOT NULL,
    ensemble_runs INTEGER NOT NULL,
    method TEXT NOT NULL,
    random_seed INTEGER NOT NULL,
    transition_spectral_radius REAL NOT NULL,
    transition_density REAL NOT NULL,
    final_state_mean_norm REAL NOT NULL,
    final_state_mean_total REAL NOT NULL,
    final_state_95th_percentile_total REAL NOT NULL,
    threshold_exceedance_probability REAL NOT NULL,
    first_three_component_energy REAL NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO high_dimensional_simulation_audit_cases VALUES
('synthetic_high_dimensional_simulation_audit',24,40,250,'sparse_linear_state_update_with_correlated_monte_carlo_shocks',20260629,0.94,0.12,4.8,24.6,26.0,0.10,0.78,'Simulation outputs are conditional model outcomes not observations of the future.');
