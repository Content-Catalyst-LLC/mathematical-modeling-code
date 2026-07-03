DROP TABLE IF EXISTS incidence_representation_registry;
DROP TABLE IF EXISTS incidence_structure_audit_cases;

CREATE TABLE incidence_representation_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO incidence_representation_registry VALUES
('node_definition','Node definition','Defines rows of the incidence matrix.','Determines which entities can accumulate supply demand receive or send flow.','Excluded nodes can distort balance and connectivity conclusions.'),
('edge_definition','Edge definition','Defines columns of the incidence matrix.','Determines which relationships or flow channels are represented.','Different edge definitions produce different incidence structure.'),
('sign_convention','Sign convention','Defines whether source nodes receive -1 or +1 entries.','Determines how edge flows translate into node balances.','Changing sign conventions reverses balance interpretation.'),
('edge_direction','Edge direction','Defines source and target for each edge.','Determines orientation of flow influence dependency or relation.','Direction must match domain meaning not just visual layout.'),
('edge_weight','Edge weight','Defines edge weight semantics.','Determines whether weights represent capacity conductance resistance cost exposure or probability.','Weights may require transformation before entering Laplacian or flow equations.'),
('flow_conservation','Flow conservation','Defines whether Bf = b represents conservation imbalance storage supply or demand.','Determines interpretation of node balances.','Conservation assumptions must be matched to physical or institutional reality.'),
('laplacian_construction','Laplacian construction','Defines how incidence structure is transformed into a graph Laplacian.','Supports diffusion cuts smoothness electrical analogy and spectral analysis.','Unweighted and weighted Laplacians encode different assumptions.');

CREATE TABLE incidence_structure_audit_cases (
    graph_name TEXT NOT NULL,
    node_count INTEGER NOT NULL,
    edge_count INTEGER NOT NULL,
    signed_incidence INTEGER NOT NULL,
    nonzero_incidence_entries INTEGER NOT NULL,
    incidence_density REAL NOT NULL,
    max_absolute_node_balance REAL NOT NULL,
    laplacian_trace REAL NOT NULL,
    rank_estimate INTEGER NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO incidence_structure_audit_cases VALUES
('synthetic_infrastructure_incidence_graph',4,5,1,10,0.5,9.0,10.0,3,'Incidence matrices require node definitions edge definitions sign conventions flow assumptions weights provenance and conservation review.');
