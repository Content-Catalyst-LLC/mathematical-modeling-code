DROP TABLE IF EXISTS economic_growth_governance_registry;
DROP TABLE IF EXISTS economic_parameter_records;
DROP TABLE IF EXISTS economic_scenario_records;
DROP TABLE IF EXISTS economic_growth_records;

CREATE TABLE economic_growth_governance_registry (
    registry_key TEXT PRIMARY KEY,
    registry_name TEXT NOT NULL,
    analytical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO economic_growth_governance_registry VALUES
('output_record','Output record','Defines output measure, price basis, sector boundary, data source, and time horizon.','Prevents confusion between output, welfare, distribution, and sustainability.','Output growth should not be treated as complete social progress.'),
('growth_record','Growth record','Documents growth rate, time horizon, compounding assumption, and whether the rate is historical, assumed, or scenario-based.','Makes rate assumptions and compounding visible.','Growth-rate assumptions compound strongly over time.'),
('capital_record','Capital record','Documents capital stock, investment, depreciation, maintenance, and asset quality.','Connects output growth to accumulation and capacity.','Capital stock measures can hide quality, maintenance, and obsolescence.'),
('productivity_record','Productivity record','Documents productivity assumptions, technology, organization, institutions, skills, and measurement residuals.','Prevents productivity from becoming an unexplained placeholder.','Productivity should not be used as a residual without interpretation.'),
('adjustment_record','Adjustment record','Documents adjustment speed, target, lag, shock response, and disequilibrium process.','Connects short-run dynamics to delayed system response.','Instant adjustment assumptions can hide overshoot and persistence.'),
('constraint_record','Constraint record','Documents infrastructure, labor, resource, energy, financial, institutional, and ecological constraints.','Connects growth pathways to system limits and bottlenecks.','Unconstrained growth assumptions should be compared with constrained scenarios.'),
('claim_boundary','Claim boundary','Defines whether the model supports teaching, scenario comparison, forecasting, policy analysis, development planning, or decision support.','Prevents overclaiming and scope drift.','Economic conclusions should not exceed output definitions, data evidence, structural assumptions, uncertainty, distributional interpretation, and tested scope.');

CREATE TABLE economic_parameter_records (
    parameter_name TEXT PRIMARY KEY,
    value REAL NOT NULL,
    unit TEXT NOT NULL,
    interpretation TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO economic_parameter_records VALUES
('Y0',100.0,'index','initial output index','Output measure and price basis must be documented.');
INSERT INTO economic_parameter_records VALUES
('g',0.025,'per year','baseline output growth rate','Growth-rate assumptions compound strongly over time.');
INSERT INTO economic_parameter_records VALUES
('s',0.22,'share of output','investment or savings share','Savings does not automatically become productive investment.');
INSERT INTO economic_parameter_records VALUES
('delta',0.05,'per year','depreciation rate','Depreciation should include maintenance and obsolescence assumptions.');
INSERT INTO economic_parameter_records VALUES
('A_growth',0.012,'per year','productivity growth rate','Productivity should not be used as an unexplained residual without interpretation.');
INSERT INTO economic_parameter_records VALUES
('lambda',0.35,'per year','adjustment speed','Adjustment speed depends on institutions, frictions, contracts, and expectations.');

CREATE TABLE economic_scenario_records (
    scenario_name TEXT PRIMARY KEY,
    model_type TEXT NOT NULL,
    final_output REAL NOT NULL,
    final_capital REAL NOT NULL,
    interpretation TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO economic_scenario_records VALUES
('constant_growth_projection','exponential_growth',271.83,0.0,'constant proportional growth compounds over time','Growth-rate assumptions compound strongly over time.');
INSERT INTO economic_scenario_records VALUES
('capacity_constrained_growth','logistic_constraint',224.0,0.0,'growth slows near a defined capacity or saturation limit','Constrained growth requires a defined mechanism and boundary.');
INSERT INTO economic_scenario_records VALUES
('capital_accumulation_case','capital_stock_flow',180.0,420.0,'investment and depreciation shape long-run output capacity','Capital stock measures can hide quality, maintenance, and obsolescence.');
INSERT INTO economic_scenario_records VALUES
('adjustment_after_shock','target_adjustment',160.0,0.0,'adjustment speed and shocks shape convergence dynamics','Instant adjustment assumptions can hide overshoot and persistence.');

CREATE TABLE economic_growth_records (
    record_name TEXT PRIMARY KEY,
    initial_output REAL NOT NULL,
    growth_rate REAL NOT NULL,
    horizon REAL NOT NULL,
    final_output REAL NOT NULL,
    doubling_time REAL NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO economic_growth_records VALUES
('growth_rate_0_010',100.0,0.010,40.0,149.18,69.31,'Growth-rate assumptions compound strongly over time.');
INSERT INTO economic_growth_records VALUES
('growth_rate_0_025',100.0,0.025,40.0,271.83,27.73,'Growth-rate assumptions compound strongly over time.');
INSERT INTO economic_growth_records VALUES
('growth_rate_0_040',100.0,0.040,40.0,495.30,17.33,'Growth-rate assumptions compound strongly over time.');
