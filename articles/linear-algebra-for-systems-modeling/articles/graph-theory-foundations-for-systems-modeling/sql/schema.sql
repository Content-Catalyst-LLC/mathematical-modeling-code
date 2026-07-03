DROP TABLE IF EXISTS graph_modeling_registry;
DROP TABLE IF EXISTS graph_structure_audit_cases;

CREATE TABLE graph_modeling_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO graph_modeling_registry VALUES
('node_definition','Node definition','Defines the elements of the vertex set V.','Determines what entities the graph can represent.','Changing node definitions can change every graph metric.'),
('edge_definition','Edge definition','Defines the relationships in the edge set E.','Determines what counts as connection flow dependence or interaction.','Different edge definitions can produce different systems conclusions.'),
('graph_boundary','Graph boundary','Defines what is included in or excluded from the graph.','Determines whether the modeled system is complete partial local or sampled.','Excluded nodes and edges can distort connectivity and vulnerability claims.'),
('direction_convention','Direction convention','Defines orientation for directed edges.','Determines how reachability influence citation dependency and flow are interpreted.','Reversing directions can reverse substantive conclusions.'),
('weight_semantics','Weight semantics','Defines numeric meaning of edge weights.','Determines whether weights represent distance capacity cost frequency exposure or similarity.','Weights with different meanings require different algorithms and transformations.'),
('temporal_scope','Temporal scope','Defines the time period represented by nodes and edges.','Determines whether the graph is static historical dynamic or streaming.','Static graphs can hide time ordering and changing structure.'),
('metric_interpretation','Metric interpretation','Defines how graph metrics should be read in domain context.','Determines whether degree centrality distance or cuts have substantive meaning.','Graph metrics are structural indicators not automatic explanations.');

CREATE TABLE graph_structure_audit_cases (
    graph_name TEXT NOT NULL,
    node_count INTEGER NOT NULL,
    edge_count INTEGER NOT NULL,
    directed INTEGER NOT NULL,
    weighted INTEGER NOT NULL,
    component_count INTEGER NOT NULL,
    max_degree INTEGER NOT NULL,
    min_degree INTEGER NOT NULL,
    average_degree REAL NOT NULL,
    has_cycle INTEGER NOT NULL,
    graph_density REAL NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO graph_structure_audit_cases VALUES
('synthetic_infrastructure_graph_foundations',5,6,0,1,1,3,2,2.4,1,0.6,'Graph metrics require node definitions edge definitions graph boundary direction conventions weight semantics time period and provenance review.');
