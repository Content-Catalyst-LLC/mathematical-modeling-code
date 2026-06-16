DROP TABLE IF EXISTS resource_governance_registry;
DROP TABLE IF EXISTS resource_parameter_records;
DROP TABLE IF EXISTS resource_scenario_records;
DROP TABLE IF EXISTS resource_yield_records;

CREATE TABLE resource_governance_registry (
    registry_key TEXT PRIMARY KEY,
    registry_name TEXT NOT NULL,
    analytical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO resource_governance_registry VALUES
('stock_flow_record','Stock-flow record','Defines resource stock, extraction, regeneration, loss, units, measurement status, and system boundary.','Makes depletion and recovery dynamics explicit.','Resource outputs cannot be interpreted responsibly if stock-flow definitions are unclear.'),
('regeneration_record','Regeneration record','Documents whether regeneration is constant, proportional, logistic, threshold-dependent, seasonal, or environment-dependent.','Connects recovery assumptions to resource dynamics.','Renewable does not mean unlimited.'),
('extraction_record','Extraction record','Documents harvest, pumping, mining, demand, leakage, waste, efficiency, substitution, and governance rules.','Separates resource use from recovery capacity.','Extraction should not be treated as controllable without governance assumptions.'),
('threshold_record','Threshold record','Documents critical stock levels, slow recovery, collapse risk, and irreversibility assumptions.','Connects overshoot to recovery risk.','Threshold values require evidence and precaution.'),
('yield_record','Yield record','Documents sustainable yield, maximum sustainable yield, precautionary harvest, and uncertainty.','Connects extraction rules to regeneration assumptions.','MSY is not a safe target under uncertainty by default.'),
('claim_boundary','Claim boundary','Defines whether the model supports teaching, monitoring, scenario comparison, management, policy analysis, or decision support.','Prevents overclaiming and scope drift.','Resource conclusions should not exceed stock definitions, evidence, assumptions, governance feasibility, uncertainty, and tested scope.');

CREATE TABLE resource_parameter_records (
    parameter_name TEXT PRIMARY KEY,
    value REAL NOT NULL,
    unit TEXT NOT NULL,
    interpretation TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO resource_parameter_records VALUES
('R0',600.0,'stock units','initial resource stock','Stock definition and measurement boundary must be documented.');
INSERT INTO resource_parameter_records VALUES
('r',0.18,'per year','regeneration rate','Regeneration may be seasonal, climate-dependent, or threshold-dependent.');
INSERT INTO resource_parameter_records VALUES
('K',1000.0,'stock units','carrying capacity','Capacity can change with degradation, habitat, climate, or management.');
INSERT INTO resource_parameter_records VALUES
('H',45.0,'stock units per year','constant extraction or harvest','Harvest should not be treated as controllable without governance assumptions.');
INSERT INTO resource_parameter_records VALUES
('A',180.0,'stock units','critical recovery threshold','Threshold values require evidence and precaution.');
INSERT INTO resource_parameter_records VALUES
('loss_rate',0.02,'per year','additional degradation or leakage loss','Hidden loss terms can make sustainability claims misleading.');

CREATE TABLE resource_scenario_records (
    scenario_name TEXT PRIMARY KEY,
    resource_type TEXT NOT NULL,
    final_stock REAL NOT NULL,
    cumulative_extraction REAL NOT NULL,
    interpretation TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO resource_scenario_records VALUES
('renewable_precautionary_harvest','renewable_logistic',600.0,2800.0,'harvest below idealized maximum yield allows persistence under baseline assumptions','Sustainable yield is model-dependent.');
INSERT INTO resource_scenario_records VALUES
('renewable_high_harvest','renewable_logistic',250.0,4200.0,'higher harvest pressure can push stock downward','High harvest can move stock toward thresholds.');
INSERT INTO resource_scenario_records VALUES
('threshold_recovery_risk','threshold_regeneration',150.0,3000.0,'threshold-dependent recovery can slow or fail under depletion','Threshold values require evidence and precaution.');
INSERT INTO resource_scenario_records VALUES
('nonrenewable_drawdown','nonrenewable',0.0,600.0,'nonrenewable resource declines through extraction without regeneration','Nonrenewable drawdown should be modeled separately from renewable recovery.');

CREATE TABLE resource_yield_records (
    record_name TEXT PRIMARY KEY,
    regeneration_rate REAL NOT NULL,
    carrying_capacity REAL NOT NULL,
    maximum_sustainable_yield REAL NOT NULL,
    precautionary_yield REAL NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO resource_yield_records VALUES
('logistic_msy_baseline',0.18,1000.0,45.0,31.5,'MSY is not a safe target under uncertainty by default; precautionary harvest is lower.');
