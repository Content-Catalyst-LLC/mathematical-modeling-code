DROP TABLE IF EXISTS infrastructure_modeling_registry;
DROP TABLE IF EXISTS infrastructure_network_audit_cases;

CREATE TABLE infrastructure_modeling_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO infrastructure_modeling_registry VALUES
('asset_definition','Asset definition','Defines the nodes of the infrastructure graph.','Determines what physical functional spatial or institutional entities are represented.','Changing asset definitions changes connectivity criticality and vulnerability metrics.'),
('edge_definition','Edge definition','Defines the relationships among infrastructure nodes.','Determines whether edges represent physical links flows dependencies access control or governance.','Different edge meanings should not be mixed without documentation.'),
('layer_boundary','Layer boundary','Defines infrastructure layers in a multilayer network.','Determines whether transportation energy water communication logistics health and institutional layers are separated or combined.','Cross-layer dependency can be hidden if layers are collapsed.'),
('capacity_semantics','Capacity semantics','Defines capacity values on nodes or edges.','Determines whether capacity means design rating observed throughput emergency capacity degraded capacity or service capability.','Capacity values require units time scale and provenance.'),
('dependency_rule','Dependency rule','Defines how failure or degradation propagates across links.','Supports cascading-failure and interdependence analysis.','Dependency strength and thresholds must be justified.'),
('scenario_design','Scenario design','Defines disruptions hazards demand shifts and recovery assumptions.','Supports stress testing and resilience analysis.','Scenario choices determine what vulnerabilities become visible.'),
('recovery_priority','Recovery priority','Defines restoration objective and repair sequence logic.','Determines how service recovery is valued over time.','Recovery priorities can encode equity economic institutional or political assumptions.'),
('governance_review','Governance review','Defines provenance security accountability and interpretation controls.','Connects infrastructure metrics to responsible decision use.','Infrastructure outputs can affect public investment access safety and accountability.');

CREATE TABLE infrastructure_network_audit_cases (
    network_name TEXT NOT NULL,
    node_count INTEGER NOT NULL,
    edge_count INTEGER NOT NULL,
    layer_count INTEGER NOT NULL,
    critical_asset_count INTEGER NOT NULL,
    interdependency_edge_count INTEGER NOT NULL,
    total_baseline_capacity REAL NOT NULL,
    disrupted_asset TEXT NOT NULL,
    remaining_capacity_after_disruption REAL NOT NULL,
    capacity_loss_fraction REAL NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO infrastructure_network_audit_cases VALUES
('synthetic_multilayer_infrastructure_network',6,7,6,5,3,400.0,'power_substation',160.0,0.6,'Infrastructure network results depend on asset definitions edge definitions layer boundaries capacity units dependency rules scenarios operating conditions provenance security and vulnerability interpretation.');
