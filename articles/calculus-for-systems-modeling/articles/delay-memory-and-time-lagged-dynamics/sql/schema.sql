DROP TABLE IF EXISTS delay_assumption_registry;
DROP TABLE IF EXISTS delay_audit_cases;

CREATE TABLE delay_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO delay_assumption_registry VALUES
('delay_length','Delay length','Defines the time lag between cause and modeled effect.','Represents transport time, reporting delay, decision delay, incubation, repair, or adjustment time.','Delay length should be justified, estimated, or tested through sensitivity analysis.'),
('history_function','History function','Specifies past states before simulation begins.','Represents pre-model conditions that still affect present dynamics.','History assumptions can strongly shape early behavior and should be documented.'),
('lagged_state','Lagged state','Uses a past state in the current rate equation.','Represents delayed feedback, outdated information, or material travel time.','Lagged states should be tied to a real mechanism, not inserted only to improve fit.'),
('memory_kernel','Memory kernel','Weights past states by their influence on the present.','Represents fading memory, cumulative exposure, or long-lived effects.','Kernel shape should be interpreted and tested.'),
('interpolation_method','Interpolation method','Defines how past values are retrieved between stored time points.','Affects numerical accuracy in delay simulation.','Interpolation and time step choices should be recorded.'),
('response_metric','Response metric','Measures gap, overshoot, oscillation, recovery, or instability.','Defines how delayed response is evaluated.','Different response metrics can support different conclusions.');

CREATE TABLE delay_audit_cases (
    scenario TEXT NOT NULL,
    initial_state REAL NOT NULL,
    target REAL NOT NULL,
    adjustment_rate REAL NOT NULL,
    delay REAL NOT NULL,
    dt REAL NOT NULL,
    steps INTEGER NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO delay_audit_cases VALUES
('delayed_adjustment_to_target',80.0,100.0,0.2,5.0,0.1,300,'Delayed adjustment depends on delay length, history function, time step, interpolation method, and feedback strength.');
