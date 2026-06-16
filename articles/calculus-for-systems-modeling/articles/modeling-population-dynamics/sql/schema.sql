DROP TABLE IF EXISTS population_model_governance_registry;
DROP TABLE IF EXISTS population_parameter_records;
DROP TABLE IF EXISTS population_scenario_records;

CREATE TABLE population_model_governance_registry (
    registry_key TEXT PRIMARY KEY,
    registry_name TEXT NOT NULL,
    analytical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO population_model_governance_registry VALUES
('state_variable','State variable','Defines the population count, unit, boundary, and measurement status.','Makes the modeled population explicit.','A population model cannot be interpreted responsibly if the counted population is unclear.'),
('growth_law','Growth law','Documents whether growth is exponential, logistic, structured, stochastic, or spatial.','Connects rate assumptions to system behavior.','A growth law is an assumption, not a universal description.'),
('parameter_record','Parameter record','Documents initial population, growth rate, carrying capacity, units, sources, and ranges.','Prevents parameter values from becoming unexamined authority.','Population projections can be highly sensitive to uncertain parameters.'),
('capacity_interpretation','Capacity interpretation','Documents what carrying capacity represents and whether it is fixed, uncertain, or dynamic.','Clarifies density dependence and constraint assumptions.','Carrying capacity is assumption-bearing and may change over time.'),
('calibration_record','Calibration record','Documents data source, fitting method, residuals, uncertainty, and validation status.','Separates fit from mechanism.','A fitted curve does not automatically prove the model mechanism.'),
('claim_boundary','Claim boundary','Defines whether the population model supports teaching, exploration, mechanism, prediction, or decision support.','Prevents overclaiming and scope drift.','Population model conclusions should not exceed evidence, assumptions, and tested scope.');

CREATE TABLE population_parameter_records (
    parameter_name TEXT PRIMARY KEY,
    value REAL NOT NULL,
    unit TEXT NOT NULL,
    source_status TEXT NOT NULL,
    interpretation TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO population_parameter_records VALUES
('N0',100.0,'individuals','synthetic teaching value','initial population','Initial values should be measured or estimated with uncertainty in empirical use.');
INSERT INTO population_parameter_records VALUES
('r',0.08,'per year','synthetic teaching value','intrinsic growth rate','Growth rates may vary over time and across conditions.');
INSERT INTO population_parameter_records VALUES
('K',1000.0,'individuals','synthetic teaching value','carrying capacity','Carrying capacity is assumption-bearing and may change over time.');

CREATE TABLE population_scenario_records (
    scenario_name TEXT PRIMARY KEY,
    model_type TEXT NOT NULL,
    initial_population REAL NOT NULL,
    growth_rate REAL NOT NULL,
    carrying_capacity REAL,
    final_time REAL NOT NULL,
    interpretation TEXT NOT NULL
);

INSERT INTO population_scenario_records VALUES
('exponential_baseline','exponential',100.0,0.08,NULL,40.0,'unconstrained growth baseline');
INSERT INTO population_scenario_records VALUES
('logistic_capacity_limited','logistic',100.0,0.08,1000.0,40.0,'growth limited by carrying capacity');
