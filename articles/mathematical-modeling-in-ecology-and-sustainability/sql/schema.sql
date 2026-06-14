-- Mathematical modeling in ecology and sustainability governance schema.

DROP TABLE IF EXISTS ecology_domain_guide;
DROP TABLE IF EXISTS resource_scenario;
DROP TABLE IF EXISTS ecology_model_register;
DROP TABLE IF EXISTS ecology_model_role_type;

CREATE TABLE ecology_model_role_type (
    model_role TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    typical_failure TEXT NOT NULL
);

CREATE TABLE ecology_model_register (
    record_id INTEGER PRIMARY KEY,
    record_key TEXT NOT NULL,
    domain TEXT NOT NULL,
    model_role TEXT NOT NULL,
    model_family TEXT NOT NULL,
    sustainability_question TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('active', 'review', 'revise', 'archive')),
    FOREIGN KEY (model_role) REFERENCES ecology_model_role_type(model_role)
);

CREATE TABLE resource_scenario (
    scenario_key TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    initial_stock REAL NOT NULL,
    growth_rate REAL NOT NULL,
    carrying_capacity REAL NOT NULL,
    extraction REAL NOT NULL,
    climate_stress REAL NOT NULL,
    years INTEGER NOT NULL,
    minimum_stock REAL NOT NULL
);

CREATE TABLE ecology_domain_guide (
    area TEXT PRIMARY KEY,
    modeling_use TEXT NOT NULL,
    typical_model_forms TEXT NOT NULL
);

INSERT INTO ecology_model_role_type VALUES
('stock_flow_review','Reviews renewable stock, regeneration, extraction, and depletion.','Stock appears stable only because extraction or stress is understated.'),
('threshold_review','Assesses distance to minimum ecological threshold.','Threshold is treated as exact or ignored entirely.'),
('scenario_analysis','Compares ecological futures under stress, policy, or management pathways.','One baseline is treated as destiny.'),
('network_review','Reviews biodiversity dependencies and ecological interactions.','Species or habitat interactions are omitted.'),
('adaptive_management','Connects monitoring triggers to changed management action.','Model results are not linked to governance or update process.');

INSERT INTO ecology_model_register(record_key, domain, model_role, model_family, sustainability_question, status) VALUES
('resource_stock_model','renewable_resource_management','stock_flow_review','dynamic_resource_model','Does extraction remain within regenerative capacity?','active'),
('resilience_model','ecosystem_resilience','threshold_review','resilience_margin_model','How close is the system to a minimum ecological threshold?','review'),
('climate_stress_model','climate_adaptation','scenario_analysis','stress_test_model','How does climate stress change long-term stock viability?','review'),
('biodiversity_model','conservation_planning','network_review','biodiversity_dependency_model','Which ecological interactions and dependencies need review?','review'),
('governance_model','sustainability_governance','adaptive_management','monitoring_trigger_model','When should management action change as evidence updates?','review');

INSERT INTO resource_scenario VALUES
('baseline','Baseline managed use',420.0,0.24,800.0,36.0,0.04,25,250.0),
('high_extraction','High extraction pressure',420.0,0.24,800.0,64.0,0.04,25,250.0),
('climate_stress','Climate stress with lower regeneration',420.0,0.24,800.0,42.0,0.22,25,250.0),
('restoration_pathway','Restoration and reduced extraction',420.0,0.28,860.0,24.0,0.03,25,250.0),
('adaptive_management','Adaptive use with monitoring trigger',420.0,0.25,820.0,32.0,0.08,25,250.0);

INSERT INTO ecology_domain_guide VALUES
('conservation_biology','Assess species viability habitat corridors and extinction risk','Population viability models spatial models metapopulation models'),
('fisheries_and_forestry','Balance harvest with regeneration','Stock-recruitment models yield models age-structured models'),
('water_systems','Represent flow demand drought quality and allocation','Hydrologic models optimization watershed models'),
('climate_adaptation','Test vulnerability and adaptation pathways','Scenario models risk models spatial exposure models'),
('urban_sustainability','Connect land use infrastructure transport energy and heat','Systems models geospatial models network models'),
('agriculture_and_food_systems','Represent yields soil water nutrients and climate stress','Crop models nutrient models sustainability assessment'),
('biodiversity_planning','Evaluate habitat interaction and landscape connectivity','Network models species distribution models corridor models'),
('environmental_policy','Compare interventions standards incentives and long-term pathways','Scenario modeling cost-effectiveness integrated assessment');
