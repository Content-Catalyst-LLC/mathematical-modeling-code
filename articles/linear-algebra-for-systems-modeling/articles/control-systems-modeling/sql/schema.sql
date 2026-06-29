DROP TABLE IF EXISTS control_system_assumption_registry;
DROP TABLE IF EXISTS control_system_audit_cases;

CREATE TABLE control_system_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO control_system_assumption_registry VALUES
('state_definition','State definition','Defines the internal coordinates of the control model.','Determines what the controller is trying to regulate.','Poorly defined states can make feedback target the wrong behavior.'),
('input_authority','Input authority','Defines the channels represented by the input matrix B.','Determines what interventions are available.','Mathematical input channels may not be physically legally or institutionally available.'),
('output_reliability','Output reliability','Defines what is measured through the output matrix C.','Determines what information feedback uses.','Noisy biased delayed or incomplete outputs can destabilize decisions.'),
('controllability','Controllability','Tests whether inputs can influence state-space directions.','Shows whether the model can move the system through relevant states.','Rank alone does not account for cost constraints or authority.'),
('observability','Observability','Tests whether outputs reveal internal state directions.','Shows whether feedback can infer what needs to be controlled.','Hidden unstable modes are serious safety and governance risks.'),
('feedback_objective','Feedback objective','Defines what the controller is designed to achieve.','Encodes performance cost safety or optimization priorities.','Control objectives are value choices and should be documented.'),
('constraints','Constraints','Defines input state rate delay and feasibility limits.','Determines whether the control law can actually be applied.','Ignoring saturation or delay can invalidate closed-loop analysis.');

CREATE TABLE control_system_audit_cases (
    system_name TEXT NOT NULL,
    time_model TEXT NOT NULL,
    state_matrix_A TEXT NOT NULL,
    input_matrix_B TEXT NOT NULL,
    output_matrix_C TEXT NOT NULL,
    feedback_matrix_K TEXT NOT NULL,
    open_loop_eigenvalues TEXT NOT NULL,
    closed_loop_eigenvalues TEXT NOT NULL,
    open_loop_max_real_part REAL NOT NULL,
    closed_loop_max_real_part REAL NOT NULL,
    controllability_rank INTEGER NOT NULL,
    observability_rank INTEGER NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO control_system_audit_cases VALUES
('two_state_control_system_audit','continuous_time_linear_state_space','0.100000,1.000000;0.000000,0.200000','0.000000;1.000000','1.000000,0.000000','0.500000,1.400000','0.200000,0.100000','-0.600000,-0.500000',0.2,-0.5,2,2,'Control models require input authority output reliability constraints uncertainty review objective transparency and domain accountability.');
