DROP TABLE IF EXISTS infrastructure_interdependence_governance_registry;
DROP TABLE IF EXISTS infrastructure_dependency_matrix;
DROP TABLE IF EXISTS infrastructure_interdependence_audit_cases;

CREATE TABLE infrastructure_interdependence_governance_registry (
    governance_key TEXT PRIMARY KEY,
    governance_name TEXT NOT NULL,
    modeling_role TEXT NOT NULL,
    review_requirement TEXT NOT NULL,
    responsible_use_warning TEXT NOT NULL
);

INSERT INTO infrastructure_interdependence_governance_registry VALUES
('sector_definition','Sector definition','Defines the infrastructure layers represented by rows and columns.','Document whether sectors represent services assets operators regions facilities or institutional functions.','Sector-level models can hide asset-level bottlenecks and uneven service impacts.'),
('dependency_semantics','Dependency semantics','Defines what cross-sector reliance means.','State whether dependencies are physical cyber geographic operational economic institutional or mixed.','Different dependency types should not be mixed without documentation.'),
('weight_evidence','Weight evidence','Defines how dependency weights were estimated.','Record whether weights come from operational data historical events expert judgment simulations or scenario assumptions.','Judgment-based weights require sensitivity testing and uncertainty flags.'),
('cascade_assumption','Cascade assumption','Defines how disruption is propagated across sectors.','Document whether the model uses one-step multi-step linear threshold delayed or nonlinear propagation.','Linear cascade estimates should not be treated as predictions without validation.'),
('redundancy_review','Redundancy review','Records backups alternative paths spare capacity reserves and workarounds.','Document backup duration fuel access capacity staffing and geographic availability.','Redundancy on paper may not be usable during regional disruptions.'),
('equity_review','Equity review','Connects service loss to people places and uneven vulnerability.','Review whether aggregate sector losses hide concentrated impacts across communities.','Average service loss can understate harm to vulnerable populations.'),
('validation_status','Validation status','Records whether modeled dependencies and cascades have evidence support.','Compare results with historical disruptions exercises operational records and domain expertise.','Unvalidated cascade scenarios should be communicated as exploratory.'),
('decision_boundary','Decision boundary','Defines what the model can and cannot support.','Attach interpretation limits uncertainty notes review status and stop-use conditions to outputs.','The model should inform public decisions not replace accountable institutional judgment.');

CREATE TABLE infrastructure_dependency_matrix (
    dependent_sector TEXT NOT NULL,
    support_sector TEXT NOT NULL,
    dependency_weight REAL NOT NULL,
    dependency_meaning TEXT NOT NULL
);

INSERT INTO infrastructure_dependency_matrix VALUES
('power','power',0.00,'synthetic_sector_dependency'),
('power','water',0.05,'synthetic_sector_dependency'),
('power','communications',0.10,'synthetic_sector_dependency'),
('power','transportation',0.10,'synthetic_sector_dependency'),
('power','health',0.00,'synthetic_sector_dependency'),
('water','power',0.70,'synthetic_sector_dependency'),
('water','water',0.00,'synthetic_sector_dependency'),
('water','communications',0.10,'synthetic_sector_dependency'),
('water','transportation',0.20,'synthetic_sector_dependency'),
('water','health',0.00,'synthetic_sector_dependency'),
('communications','power',0.60,'synthetic_sector_dependency'),
('communications','water',0.00,'synthetic_sector_dependency'),
('communications','communications',0.00,'synthetic_sector_dependency'),
('communications','transportation',0.10,'synthetic_sector_dependency'),
('communications','health',0.00,'synthetic_sector_dependency'),
('transportation','power',0.30,'synthetic_sector_dependency'),
('transportation','water',0.00,'synthetic_sector_dependency'),
('transportation','communications',0.20,'synthetic_sector_dependency'),
('transportation','transportation',0.00,'synthetic_sector_dependency'),
('transportation','health',0.05,'synthetic_sector_dependency'),
('health','power',0.80,'synthetic_sector_dependency'),
('health','water',0.50,'synthetic_sector_dependency'),
('health','communications',0.40,'synthetic_sector_dependency'),
('health','transportation',0.30,'synthetic_sector_dependency'),
('health','health',0.00,'synthetic_sector_dependency');

CREATE TABLE infrastructure_interdependence_audit_cases (
    workflow_name TEXT NOT NULL,
    scenario_name TEXT NOT NULL,
    sector_count INTEGER NOT NULL,
    initial_shock_sector TEXT NOT NULL,
    initial_shock_magnitude REAL NOT NULL,
    highest_dependency_burden_sector TEXT NOT NULL,
    highest_dependency_burden REAL NOT NULL,
    largest_downstream_loss_sector TEXT NOT NULL,
    largest_downstream_loss REAL NOT NULL,
    total_estimated_downstream_loss REAL NOT NULL,
    sensitivity_warning TEXT NOT NULL,
    interpretation_warning TEXT NOT NULL
);

INSERT INTO infrastructure_interdependence_audit_cases VALUES
('infrastructure_interdependence_audit','synthetic_power_disruption_dependency_scenario',5,'power',0.40,'power',2.40,'health',0.32,0.96,'Dependency weights are scenario assumptions and require sensitivity testing.','This one-step linear cascade estimate supports exploratory planning only and does not predict real failure behavior without validation.');
