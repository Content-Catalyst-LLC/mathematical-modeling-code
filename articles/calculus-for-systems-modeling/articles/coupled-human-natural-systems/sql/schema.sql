DROP TABLE IF EXISTS coupled_systems_governance_registry;
DROP TABLE IF EXISTS coupled_parameter_records;
DROP TABLE IF EXISTS coupled_scenario_records;
DROP TABLE IF EXISTS coupled_diagnostic_records;

CREATE TABLE coupled_systems_governance_registry (
    registry_key TEXT PRIMARY KEY,
    registry_name TEXT NOT NULL,
    analytical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO coupled_systems_governance_registry VALUES
('boundary_record','Boundary record','Defines the coupled system boundary, spatial scale, time scale, and external flows.','Prevents local results from hiding imported impacts, leakage, or displaced burden.','Coupled-system conclusions are not meaningful without a defined boundary and external-flow record.'),
('human_system_record','Human-system record','Documents population, demand, livelihoods, infrastructure, institutions, behavior, technology, inequality, and adaptive capacity.','Prevents people from being reduced to a homogeneous pressure term.','Human assumptions should include constraints, institutions, rights, and distribution where relevant.'),
('natural_system_record','Natural-system record','Documents resource stocks, regeneration, ecosystem condition, habitat, climate stress, biodiversity, water, soil, and thresholds.','Prevents nature from being reduced to a passive resource supply.','Ecological assumptions should include uncertainty, thresholds, and omitted mechanisms.'),
('coupling_record','Coupling record','Documents extraction, restoration, emissions, exposure, feedback, trade, leakage, displacement, and governance response.','Connects human activity and natural response explicitly.','Coupling terms should represent mechanisms, not just arrows.'),
('governance_record','Governance record','Documents rules, legitimacy, enforcement, capacity, participation, monitoring, and accountability.','Connects system outcomes to institutions and decision processes.','Governance should not be treated as a fixed or neutral constant without justification.'),
('equity_record','Equity record','Documents exposure, access, benefit, burden, rights, culture, participation, and vulnerability.','Connects coupled-system outputs to distributional consequences.','Aggregate efficiency can hide unequal burden, displacement, and environmental injustice.'),
('claim_boundary','Claim boundary','Defines whether the model supports teaching, exploratory scenarios, planning, policy analysis, or decision support.','Prevents overclaiming and scope drift.','Coupled-system conclusions should not exceed boundary definitions, data evidence, mechanism plausibility, uncertainty, equity review, and tested scope.');

CREATE TABLE coupled_parameter_records (
    parameter_name TEXT PRIMARY KEY,
    value REAL NOT NULL,
    unit TEXT NOT NULL,
    interpretation TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO coupled_parameter_records VALUES
('r',0.08,'per year','natural regeneration rate','Regeneration may vary with habitat, climate, age structure, and system state.');
INSERT INTO coupled_parameter_records VALUES
('K',100.0,'stock units','carrying capacity','Carrying capacity may change with climate, land use, pollution, or habitat loss.');
INSERT INTO coupled_parameter_records VALUES
('q_e',0.003,'per effort per stock','extraction efficiency','Technology can increase pressure or reduce waste depending on context.');
INSERT INTO coupled_parameter_records VALUES
('A',12.0,'effort units','human extraction effort','Effort reflects livelihoods, demand, technology, and constraints.');
INSERT INTO coupled_parameter_records VALUES
('G',0.60,'index','governance strength','Governance quality includes legitimacy, enforcement, resources, and trust.');
INSERT INTO coupled_parameter_records VALUES
('mu',0.20,'per year','adjustment rate','Human response may be slow, unequal, or constrained.');
INSERT INTO coupled_parameter_records VALUES
('Nc',30.0,'stock units','critical natural threshold','Thresholds are uncertain and should be stress-tested.');

CREATE TABLE coupled_scenario_records (
    scenario_name TEXT PRIMARY KEY,
    model_type TEXT NOT NULL,
    final_human_pressure REAL NOT NULL,
    final_natural_stock REAL NOT NULL,
    cumulative_extraction REAL NOT NULL,
    cumulative_burden REAL NOT NULL,
    interpretation TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO coupled_scenario_records VALUES
('baseline_coupled_resource','resource_governance_feedback',11.62,66.2,123.8,14.4,'Coupled outcome depends on regeneration, extraction, stress, governance, adaptation, and vulnerability.','Baseline scenario requires mechanism and boundary review.');
INSERT INTO coupled_scenario_records VALUES
('high_extraction_low_governance','resource_governance_feedback',17.84,22.5,210.7,31.2,'High extraction and weak governance can push the system toward threshold risk.','Threshold status and distributional burden require review.');
INSERT INTO coupled_scenario_records VALUES
('restoration_and_adaptation','resource_governance_feedback',9.31,88.7,84.3,4.8,'Restoration and adaptation can reduce extraction pressure and burden.','Assumptions about adaptation capacity and governance must be documented.');

CREATE TABLE coupled_diagnostic_records (
    diagnostic_name TEXT PRIMARY KEY,
    value REAL NOT NULL,
    unit TEXT NOT NULL,
    interpretation TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO coupled_diagnostic_records VALUES
('baseline_regeneration_at_stock_80',1.28,'stock units per year','regeneration at stock 80','Regeneration may vary with habitat, climate, and system state.');
INSERT INTO coupled_diagnostic_records VALUES
('baseline_extraction_example',2.88,'stock units per year','effort-based extraction example','Extraction assumptions should include technology, livelihoods, and constraints.');
INSERT INTO coupled_diagnostic_records VALUES
('burden_example',0.64,'burden units','distributional burden example','Aggregate outcomes can hide unequal burden.');
INSERT INTO coupled_diagnostic_records VALUES
('threshold_status_example',1.0,'binary','threshold review status','Thresholds are uncertain and should be stress-tested.');
