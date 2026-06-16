DROP TABLE IF EXISTS population_model_governance_registry;
DROP TABLE IF EXISTS population_parameter_records;
DROP TABLE IF EXISTS population_scenario_records;
DROP TABLE IF EXISTS population_identifiability_records;

CREATE TABLE population_model_governance_registry (
    registry_key TEXT PRIMARY KEY,
    registry_name TEXT NOT NULL,
    analytical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO population_model_governance_registry VALUES
('state_variable','State variable','Defines the population count, unit, boundary, and measurement status.','Makes the modeled population explicit.','A population model cannot be interpreted responsibly if the counted population is unclear.'),
('growth_law','Growth law','Documents whether growth is exponential, logistic, structured, stochastic, spatial, threshold-limited, or harvested.','Connects rate assumptions to system behavior.','A growth law is an assumption, not a universal description.'),
('parameter_record','Parameter record','Documents initial population, growth rate, carrying capacity, threshold, harvesting, noise, movement, units, sources, and ranges.','Prevents parameter values from becoming unexamined authority.','Population projections can be highly sensitive to uncertain parameters.'),
('capacity_interpretation','Capacity interpretation','Documents what carrying capacity represents and whether it is fixed, uncertain, or dynamic.','Clarifies density dependence and constraint assumptions.','Carrying capacity is assumption-bearing and may change over time.'),
('calibration_record','Calibration record','Documents data source, fitting method, residuals, uncertainty, identifiability, and validation status.','Separates fit from mechanism.','A fitted curve does not automatically prove the model mechanism.'),
('claim_boundary','Claim boundary','Defines whether the population model supports teaching, exploration, mechanism, prediction, or decision support.','Prevents overclaiming and scope drift.','Population model conclusions should not exceed evidence, assumptions, and tested scope.');

CREATE TABLE population_parameter_records (
    parameter_name TEXT PRIMARY KEY,
    value REAL NOT NULL,
    unit TEXT NOT NULL,
    source_status TEXT NOT NULL,
    interpretation TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO population_parameter_records VALUES ('N0',100.0,'individuals','synthetic teaching value','initial population','Initial values should include uncertainty.');
INSERT INTO population_parameter_records VALUES ('r',0.08,'per year','synthetic teaching value','intrinsic growth rate','Growth rates may vary across conditions.');
INSERT INTO population_parameter_records VALUES ('K',1000.0,'individuals','synthetic teaching value','carrying capacity','Carrying capacity may change over time.');
INSERT INTO population_parameter_records VALUES ('A',75.0,'individuals','synthetic teaching value','Allee threshold','Threshold parameters can be hard to identify.');
INSERT INTO population_parameter_records VALUES ('H',12.0,'individuals per year','synthetic teaching value','harvest/removal rate','Removal terms are management assumptions.');
INSERT INTO population_parameter_records VALUES ('sigma',0.12,'noise intensity','synthetic teaching value','environmental variability','Stochastic output should be summarized as distribution.');

CREATE TABLE population_scenario_records (
    scenario_name TEXT PRIMARY KEY,
    model_type TEXT NOT NULL,
    interpretation TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO population_scenario_records VALUES ('exponential_baseline','exponential','unconstrained growth baseline','Long-run projections may overreach.');
INSERT INTO population_scenario_records VALUES ('logistic_capacity_limited','logistic','growth limited by carrying capacity','Carrying capacity is assumption-bearing.');
INSERT INTO population_scenario_records VALUES ('allee_threshold','allee_effect','low-population threshold','Threshold claims need evidence near the threshold.');
INSERT INTO population_scenario_records VALUES ('harvesting_pressure','harvesting','external removal pressure','Removal terms are management assumptions.');
INSERT INTO population_scenario_records VALUES ('stochastic_logistic_path','stochastic','one stochastic path','A single path is not a distribution.');
INSERT INTO population_scenario_records VALUES ('structured_total','leslie_matrix','stage-structured projection','Aggregate population size can hide composition.');

CREATE TABLE population_identifiability_records (
    diagnostic_name TEXT PRIMARY KEY,
    issue TEXT NOT NULL,
    warning TEXT NOT NULL,
    governance_response TEXT NOT NULL
);

INSERT INTO population_identifiability_records VALUES ('short_series_r_k_tradeoff','Different r and K values can fit early growth similarly.','Do not infer carrying capacity from short early-growth data alone.','Use profile likelihood, grid search, or longer time series.');
INSERT INTO population_identifiability_records VALUES ('threshold_parameter_A','Allee thresholds may be invisible without low-population observations.','Threshold claims need evidence near the threshold.','Run threshold scenarios and state uncertainty.');
INSERT INTO population_identifiability_records VALUES ('stochastic_sigma','Noise intensity depends on represented variability.','A single stochastic path is not a distribution.','Summarize ensembles and quantiles.');
