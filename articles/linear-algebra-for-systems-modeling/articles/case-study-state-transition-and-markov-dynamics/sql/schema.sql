DROP TABLE IF EXISTS state_transition_markov_governance_registry;
DROP TABLE IF EXISTS transition_matrix;
DROP TABLE IF EXISTS state_transition_markov_audit_cases;

CREATE TABLE state_transition_markov_governance_registry (
    governance_key TEXT PRIMARY KEY,
    governance_name TEXT NOT NULL,
    modeling_role TEXT NOT NULL,
    review_requirement TEXT NOT NULL,
    responsible_use_warning TEXT NOT NULL
);

INSERT INTO state_transition_markov_governance_registry VALUES
('state_definition','State definition','Defines the categories or conditions represented by the state space.','Document whether states represent condition risk behavior status regime location health compliance or process stage.','State labels can hide severity heterogeneity overlapping conditions and measurement error.'),
('transition_semantics','Transition semantics','Defines what movement from one state to another means.','State whether transitions are observed frequencies probabilities policy rules simulations expert judgments or scenario assumptions.','Transition probabilities should not be treated as causal mechanisms without evidence.'),
('time_step','Time-step definition','Defines the period represented by one transition.','Document whether one step represents a day week month year event decision cycle or operational interval.','Transition probabilities lose meaning without a clear time scale.'),
('stochastic_check','Stochastic matrix check','Verifies that transition probabilities are valid.','Check nonnegative probabilities row or column sums and matrix orientation.','Invalid stochastic structure can make all downstream results meaningless.'),
('markov_assumption','Markov assumption','Defines whether current state is treated as sufficient for future movement.','Review whether history cumulative exposure repeated disruption policy intervention or hidden subgroups affect transitions.','A memoryless model may distort systems where history matters.'),
('stationary_interpretation','Stationary interpretation','Defines how long-run distributions should be communicated.','Check convergence reducibility periodicity and stability of transition probabilities.','Stationary distributions describe the model not guaranteed real-world destiny.'),
('sensitivity_testing','Sensitivity testing','Tests whether outputs are robust to transition uncertainty and scenario changes.','Compare baseline stress intervention time-varying and uncertainty-perturbed transition matrices.','Small transition-probability changes can accumulate into large long-run differences.'),
('decision_boundary','Decision boundary','Defines what the Markov model can and cannot support.','Attach interpretation limits uncertainty notes validation status and stop-use conditions to outputs.','State transition models should support accountable judgment not replace domain review.');

CREATE TABLE transition_matrix (
    current_state TEXT NOT NULL,
    next_state TEXT NOT NULL,
    transition_probability REAL NOT NULL,
    scenario_name TEXT NOT NULL
);

INSERT INTO transition_matrix VALUES
('normal','normal',0.70,'baseline'),
('normal','strained',0.20,'baseline'),
('normal','disrupted',0.05,'baseline'),
('normal','recovered',0.05,'baseline'),
('strained','normal',0.20,'baseline'),
('strained','strained',0.50,'baseline'),
('strained','disrupted',0.20,'baseline'),
('strained','recovered',0.10,'baseline'),
('disrupted','normal',0.05,'baseline'),
('disrupted','strained',0.25,'baseline'),
('disrupted','disrupted',0.55,'baseline'),
('disrupted','recovered',0.15,'baseline'),
('recovered','normal',0.50,'baseline'),
('recovered','strained',0.20,'baseline'),
('recovered','disrupted',0.05,'baseline'),
('recovered','recovered',0.25,'baseline');

CREATE TABLE state_transition_markov_audit_cases (
    workflow_name TEXT NOT NULL,
    scenario_name TEXT NOT NULL,
    state_count INTEGER NOT NULL,
    time_steps INTEGER NOT NULL,
    stochastic_check_passed INTEGER NOT NULL,
    initial_primary_state TEXT NOT NULL,
    highest_probability_state_after_horizon TEXT NOT NULL,
    highest_probability_after_horizon REAL NOT NULL,
    stationary_highest_probability_state TEXT NOT NULL,
    stationary_highest_probability REAL NOT NULL,
    stress_disrupted_probability_after_horizon REAL NOT NULL,
    baseline_disrupted_probability_after_horizon REAL NOT NULL,
    memoryless_warning TEXT NOT NULL,
    interpretation_warning TEXT NOT NULL
);

INSERT INTO state_transition_markov_audit_cases VALUES
('state_transition_markov_audit','synthetic_infrastructure_condition_transition_model',4,5,1,'normal','normal',0.42833125,'normal',0.40602189781,0.41016825,0.1756128125,'The Markov assumption treats the current state as sufficient for predicting the next state.','Stationary distributions and multi-step probabilities describe the model not guaranteed system destiny.');
