DROP TABLE IF EXISTS network_modeling_governance_registry;
DROP TABLE IF EXISTS network_system_modeling_audit_cases;
DROP TABLE IF EXISTS synthetic_network_edges;

CREATE TABLE network_modeling_governance_registry (
    governance_key TEXT PRIMARY KEY,
    governance_name TEXT NOT NULL,
    modeling_role TEXT NOT NULL,
    review_requirement TEXT NOT NULL,
    responsible_use_warning TEXT NOT NULL
);

INSERT INTO network_modeling_governance_registry VALUES
('node_definition','Node definition','Defines what each row and column in the network matrix represents.','Document whether nodes are facilities regions agents documents states sectors or components.','Centrality and vulnerability metrics are not meaningful if node types are unclear or mixed without justification.'),
('edge_definition','Edge definition','Defines what a relationship means in the network.','Document whether edges represent flow dependency similarity communication probability cost or influence.','A connection does not automatically imply causality authority capacity or reliability.'),
('weight_semantics','Weight semantics','Defines how edge magnitudes should be interpreted.','State whether larger weights mean stronger cheaper riskier more likely more costly or more capacious relationships.','Weight meaning must be clear before ranking optimizing or comparing network structure.'),
('directionality','Directionality','Defines whether links are symmetric or directional.','Document whether adjacency matrices are symmetric and whether in-degree and out-degree require separate interpretation.','Undirected simplification can hide asymmetric dependency or influence.'),
('boundary_scope','Boundary scope','Defines which nodes edges and external dependencies are included or excluded.','Maintain a boundary register with omitted nodes omitted edges and external support assumptions.','Network vulnerability may be underestimated when external dependencies are excluded.'),
('centrality_interpretation','Centrality interpretation','Connects centrality metrics to specific definitions of importance.','Report which centrality metric was used and why it matches the modeling purpose.','Centrality means importance only under the chosen representation and metric.'),
('stress_testing','Stress testing','Compares matrix outputs under node edge weight or boundary perturbations.','Document stress scenarios removed elements and scenario assumptions.','Stress tests are scenario analyses not predictions unless validated against real failure behavior.'),
('visualization_limits','Visualization limits','Defines how network graphics should be interpreted.','State whether layout is geographic algorithmic schematic or metric-based.','Graph layout can visually imply structure not supported by the model.');

CREATE TABLE synthetic_network_edges (
    source_node TEXT NOT NULL,
    target_node TEXT NOT NULL,
    weight REAL NOT NULL,
    edge_meaning TEXT NOT NULL
);

INSERT INTO synthetic_network_edges VALUES
('A','B',4.0,'relative_service_capacity'),
('A','C',2.0,'relative_service_capacity'),
('B','C',3.0,'relative_service_capacity'),
('B','D',5.0,'relative_service_capacity'),
('C','D',1.0,'relative_service_capacity'),
('D','E',2.0,'relative_service_capacity');

CREATE TABLE network_system_modeling_audit_cases (
    workflow_name TEXT NOT NULL,
    network_name TEXT NOT NULL,
    node_count INTEGER NOT NULL,
    edge_count INTEGER NOT NULL,
    total_weight REAL NOT NULL,
    highest_weighted_degree_node TEXT NOT NULL,
    highest_weighted_degree REAL NOT NULL,
    laplacian_trace REAL NOT NULL,
    baseline_component_count INTEGER NOT NULL,
    stressed_component_count INTEGER NOT NULL,
    removed_edge TEXT NOT NULL,
    vulnerability_warning TEXT NOT NULL,
    interpretation_warning TEXT NOT NULL
);

INSERT INTO network_system_modeling_audit_cases VALUES
('network_system_modeling_audit','synthetic_infrastructure_service_network',5,6,17.0,'B',12.0,34.0,1,1,'B-D','The edge-removal scenario is a simplified stress test and does not predict real failure behavior without validation.','Network metrics depend on node definitions edge meanings weights directionality boundaries and missing-edge assumptions.');
