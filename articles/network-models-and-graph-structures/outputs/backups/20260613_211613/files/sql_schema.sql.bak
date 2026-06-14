DROP TABLE IF EXISTS network_component_guide;
DROP TABLE IF EXISTS infrastructure_edge;
DROP TABLE IF EXISTS network_model_register;
DROP TABLE IF EXISTS network_component_type;

CREATE TABLE network_component_type (
    component_type TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    typical_failure TEXT NOT NULL
);

CREATE TABLE network_model_register (
    record_id INTEGER PRIMARY KEY,
    record_key TEXT NOT NULL,
    component_type TEXT NOT NULL,
    expression_or_structure TEXT NOT NULL,
    interpretation TEXT NOT NULL,
    review_question TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('active', 'review', 'revise', 'archive')),
    FOREIGN KEY (component_type) REFERENCES network_component_type(component_type)
);

CREATE TABLE infrastructure_edge (
    edge_id INTEGER PRIMARY KEY,
    source TEXT NOT NULL,
    target TEXT NOT NULL,
    relationship TEXT NOT NULL,
    weight REAL NOT NULL CHECK (weight >= 0),
    evidence_quality TEXT NOT NULL CHECK (evidence_quality IN ('high', 'medium', 'low'))
);

CREATE TABLE network_component_guide (
    component_type TEXT PRIMARY KEY,
    meaning TEXT NOT NULL,
    example TEXT NOT NULL,
    review_question TEXT NOT NULL
);

INSERT INTO network_component_type VALUES
('node','Entity represented in the graph.','Node scale or boundary is unclear.'),
('edge','Relationship between nodes.','Edge meaning is ambiguous or mixed.'),
('edge_weight','Strength or magnitude of a relationship.','Weight is estimated weakly or treated as exact.'),
('direction_rule','Rule for edge orientation.','Direction does not match operational reality.'),
('diagnostic','Computed graph measure.','Metric is overinterpreted.'),
('process_rule','Rule for flow, diffusion, contagion, or cascade.','Graph path is confused with actual process.'),
('validation_diagnostic','Credibility check.','Missing-edge and weight uncertainty are not tested.'),
('network_boundary','Included nodes and relationships.','Important nodes or relationships are excluded.');

INSERT INTO network_model_register(record_key, component_type, expression_or_structure, interpretation, review_question, status) VALUES
('node_definition','node','facility_or_service_asset','Nodes represent infrastructure assets','Are critical assets included at the right scale?','review'),
('directed_dependency_edge','edge','source_to_target','Directed edge indicates dependency or service flow','Does edge direction match operational reality?','review'),
('edge_weight','edge_weight','w_ij','Weight represents dependency strength or criticality','How was weight estimated and validated?','review'),
('centrality_diagnostic','diagnostic','in_degree out_degree reachability','Diagnostics identify structurally important nodes','Does structural centrality match practical importance?','active'),
('edge_evidence_quality','validation_diagnostic','evidence_quality','Each edge receives an evidence-quality flag','Are low-evidence edges reviewed before decision use?','review'),
('boundary_definition','network_boundary','V_and_E_scope','The model states included nodes and edges','What relationships are excluded?','review');

INSERT INTO infrastructure_edge(source, target, relationship, weight, evidence_quality) VALUES
('power_substation','hospital','electricity_supply',0.95,'high'),
('power_substation','water_treatment','electricity_supply',0.90,'high'),
('communications_hub','hospital','data_connectivity',0.70,'medium'),
('fuel_depot','power_substation','fuel_dependency',0.60,'medium'),
('transport_hub','hospital','patient_transfer',0.50,'medium'),
('transport_hub','fuel_depot','fuel_delivery',0.65,'medium'),
('water_treatment','hospital','water_service',0.80,'high'),
('emergency_depot','hospital','emergency_supply',0.75,'medium'),
('communications_hub','emergency_depot','coordination',0.55,'medium'),
('power_substation','communications_hub','electricity_supply',0.85,'high');

INSERT INTO network_component_guide VALUES
('node','Entity represented in the graph','facility','What counts as a unit?'),
('edge','Relationship between nodes','dependency','What kind of relationship is modeled?'),
('edge_weight','Strength or magnitude of relationship','w_ij','How was weight estimated?'),
('direction_rule','Rule for edge orientation','source_to_target','Does direction match reality?'),
('diagnostic','Computed graph measure','in_degree','What does the measure claim?'),
('process_rule','Rule for flow or spread','x_next=F(x,A)','Does the process match evidence?'),
('validation_diagnostic','Credibility check','missing-edge sensitivity','Are conclusions robust?'),
('network_boundary','Included nodes and relationships','V and E scope','What is excluded?');
