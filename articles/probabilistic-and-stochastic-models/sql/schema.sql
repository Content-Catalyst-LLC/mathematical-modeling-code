-- Probabilistic and stochastic models governance schema.

DROP TABLE IF EXISTS probability_component_guide;
DROP TABLE IF EXISTS risk_scenario;
DROP TABLE IF EXISTS probability_model_register;
DROP TABLE IF EXISTS probability_component_type;

CREATE TABLE probability_component_type (
    model_component TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    typical_failure TEXT NOT NULL
);

CREATE TABLE probability_model_register (
    record_id INTEGER PRIMARY KEY,
    record_key TEXT NOT NULL,
    model_component TEXT NOT NULL,
    distribution_or_rule TEXT NOT NULL,
    interpretation TEXT NOT NULL,
    review_question TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('active', 'review', 'revise', 'archive')),
    FOREIGN KEY (model_component) REFERENCES probability_component_type(model_component)
);

CREATE TABLE risk_scenario (
    scenario TEXT PRIMARY KEY,
    demand_mu REAL NOT NULL,
    demand_sigma REAL NOT NULL CHECK (demand_sigma > 0),
    supply_mean REAL NOT NULL CHECK (supply_mean > 0),
    supply_sd REAL NOT NULL CHECK (supply_sd > 0),
    reserve REAL NOT NULL CHECK (reserve >= 0),
    simulations INTEGER NOT NULL CHECK (simulations >= 100),
    seed INTEGER NOT NULL,
    description TEXT
);

CREATE TABLE probability_component_guide (
    model_component TEXT PRIMARY KEY,
    meaning TEXT NOT NULL,
    example TEXT NOT NULL,
    review_question TEXT NOT NULL
);

INSERT INTO probability_component_type VALUES
('random_variable','Quantity represented as uncertain.','Support or tail behavior is inappropriate.'),
('distribution_choice','Assumption about uncertainty shape.','Distribution is chosen by convenience.'),
('parameter_uncertainty','Uncertain parameter value.','Uncertainty is not propagated.'),
('derived_risk','Risk output derived from random variables.','Probability and severity are confused.'),
('risk_measure','Summary of probability or tail severity.','Expected value hides tail risk.'),
('conditional_statement','Probability conditioned on evidence.','Conditioning is unclear or reversed.'),
('simulation_setting','Monte Carlo configuration.','Simulation count or seed is undocumented.'),
('validation_diagnostic','Probabilistic validation check.','Calibration and coverage are not tested.');

INSERT INTO probability_model_register(record_key, model_component, distribution_or_rule, interpretation, review_question, status) VALUES
('demand_distribution','random_variable','D ~ Lognormal(mu sigma)','Demand is positive and right-skewed','Is the tail behavior justified by evidence?','review'),
('supply_distribution','random_variable','S ~ Normal(mean sd) truncated at zero','Supply varies around a planned level','Is normal uncertainty plausible near zero?','review'),
('shortage_amount','derived_risk','Q = max(0 D - S - reserve)','Shortage is positive when demand exceeds available supply and reserve','Are shortage amount and shortage probability both reported?','active'),
('tail_risk','risk_measure','quantile(Q 0.95)','High-end shortage risk is summarized by a tail quantile','Is tail risk used alongside expected shortage?','active'),
('simulation_count','simulation_setting','M','Monte Carlo sample size','Is the simulation count adequate for tail estimates?','review');

INSERT INTO risk_scenario VALUES
('baseline',4.50,0.25,95,8,5,5000,101,'Baseline probabilistic risk scenario'),
('high_variability',4.50,0.45,95,12,5,5000,102,'Higher uncertainty in demand and supply'),
('low_reserve',4.50,0.25,95,8,0,5000,103,'No reserve buffer scenario'),
('stress_demand',4.65,0.35,90,10,5,5000,104,'Higher demand and lower supply stress scenario');

INSERT INTO probability_component_guide VALUES
('random_variable','Quantity represented as uncertain','D ~ Lognormal(mu sigma)','Is distribution support appropriate?'),
('distribution_choice','Assumption about uncertainty shape','Normal vs lognormal','Is tail behavior justified?'),
('parameter_uncertainty','Uncertain parameter value','theta ~ posterior','Is parameter uncertainty propagated?'),
('derived_risk','Output derived from random variables','Q = max(0 D-S)','Are probability and severity separated?'),
('conditional_statement','Probability given evidence','P(A|B)','Is conditioning clear?'),
('simulation_setting','Monte Carlo configuration','M and seed','Is simulation reproducible?'),
('validation_diagnostic','Check for probabilistic credibility','coverage or calibration','Are probability statements validated?');
