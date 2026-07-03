DROP TABLE IF EXISTS network_flow_registry;
DROP TABLE IF EXISTS network_flow_audit_cases;

CREATE TABLE network_flow_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO network_flow_registry VALUES
('flow_quantity','Flow quantity','Defines what the edge-flow variables measure.','Determines whether flow represents vehicles goods water power data patients money or services.','Flow units and time scale must be documented.'),
('source_sink_definition','Source and sink definition','Defines where flow enters and leaves the network.','Determines the meaning of throughput demand and supply.','Changing sources or sinks changes the problem.'),
('capacity_definition','Capacity definition','Defines upper bounds on edge flow.','Represents physical operational regulatory or institutional limits.','Capacities may vary over time and may be uncertain.'),
('conservation_assumption','Conservation assumption','Defines node-balance constraints.','Determines whether intermediate nodes preserve store lose or transform flow.','Simple conservation can be wrong for systems with storage loss queues or delay.'),
('cost_semantics','Cost semantics','Defines objective coefficients for costed flow.','Determines whether optimization minimizes distance time money risk emissions or loss.','Mixed or unclear costs can produce misleading optimal routes.'),
('cut_interpretation','Cut interpretation','Defines what source-sink partitions mean.','Supports bottleneck and vulnerability analysis.','A minimum cut is a model-based bottleneck not automatically a policy priority.'),
('sensitivity_review','Sensitivity review','Tests how flows change under capacity cost demand and edge perturbations.','Assesses robustness of capacity and bottleneck conclusions.','Optimal flows can be fragile under uncertainty.');

CREATE TABLE network_flow_audit_cases (
    graph_name TEXT NOT NULL,
    node_count INTEGER NOT NULL,
    edge_count INTEGER NOT NULL,
    source_node TEXT NOT NULL,
    sink_node TEXT NOT NULL,
    total_source_outflow REAL NOT NULL,
    total_sink_inflow REAL NOT NULL,
    capacity_violations INTEGER NOT NULL,
    saturated_edge_count INTEGER NOT NULL,
    total_flow_cost REAL NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO network_flow_audit_cases VALUES
('synthetic_capacitated_flow_network',5,6,'source','sink',16.0,16.0,0,2,82.0,'Network flow results depend on node definitions edge definitions capacities costs conservation source sink time scale uncertainty and provenance.');
