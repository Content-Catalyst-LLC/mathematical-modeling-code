DROP TABLE IF EXISTS urban_congestion_governance_registry;
DROP TABLE IF EXISTS urban_parameter_records;
DROP TABLE IF EXISTS urban_scenario_records;
DROP TABLE IF EXISTS urban_diagnostic_records;

CREATE TABLE urban_congestion_governance_registry (
    registry_key TEXT PRIMARY KEY,
    registry_name TEXT NOT NULL,
    analytical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO urban_congestion_governance_registry VALUES
('boundary_record','Boundary record','Defines whether the model represents a link, corridor, intersection, station, curb zone, district, or metropolitan system.','Prevents local results from being interpreted as full-system outcomes.','Urban congestion conclusions are not meaningful without a defined boundary and spillover context.'),
('flow_record','Flow record','Documents vehicle flows, person flows, freight flows, transit flows, pedestrian flows, and inflow-outflow timing.','Connects congestion to movement and accumulation.','Vehicle flow should not be treated as the only mobility outcome.'),
('capacity_record','Capacity record','Documents physical, operational, institutional, curbside, transit, signal, or service capacity constraints.','Connects delay and queue formation to service limits.','Capacity depends on design, operations, behavior, incidents, and curb use.'),
('behavior_record','Behavior record','Documents route choice, mode choice, departure-time choice, parking behavior, induced demand, and land-use adjustment.','Connects congestion to feedback and adaptation.','Fixed-demand assumptions can mislead in long-run planning.'),
('multimodal_record','Multimodal record','Documents transit, walking, cycling, ride-hail, freight, curbside, and emergency access assumptions.','Connects mobility to person movement and access rather than vehicle throughput alone.','Ignoring non-auto modes can distort congestion and equity interpretation.'),
('equity_record','Equity record','Documents travel burden, access, exposure, affordability, mode constraints, safety, and neighborhood impacts.','Connects congestion outcomes to distributional consequences.','Average travel-time improvements can hide unequal burden or local harm.'),
('claim_boundary','Claim boundary','Defines whether the model supports teaching, operations, scenario comparison, infrastructure planning, or decision support.','Prevents overclaiming and scope drift.','Urban conclusions should not exceed boundary definitions, data evidence, behavioral assumptions, uncertainty, equity review, and tested scope.');

CREATE TABLE urban_parameter_records (
    parameter_name TEXT PRIMARY KEY,
    value REAL NOT NULL,
    unit TEXT NOT NULL,
    interpretation TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO urban_parameter_records VALUES
('q',1800.0,'vehicles per hour','traffic flow','Flow unit and mode must be documented.');
INSERT INTO urban_parameter_records VALUES
('k',35.0,'vehicles per kilometer','density','Density depends on vehicle mix, lane definition, and measurement method.');
INSERT INTO urban_parameter_records VALUES
('v_f',60.0,'kilometers per hour','free-flow speed','Free-flow speed should not be treated as a universal target.');
INSERT INTO urban_parameter_records VALUES
('k_j',140.0,'vehicles per kilometer','jam density','Jam density represents near-standstill conditions.');
INSERT INTO urban_parameter_records VALUES
('C',2000.0,'vehicles per hour','capacity','Capacity depends on design, signals, incidents, weather, and curb use.');
INSERT INTO urban_parameter_records VALUES
('mu',0.10,'per year','demand adjustment rate','Long-run demand can change after capacity or accessibility changes.');
INSERT INTO urban_parameter_records VALUES
('theta',0.08,'per minute','accessibility decay','Accessibility assumptions shape equity interpretation.');

CREATE TABLE urban_scenario_records (
    scenario_name TEXT PRIMARY KEY,
    model_type TEXT NOT NULL,
    demand REAL NOT NULL,
    capacity REAL NOT NULL,
    final_queue REAL NOT NULL,
    total_delay REAL NOT NULL,
    travel_time REAL NOT NULL,
    interpretation TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO urban_scenario_records VALUES
('below_capacity_corridor','queue_and_bpr',1800.0,2000.0,0.0,0.0,21.9683,'demand below capacity produces limited queue accumulation','Below-capacity results depend on capacity assumptions.');
INSERT INTO urban_scenario_records VALUES
('over_capacity_bottleneck','queue_and_bpr',2300.0,2000.0,900.0,1351.5,25.2476,'demand above capacity produces persistent queue and delay','Over-capacity delays can spill back upstream.');
INSERT INTO urban_scenario_records VALUES
('capacity_expansion_with_induced_demand','capacity_adjustment',2541.0,2600.0,0.0,0.0,22.7382,'capacity expansion may reduce delay while long-run demand adjusts upward','Capacity expansion should be reviewed with induced demand and land-use feedback.');
INSERT INTO urban_scenario_records VALUES
('transit_priority_case','multimodal_capacity',1200.0,1600.0,0.0,0.0,20.9492,'transit priority can reduce person-delay when person throughput is considered','Transit priority should be evaluated through access, reliability, and person throughput.');

CREATE TABLE urban_diagnostic_records (
    diagnostic_name TEXT PRIMARY KEY,
    value REAL NOT NULL,
    unit TEXT NOT NULL,
    interpretation TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO urban_diagnostic_records VALUES
('critical_density_example',70.0,'vehicles per kilometer','density at maximum flow in simple parabolic model','Critical density depends on the selected flow-density relation.');
INSERT INTO urban_diagnostic_records VALUES
('flow_at_density_example',1575.0,'vehicles per hour','flow estimated from density, free-flow speed, and jam density','Fundamental diagrams are context-specific, not universal laws.');
INSERT INTO urban_diagnostic_records VALUES
('accessibility_example',591.858,'weighted opportunities','accessibility from opportunities and travel times','Accessibility depends on opportunity definition and travel-cost assumptions.');
INSERT INTO urban_diagnostic_records VALUES
('distributional_delay_burden_example',110.0,'weighted minutes','delay burden weighted across groups','Average delay can hide unequal burden.');
INSERT INTO urban_diagnostic_records VALUES
('curb_occupancy_step_example',19.0,'occupied spaces','curb occupancy after use and release','Curb dynamics can reduce effective road and transit capacity.');
