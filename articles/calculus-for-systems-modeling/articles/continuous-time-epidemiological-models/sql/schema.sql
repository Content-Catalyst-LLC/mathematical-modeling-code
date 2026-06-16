DROP TABLE IF EXISTS epidemiological_governance_registry;
DROP TABLE IF EXISTS epidemiological_parameter_records;
DROP TABLE IF EXISTS epidemiological_scenario_records;
DROP TABLE IF EXISTS epidemiological_threshold_records;

CREATE TABLE epidemiological_governance_registry (
    registry_key TEXT PRIMARY KEY,
    registry_name TEXT NOT NULL,
    analytical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO epidemiological_governance_registry VALUES
('compartment_record','Compartment record','Defines susceptible, exposed, infectious, recovered, vaccinated, hospitalized, removed, and other states.','Connects biological interpretation to model structure.','Compartments should not be treated as exact reality without definition and validation.'),
('transmission_record','Transmission record','Documents transmission parameter, force of infection, contact structure, and mixing assumption.','Connects infection flow to contact and susceptibility.','Transmission parameters can hide behavior, contact, biology, and environment.'),
('observation_record','Observation record','Documents reported cases, detection fraction, delays, testing context, hospitalization, mortality, and surveillance source.','Separates true system states from observed data.','Reported cases should not be treated as true infections without observation assumptions.'),
('intervention_record','Intervention record','Documents whether intervention affects contact, susceptibility, infectious duration, severity, reporting, or behavior.','Connects scenario changes to explicit mechanisms.','Intervention effects should not be represented as unexplained reductions.'),
('immunity_record','Immunity record','Documents recovered immunity, vaccination, efficacy, waning, boosters, and population coverage.','Connects susceptible dynamics to protection assumptions.','Immunity assumptions can strongly change long-run dynamics.'),
('uncertainty_record','Uncertainty record','Documents parameter uncertainty, structural uncertainty, reporting uncertainty, initial-condition uncertainty, and sensitivity.','Keeps scenarios from becoming false precision.','Epidemiological outputs should be presented with uncertainty and purpose.'),
('claim_boundary','Claim boundary','Defines whether the model supports teaching, scenario comparison, preparedness, operational analysis, or decision support.','Prevents overclaiming and scope drift.','Epidemiological conclusions should not exceed compartment definitions, data evidence, uncertainty, domain review, and tested scope.');

CREATE TABLE epidemiological_parameter_records (
    parameter_name TEXT PRIMARY KEY,
    value REAL NOT NULL,
    unit TEXT NOT NULL,
    interpretation TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO epidemiological_parameter_records VALUES
('N',100000.0,'people','population boundary','Population boundary and mixing assumptions must be documented.');
INSERT INTO epidemiological_parameter_records VALUES
('beta',0.32,'per day','transmission parameter','Transmission combines contact, infectiousness, behavior, setting, and reporting context.');
INSERT INTO epidemiological_parameter_records VALUES
('gamma',0.10,'per day','recovery or removal rate','Recovery rate should be tied to infectious period assumptions.');
INSERT INTO epidemiological_parameter_records VALUES
('sigma',0.20,'per day','progression from exposed to infectious','Latency and incubation assumptions should be distinguished where needed.');
INSERT INTO epidemiological_parameter_records VALUES
('nu',0.005,'per day','vaccination rate','Vaccination assumptions require coverage, timing, efficacy, and equity records.');
INSERT INTO epidemiological_parameter_records VALUES
('omega',0.001,'per day','waning protection rate','Waning immunity assumptions can change long-run dynamics.');
INSERT INTO epidemiological_parameter_records VALUES
('rho',0.50,'fraction','reporting or detection fraction','Reported cases should not be treated as true infections without observation assumptions.');

CREATE TABLE epidemiological_scenario_records (
    scenario_name TEXT PRIMARY KEY,
    model_type TEXT NOT NULL,
    peak_infectious REAL NOT NULL,
    final_recovered REAL NOT NULL,
    reproduction_number REAL NOT NULL,
    interpretation TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO epidemiological_scenario_records VALUES
('baseline_sir','SIR',30000.0,93000.0,3.2,'baseline SIR scenario with susceptible depletion','Baseline scenario depends on homogeneous mixing assumptions.');
INSERT INTO epidemiological_scenario_records VALUES
('reduced_transmission_sir','SIR',12000.0,73000.0,2.2,'lower transmission reduces peak infectious burden','Reduced transmission must be tied to a mechanism.');
INSERT INTO epidemiological_scenario_records VALUES
('latent_period_seir','SEIR',25000.0,92000.0,3.2,'exposed compartment delays infectious growth','Latency and incubation assumptions should be distinguished.');
INSERT INTO epidemiological_scenario_records VALUES
('vaccination_reduced_susceptible','SIR_vaccination',9000.0,50000.0,2.72,'lower susceptible share reduces effective reproduction number','Vaccination assumptions require coverage timing efficacy and equity records.');

CREATE TABLE epidemiological_threshold_records (
    record_name TEXT PRIMARY KEY,
    r0 REAL NOT NULL,
    susceptible_threshold REAL NOT NULL,
    herd_immunity_threshold REAL NOT NULL,
    doubling_time REAL NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO epidemiological_threshold_records VALUES
('baseline_thresholds',3.2,0.3125,0.6875,3.1507,'Thresholds are model-dependent summaries and should be presented with assumptions and context.');
