DROP TABLE IF EXISTS network_influence_registry;
DROP TABLE IF EXISTS pagerank_audit_cases;

CREATE TABLE network_influence_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO network_influence_registry VALUES
('node_definition','Node definition','Defines the entities ranked by the PageRank vector.','Determines what influence scores can mean.','Changing node definitions can change the ranking.'),
('directed_edge_meaning','Directed edge meaning','Defines what directed links represent.','Determines whether rank means attention authority dependence exposure or flow.','Reversing edge direction can reverse substantive interpretation.'),
('transition_normalization','Transition normalization','Converts directed adjacency into a stochastic matrix.','Determines how rank is distributed across outgoing links.','Normalization changes raw link structure into probabilistic movement.'),
('dangling_node_handling','Dangling-node handling','Defines redistribution for nodes with no outgoing links.','Prevents rank from leaking or becoming trapped.','Different redistribution rules can change scores.'),
('damping_factor','Damping factor','Controls the balance between link-following and teleportation.','Determines how strongly network structure governs rank.','The damping value is a modeling assumption not a neutral constant.'),
('teleportation_vector','Teleportation vector','Defines restart distribution.','Represents background attention personalization or topic sensitivity.','Teleportation choices encode value and scope assumptions.'),
('convergence_tolerance','Convergence tolerance','Defines stopping rule for power iteration.','Determines numerical reliability of ranking output.','Small score differences may not be meaningful without convergence review.'),
('ranking_governance','Ranking governance','Defines how rank scores should be interpreted and used.','Determines accountability for downstream decisions.','Ranking models can create feedback manipulation incentives and concentration effects.');

CREATE TABLE pagerank_audit_cases (
    graph_name TEXT NOT NULL,
    node_count INTEGER NOT NULL,
    edge_count INTEGER NOT NULL,
    damping_factor REAL NOT NULL,
    tolerance REAL NOT NULL,
    converged INTEGER NOT NULL,
    rank_sum REAL NOT NULL,
    dangling_node_count INTEGER NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO pagerank_audit_cases VALUES
('synthetic_directed_network_influence_model',5,8,0.85,1.0e-10,1,1.0,0,'PageRank scores require node definitions directed-edge meaning normalization dangling-node handling damping teleportation convergence graph boundary and provenance review.');
