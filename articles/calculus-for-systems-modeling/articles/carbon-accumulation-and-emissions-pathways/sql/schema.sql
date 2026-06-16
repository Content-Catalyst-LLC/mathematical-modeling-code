DROP TABLE IF EXISTS carbon_pathway_governance_registry;
DROP TABLE IF EXISTS carbon_pathway_parameter_records;
DROP TABLE IF EXISTS carbon_pathway_scenario_records;
DROP TABLE IF EXISTS carbon_budget_records;

CREATE TABLE carbon_pathway_governance_registry (
    registry_key TEXT PRIMARY KEY,
    registry_name TEXT NOT NULL,
    analytical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO carbon_pathway_governance_registry VALUES
('stock_flow_record','Stock-flow record','Defines emissions, removals, atmospheric carbon, land sinks, ocean sinks, units, and accounting boundary.','Makes accumulation and pathway memory explicit.','Carbon pathway outputs cannot be interpreted responsibly if stock-flow definitions are unclear.'),
('pathway_record','Pathway record','Documents whether emissions follow historical, baseline, mitigation, net-zero, overshoot, or negative-emissions pathways.','Separates scenario assumptions from physical accumulation.','Pathway scenarios should not be presented as guaranteed futures.'),
('sink_record','Sink record','Documents land uptake, ocean uptake, airborne fraction, impulse response, and carbon-cycle feedback assumptions.','Connects atmospheric accumulation to reservoir exchange.','Fixed sink assumptions can hide nonlinear carbon-cycle feedback.'),
('budget_record','Budget record','Documents carbon budget, temperature goal, probability framing, historical emissions, and remaining allowance.','Connects cumulative emissions to pathway constraints.','Carbon budgets are conditional estimates, not exact guarantees.'),
('removal_record','Removal record','Documents negative-emissions rate, durability, accounting status, feasibility, and permanence.','Separates gross emissions, removals, and net emissions.','Net-zero and overshoot claims require removal governance.'),
('claim_boundary','Claim boundary','Defines whether the model supports teaching, pathway comparison, carbon budgeting, policy analysis, or decision support.','Prevents overclaiming and scope drift.','Carbon pathway conclusions should not exceed accounting boundaries, evidence, assumptions, uncertainty, and tested scope.');

CREATE TABLE carbon_pathway_parameter_records (
    parameter_name TEXT PRIMARY KEY,
    value REAL NOT NULL,
    unit TEXT NOT NULL,
    interpretation TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO carbon_pathway_parameter_records VALUES
('E0',40.0,'GtCO2 per year','initial annual emissions','Accounting boundary must be documented.');
INSERT INTO carbon_pathway_parameter_records VALUES
('decline_rate',0.08,'per year','exponential emissions decline rate','Pathway assumptions should not be presented as predictions.');
INSERT INTO carbon_pathway_parameter_records VALUES
('airborne_fraction',0.45,'fraction','fixed simplified airborne fraction','Airborne fraction is not constant across all time scales and scenarios.');
INSERT INTO carbon_pathway_parameter_records VALUES
('budget',500.0,'GtCO2','illustrative remaining carbon budget','Carbon budgets depend on temperature goal, probability framing, and uncertainty.');
INSERT INTO carbon_pathway_parameter_records VALUES
('removal_rate',5.0,'GtCO2 per year','illustrative negative-emissions rate','Removal feasibility, permanence, scale, and governance must be reviewed.');

CREATE TABLE carbon_pathway_scenario_records (
    scenario_name TEXT PRIMARY KEY,
    pathway_type TEXT NOT NULL,
    cumulative_emissions REAL NOT NULL,
    atmospheric_burden REAL NOT NULL,
    interpretation TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO carbon_pathway_scenario_records VALUES
('constant_emissions','constant',1240.0,558.0,'constant emissions continue accumulating carbon','Annual-flow values are not enough; cumulative burden matters.');
INSERT INTO carbon_pathway_scenario_records VALUES
('linear_decline_to_zero','linear_decline',600.0,270.0,'linear decline reaches zero after 30 years','Net zero does not erase past accumulation.');
INSERT INTO carbon_pathway_scenario_records VALUES
('exponential_decline','exponential_decline',480.0,216.0,'exponential decline reduces early cumulative burden','Pathway shape changes cumulative burden.');
INSERT INTO carbon_pathway_scenario_records VALUES
('overshoot_with_negative_emissions','overshoot',500.0,225.0,'negative emissions partly offset earlier cumulative emissions','Removals require feasibility, durability, and governance review.');

CREATE TABLE carbon_budget_records (
    scenario_name TEXT PRIMARY KEY,
    cumulative_emissions REAL NOT NULL,
    budget REAL NOT NULL,
    exceeds_budget INTEGER NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO carbon_budget_records VALUES
('constant_emissions',1240.0,500.0,1,'Carbon budgets are conditional estimates, not exact guarantees.');
INSERT INTO carbon_budget_records VALUES
('linear_decline_to_zero',600.0,500.0,1,'Carbon budgets are conditional estimates, not exact guarantees.');
INSERT INTO carbon_budget_records VALUES
('exponential_decline',480.0,500.0,0,'Carbon budgets are conditional estimates, not exact guarantees.');
INSERT INTO carbon_budget_records VALUES
('overshoot_with_negative_emissions',500.0,500.0,0,'Carbon budgets are conditional estimates, not exact guarantees.');
