-- Model purpose governance schema.

DROP TABLE IF EXISTS purpose_validation_matrix;
DROP TABLE IF EXISTS scenario_parameter;
DROP TABLE IF EXISTS purpose_register;
DROP TABLE IF EXISTS purpose_type;
DROP TABLE IF EXISTS prohibited_use;

CREATE TABLE purpose_type (
    purpose TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    typical_failure TEXT NOT NULL
);

CREATE TABLE purpose_register (
    purpose_id INTEGER PRIMARY KEY,
    purpose TEXT NOT NULL,
    primary_question TEXT NOT NULL,
    design_emphasis TEXT NOT NULL,
    validation_standard TEXT NOT NULL,
    uncertainty_format TEXT NOT NULL,
    misuse_risk TEXT NOT NULL,
    supported_use_status TEXT NOT NULL CHECK (supported_use_status IN ('supported', 'exploratory', 'review', 'revise', 'prohibited')),
    FOREIGN KEY (purpose) REFERENCES purpose_type(purpose)
);

CREATE TABLE scenario_parameter (
    scenario TEXT PRIMARY KEY,
    purpose TEXT NOT NULL,
    initial_stock REAL NOT NULL CHECK (initial_stock >= 0),
    capacity REAL NOT NULL CHECK (capacity > 0),
    inflow REAL NOT NULL CHECK (inflow >= 0),
    demand REAL NOT NULL CHECK (demand >= 0),
    loss_rate REAL NOT NULL CHECK (loss_rate >= 0),
    control_action REAL NOT NULL CHECK (control_action >= 0),
    periods INTEGER NOT NULL CHECK (periods > 0),
    description TEXT,
    FOREIGN KEY (purpose) REFERENCES purpose_type(purpose)
);

CREATE TABLE purpose_validation_matrix (
    matrix_id INTEGER PRIMARY KEY,
    purpose TEXT NOT NULL,
    validation_emphasis TEXT NOT NULL,
    evidence_needed TEXT NOT NULL,
    prohibited_without_review TEXT NOT NULL,
    FOREIGN KEY (purpose) REFERENCES purpose_type(purpose)
);

CREATE TABLE prohibited_use (
    use_id INTEGER PRIMARY KEY,
    prohibited_use TEXT NOT NULL,
    reason TEXT NOT NULL,
    evidence_required_for_expansion TEXT NOT NULL
);

INSERT INTO purpose_type VALUES
('explanation', 'Clarifies why system behavior occurs.', 'Plausible mechanism treated as validated cause.'),
('prediction', 'Estimates unknown or future values.', 'Prediction used beyond validation horizon.'),
('control', 'Guides action through feedback.', 'Action taken without robustness, monitoring, or fail-safes.'),
('decision_support', 'Compares alternatives under uncertainty.', 'Decision support becomes decision substitution.'),
('simulation', 'Explores behavior under assumptions.', 'Simulation trace treated as forecast.'),
('optimization', 'Selects a feasible option by objective and constraints.', 'Objective treated as complete value system.');

INSERT INTO purpose_register(purpose, primary_question, design_emphasis, validation_standard, uncertainty_format, misuse_risk, supported_use_status) VALUES
('explanation','Why does the system behave this way?','Mechanism interpretability stock-flow structure','Structural plausibility qualitative behavior domain review','Assumption and mechanism sensitivity','Plausible mechanism treated as validated cause','supported'),
('prediction','What is likely to happen?','Forecast target calibration validation horizon','Out-of-sample forecast performance calibration monitoring','Prediction interval and calibration report','Forecast used beyond validation horizon','review'),
('control','What action should steer the system?','State action feedback constraints robustness','Stability stress testing monitoring fail-safes','Robustness envelope and failure modes','Automated action without sufficient oversight','review'),
('decision_support','Which alternative should be considered?','Alternatives consequences trade-offs uncertainty','Fit to decision context uncertainty communication governance','Scenario matrix robustness profile trade-off table','Decision support becomes decision substitution','review'),
('simulation','What behavior emerges under assumptions?','Scenario design structural adequacy numerical experiment','Scenario adequacy structural review uncertainty ranges','Scenario notes ensembles and use limitations','Simulation trace treated as forecast','review'),
('optimization','Which feasible option best satisfies an objective?','Objective function constraints feasible set trade-offs','Objective sensitivity constraint validation robustness','Trade-off curve sensitivity sweep robust comparison','Objective function treated as complete value system','review');

INSERT INTO scenario_parameter VALUES
('explanatory_baseline','explanation',80,100,8,6,0.015,0,60,'Mechanism-oriented stock-flow demonstration'),
('prediction_low_inflow','prediction',80,100,5,6,0.015,0,60,'Forecast-oriented lower inflow case'),
('control_demand_reduction','control',80,100,5,6,0.015,1.5,60,'Control-oriented demand reduction case'),
('decision_support_stress','decision_support',70,80,5,7,0.030,0.5,60,'Decision-support stress case'),
('simulation_extreme_case','simulation',60,75,4,7,0.035,0.25,80,'Exploratory simulation stress case'),
('optimization_proxy_case','optimization',80,100,5,6,0.015,1.0,60,'Optimization-style proxy control case');

INSERT INTO purpose_validation_matrix(purpose, validation_emphasis, evidence_needed, prohibited_without_review) VALUES
('explanation','Mechanism and structural plausibility','Theory domain review qualitative behavior empirical consistency','Precise operational forecast'),
('prediction','Out-of-sample performance and calibration','Validation data forecast error uncertainty calibration monitoring','Causal explanation or long-horizon extrapolation'),
('control','Robust action under feedback','Stability analysis stress tests monitoring fail-safes','Automated action without oversight'),
('decision_support','Fit to decision context','Alternatives consequences uncertainty trade-offs governance','Decision substitution'),
('simulation','Scenario credibility and structural transparency','Scenario rationale assumptions uncertainty use limitations','Probability claims without probabilistic model'),
('optimization','Objective and constraint adequacy','Objective sensitivity feasibility review robustness analysis','Policy legitimacy without value review');

INSERT INTO prohibited_use VALUES
(1, 'Use scenario traces as probability forecasts.', 'Scenario exploration does not assign probability without a probabilistic model.', 'Probability model, calibration, validation, and uncertainty report.'),
(2, 'Use decision-support output as automatic decision authority.', 'Decision support informs judgment but does not replace accountability.', 'Governance review, stakeholder process, and accountable decision protocol.'),
(3, 'Use predictive output as causal explanation.', 'Predictive association may not reveal mechanism.', 'Causal design, mechanism evidence, and alternative explanation review.');
