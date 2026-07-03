DROP TABLE IF EXISTS leontief_governance_registry;
DROP TABLE IF EXISTS leontief_system_audit_cases;

CREATE TABLE leontief_governance_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO leontief_governance_registry VALUES
('technical_coefficients','Technical coefficients','Define direct input requirements per unit of sector output.','Represent direct intersectoral dependence.','Coefficients assume stable production recipes over the scenario.'),
('net_requirements','Net requirements matrix','Defines the system matrix I minus A.','Links final demand to total output through a solvable linear system.','Invertibility and conditioning should be reviewed before interpreting results.'),
('leontief_inverse','Leontief inverse','Maps final demand into direct and indirect total output requirements.','Summarizes system-wide intersectoral dependence.','The inverse is a structured model estimate not automatic causal proof.'),
('productivity_condition','Productivity condition','Checks whether the coefficient system can satisfy positive final demand.','Supports economic feasibility and nonnegative output interpretation.','A computed inverse without productivity review can be misleading.'),
('shock_scenario','Shock scenario','Defines a final demand change applied to the system.','Estimates total output response under fixed coefficients.','Demand shocks are not full dynamic forecasts or supply-constrained disruption models.'),
('multiplier_interpretation','Multiplier interpretation','Summarizes total requirements per unit final demand.','Supports compact comparison of sector dependence.','Multipliers depend on sector aggregation boundaries imports and assumptions.'),
('extension_coefficients','Extension coefficients','Attach emissions energy labor water value-added or other intensities to output.','Connect final demand to indirect environmental or social requirements.','Units boundaries allocation rules and provenance must be documented.'),
('responsible_use','Responsible use','Defines how assumptions diagnostics uncertainty and limitations are communicated.','Prevents total-requirements estimates from being overstated.','Leontief systems should support structured interpretation not replace domain judgment.');

CREATE TABLE leontief_system_audit_cases (
    model_name TEXT NOT NULL,
    sectors INTEGER NOT NULL,
    method TEXT NOT NULL,
    coefficient_basis TEXT NOT NULL,
    spectral_radius REAL NOT NULL,
    condition_number REAL NOT NULL,
    productive_system_flag INTEGER NOT NULL,
    maximum_output_multiplier REAL NOT NULL,
    highest_multiplier_sector TEXT NOT NULL,
    total_output_required REAL NOT NULL,
    total_shock_output_change REAL NOT NULL,
    emissions_for_final_demand REAL NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO leontief_system_audit_cases VALUES
('synthetic_leontief_intersectoral_dependence_audit',4,'demand_driven_leontief_system','sector_input_per_unit_output',0.331,2.41,1,1.47,'manufacturing',319.8,36.2,150.6,'The Leontief inverse gives structured dependency estimates under model assumptions not automatic causal proof.');
