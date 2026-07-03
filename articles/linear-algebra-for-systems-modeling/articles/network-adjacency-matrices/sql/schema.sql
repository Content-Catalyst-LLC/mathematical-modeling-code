DROP TABLE IF EXISTS network_adjacency_assumption_registry;
DROP TABLE IF EXISTS network_adjacency_audit_cases;
CREATE TABLE network_adjacency_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);
INSERT INTO network_adjacency_assumption_registry VALUES
('node_definition','Node definition','Defines row and column entities in the adjacency matrix.','Determines what the network can represent.','Boundary choices can exclude important entities.'),
('edge_definition','Edge definition','Defines what nonzero matrix entries mean.','Determines what kind of relationship is modeled.','Different edge definitions produce different networks.'),
('direction_convention','Direction convention','Defines whether A[i,j] points from row to column or column to row.','Determines interpretation of influence exposure dependency and flow.','Reversing direction can invert conclusions.'),
('weight_meaning','Weight meaning','Defines the units or scale of edge weights.','Determines whether weights represent capacity cost frequency probability exposure or similarity.','Weights with different meanings should not be compared casually.'),
('normalization','Normalization','Defines transformations from raw adjacency to transition or diffusion matrices.','Determines downstream matrix interpretation.','Normalization changes matrix meaning and must be documented.');
CREATE TABLE network_adjacency_audit_cases (
    network_name TEXT NOT NULL,
    node_count INTEGER NOT NULL,
    edge_count INTEGER NOT NULL,
    directed INTEGER NOT NULL,
    weighted INTEGER NOT NULL,
    density REAL NOT NULL,
    max_out_weight REAL NOT NULL,
    max_in_weight REAL NOT NULL,
    row_normalized INTEGER NOT NULL,
    warning TEXT NOT NULL
);
INSERT INTO network_adjacency_audit_cases VALUES
('synthetic_infrastructure_dependency_network',5,20,1,1,0.8,2.15,1.95,1,'Adjacency matrices require node boundary edge definition direction convention weight meaning and data provenance review.');
