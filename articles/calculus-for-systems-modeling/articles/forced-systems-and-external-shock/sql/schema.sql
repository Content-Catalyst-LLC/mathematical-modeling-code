DROP TABLE IF EXISTS shock_assumption_registry;
DROP TABLE IF EXISTS forced_system_audit_cases;

CREATE TABLE shock_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO shock_assumption_registry VALUES
('forcing_function','Forcing function','Defines the external input applied to the dynamic system.','Represents shock intervention stress seasonality policy or disturbance.','The forcing function should be justified and documented.'),
('shock_timing','Shock timing','Identifies when the external disturbance occurs.','Determines whether the system is shocked during a stable or fragile state.','Timing assumptions can strongly affect response and recovery.'),
('shock_magnitude','Shock magnitude','Defines the size of the external disturbance.','Represents severity intensity intervention strength or loss.','Magnitude should include units scaling and scenario rationale.'),
('recovery_rate','Recovery rate','Controls how quickly the system returns toward a reference state.','Represents resilience repair adaptation damping or institutional response.','Recovery-rate estimates should not be treated as universal constants.'),
('response_metric','Response metric','Measures deviation loss recovery time overshoot or threshold crossing.','Defines what counts as impact or resilience.','Different metrics can support different conclusions.'),
('model_boundary','Model boundary','Defines why the driver is treated as external.','Clarifies which causes are inside or outside the model scope.','External forcing may become endogenous in a larger model.');

CREATE TABLE forced_system_audit_cases (
    scenario TEXT NOT NULL,
    initial_state REAL NOT NULL,
    equilibrium REAL NOT NULL,
    recovery_rate REAL NOT NULL,
    shock_time REAL NOT NULL,
    shock_magnitude REAL NOT NULL,
    dt REAL NOT NULL,
    steps INTEGER NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO forced_system_audit_cases VALUES
('baseline_vs_impulse_shock',100.0,100.0,0.15,10.0,-30.0,0.1,300,'Shock response depends on forcing form, timing, magnitude, recovery rate, numerical step size, and model boundary.');
