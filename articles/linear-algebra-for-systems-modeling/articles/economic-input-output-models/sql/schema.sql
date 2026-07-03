DROP TABLE IF EXISTS input_output_governance_registry;
DROP TABLE IF EXISTS input_output_audit_cases;

CREATE TABLE input_output_governance_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO input_output_governance_registry VALUES
('sector_classification','Sector classification','Defines rows and columns of the input-output system.','Determines which production relationships are visible.','Aggregation can hide critical dependencies bottlenecks or heterogeneous activities.'),
('transactions_matrix','Transactions matrix','Records intersectoral flows from supplying sectors to using sectors.','Defines the empirical structure of production interdependence.','Transaction values depend on data source accounting framework year valuation basis and boundary.'),
('technical_coefficients','Technical coefficients','Normalize intersectoral flows by sector output.','Define direct input requirements per unit of output.','Coefficients assume stable production recipes over the scenario.'),
('final_demand','Final demand','Defines the exogenous demand vector applied to the production system.','Drives total output requirements through direct and indirect effects.','Scenario results depend strongly on demand definition and boundary.'),
('leontief_inverse','Leontief inverse','Solves total requirements through the matrix inverse of net requirements.','Captures direct and indirect production requirements.','Invertibility conditioning and productivity assumptions should be reviewed.'),
('multiplier_interpretation','Multiplier interpretation','Summarizes total requirements or extensions per unit of final demand.','Supports compact reporting of system dependence.','Multipliers are estimates under assumptions not automatic causal proof.'),
('environmental_extension','Environmental extension','Applies emissions energy water material labor or other coefficients to output requirements.','Connects final demand to indirect environmental or social impacts.','Extension coefficients require unit boundary allocation and provenance review.'),
('responsible_use','Responsible use','Defines how assumptions uncertainty sensitivity and limitations are documented.','Prevents sector dependency estimates from being overstated.','Input-output models should support structured interpretation not replace domain judgment.');

CREATE TABLE input_output_audit_cases (
    model_name TEXT NOT NULL,
    sectors INTEGER NOT NULL,
    method TEXT NOT NULL,
    coefficient_basis TEXT NOT NULL,
    condition_number REAL NOT NULL,
    maximum_output_multiplier REAL NOT NULL,
    highest_multiplier_sector TEXT NOT NULL,
    total_baseline_output REAL NOT NULL,
    total_shock_output_change REAL NOT NULL,
    total_emissions_for_final_demand REAL NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO input_output_audit_cases VALUES
('synthetic_economic_input_output_audit',4,'demand_driven_leontief_input_output_system','sector_input_per_unit_output',2.41,1.47,'manufacturing',319.8,36.2,150.6,'Input-output multipliers are model-derived dependency estimates not automatic causal proof.');
