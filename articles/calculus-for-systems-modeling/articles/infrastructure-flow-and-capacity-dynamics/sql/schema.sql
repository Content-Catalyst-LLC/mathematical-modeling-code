DROP TABLE IF EXISTS infrastructure_governance_registry;
DROP TABLE IF EXISTS infrastructure_parameter_records;
DROP TABLE IF EXISTS infrastructure_scenario_records;
DROP TABLE IF EXISTS infrastructure_bottleneck_records;

CREATE TABLE infrastructure_governance_registry (
    registry_key TEXT PRIMARY KEY,
    registry_name TEXT NOT NULL,
    analytical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO infrastructure_governance_registry VALUES
('flow_record','Flow record','Defines what moves through the system, including units, time scale, origin, destination, and measurement boundary.','Makes arrival, service, and throughput dynamics explicit.','Infrastructure outputs cannot be interpreted responsibly if flow definitions are unclear.'),
('capacity_record','Capacity record','Documents physical, operational, effective, regulatory, and stress-condition capacity assumptions.','Separates nominal capacity from reliable service capacity.','Nominal capacity may differ from effective capacity.'),
('queue_record','Queue record','Documents visible and hidden backlogs, waiting times, queue discipline, and service constraints.','Connects rate imbalance to user delay and accumulated backlog.','Average throughput can hide waiting-time and backlog effects.'),
('bottleneck_record','Bottleneck record','Documents limiting stages, downstream constraints, routing assumptions, and effective capacity.','Identifies where local constraints limit system throughput.','The apparent bottleneck may shift under disruption or demand change.'),
('maintenance_record','Maintenance record','Documents asset condition, capacity decay, repair rates, inspection uncertainty, and deferred maintenance.','Connects present capacity to future reliability.','Capacity should not be assumed fixed without maintenance records.'),
('resilience_record','Resilience record','Documents buffers, redundancy, failure modes, cascading dependencies, and recovery rates.','Connects normal operation to stress performance.','Spare capacity may be essential resilience, not waste.'),
('claim_boundary','Claim boundary','Defines whether the model supports teaching, monitoring, scenario comparison, investment planning, emergency planning, or decision support.','Prevents overclaiming and scope drift.','Infrastructure conclusions should not exceed flow definitions, capacity evidence, operating conditions, uncertainty, governance feasibility, and tested scope.');

CREATE TABLE infrastructure_parameter_records (
    parameter_name TEXT PRIMARY KEY,
    value REAL NOT NULL,
    unit TEXT NOT NULL,
    interpretation TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO infrastructure_parameter_records VALUES
('lambda',95.0,'units per hour','arrival or demand rate','Peak and average demand should be documented separately.');
INSERT INTO infrastructure_parameter_records VALUES
('mu',100.0,'units per hour','service capacity','Nominal capacity may differ from effective capacity.');
INSERT INTO infrastructure_parameter_records VALUES
('buffer_capacity',300.0,'units','maximum buffer or storage capacity','Buffers can saturate under sustained imbalance.');
INSERT INTO infrastructure_parameter_records VALUES
('base_delay',1.0,'time units','delay under low utilization','Delay rises nonlinearly near capacity.');
INSERT INTO infrastructure_parameter_records VALUES
('decay_rate',0.03,'per year','capacity decay rate','Capacity should not be assumed fixed without maintenance records.');
INSERT INTO infrastructure_parameter_records VALUES
('recovery_rate',0.15,'per period','post-disruption recovery rate','Recovery depends on labor, parts, finance, and governance.');

CREATE TABLE infrastructure_scenario_records (
    scenario_name TEXT PRIMARY KEY,
    system_type TEXT NOT NULL,
    final_queue REAL NOT NULL,
    average_utilization REAL NOT NULL,
    maximum_delay REAL NOT NULL,
    interpretation TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO infrastructure_scenario_records VALUES
('baseline_spare_capacity','queue_capacity',0.0,0.75,3.4,'spare capacity keeps queues low','Spare capacity may be essential resilience, not waste.');
INSERT INTO infrastructure_scenario_records VALUES
('near_capacity_operation','queue_capacity',0.0,0.95,16.2,'near-capacity operation creates high delay sensitivity','Near-capacity operation increases fragility.');
INSERT INTO infrastructure_scenario_records VALUES
('over_capacity_backlog','queue_capacity',360.0,1.15,800.2,'arrival rate above capacity causes backlog accumulation','Over-capacity operation creates accumulated delay.');
INSERT INTO infrastructure_scenario_records VALUES
('series_bottleneck','network_bottleneck',120.0,1.06,800.2,'minimum stage capacity limits effective throughput','The apparent bottleneck may shift under disruption.');
INSERT INTO infrastructure_scenario_records VALUES
('capacity_decay_case','maintenance_capacity',50.0,1.05,800.2,'capacity decay can create congestion even if demand is unchanged','Capacity should not be assumed fixed without maintenance records.');

CREATE TABLE infrastructure_bottleneck_records (
    record_name TEXT PRIMARY KEY,
    stage_capacities TEXT NOT NULL,
    effective_capacity REAL NOT NULL,
    bottleneck_stage INTEGER NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO infrastructure_bottleneck_records VALUES
('series_process_bottleneck','140,120,90,130',90.0,3,'Effective capacity is limited by the smallest stage capacity.');
