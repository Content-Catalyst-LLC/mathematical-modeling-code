DROP TABLE IF EXISTS economic_input_output_governance_registry;
DROP TABLE IF EXISTS technical_coefficients;
DROP TABLE IF EXISTS final_demand;
DROP TABLE IF EXISTS economic_input_output_audit_cases;

CREATE TABLE economic_input_output_governance_registry (
    governance_key TEXT PRIMARY KEY,
    governance_name TEXT NOT NULL,
    modeling_role TEXT NOT NULL,
    review_requirement TEXT NOT NULL,
    responsible_use_warning TEXT NOT NULL
);

INSERT INTO economic_input_output_governance_registry VALUES
('sector_definition','Sector definition','Defines the industries or commodities represented by rows and columns.','Document sector classification aggregation level region table year and table source.','Sector aggregation can hide specialized supply-chain bottlenecks and distributional effects.'),
('coefficient_construction','Coefficient construction','Defines how transactions are converted into technical coefficients.','Record transaction source output denominator price basis domestic/import treatment and matrix orientation.','Technical coefficients are assumptions about fixed production relationships not timeless production laws.'),
('leontief_solution','Leontief solution','Solves total gross output required for final demand.','Check invertibility numerical stability plausibility and economically meaningful output levels.','A mathematically valid solution may still be infeasible under capacity price labor or material constraints.'),
('multiplier_interpretation','Multiplier interpretation','Summarizes direct and indirect output requirements.','Define the multiplier type and attach accounting boundaries.','Multipliers are not automatic measures of welfare productivity social value or policy priority.'),
('demand_scenario','Demand scenario','Defines the final-demand vector or demand shock being modeled.','Document scenario source units timing price basis affected sectors and uncertainty.','Demand shocks are what-if assumptions not forecasts unless externally validated.'),
('import_boundary','Import boundary','Distinguishes domestic requirements from total requirements.','State whether coefficients are domestic total import-adjusted regional national or multi-region.','Local and domestic effects can be overstated when import leakage is ignored.'),
('extension_factors','Environmental and social extension factors','Maps production requirements into emissions energy water labor income or other indicators.','Document extension source year units sector match and uncertainty.','Extensions can inherit both coefficient uncertainty and footprint-factor uncertainty.'),
('decision_boundary','Decision boundary','Defines what the model can and cannot support.','Attach interpretation limits uncertainty notes validation status and stop-use conditions to outputs.','Input-output analysis should inform economic systems reasoning not replace accountable policy judgment.');

CREATE TABLE technical_coefficients (
    input_sector TEXT NOT NULL,
    output_sector TEXT NOT NULL,
    coefficient REAL NOT NULL,
    coefficient_meaning TEXT NOT NULL
);

INSERT INTO technical_coefficients VALUES
('agriculture','agriculture',0.10,'input_required_per_unit_output'),
('agriculture','manufacturing',0.20,'input_required_per_unit_output'),
('agriculture','services',0.05,'input_required_per_unit_output'),
('manufacturing','agriculture',0.15,'input_required_per_unit_output'),
('manufacturing','manufacturing',0.25,'input_required_per_unit_output'),
('manufacturing','services',0.10,'input_required_per_unit_output'),
('services','agriculture',0.05,'input_required_per_unit_output'),
('services','manufacturing',0.10,'input_required_per_unit_output'),
('services','services',0.20,'input_required_per_unit_output');

CREATE TABLE final_demand (
    sector TEXT PRIMARY KEY,
    final_demand REAL NOT NULL
);

INSERT INTO final_demand VALUES
('agriculture',100.0),
('manufacturing',150.0),
('services',200.0);

CREATE TABLE economic_input_output_audit_cases (
    workflow_name TEXT NOT NULL,
    economy_name TEXT NOT NULL,
    sector_count INTEGER NOT NULL,
    final_demand_total REAL NOT NULL,
    gross_output_total REAL NOT NULL,
    highest_multiplier_sector TEXT NOT NULL,
    highest_output_multiplier REAL NOT NULL,
    shock_sector TEXT NOT NULL,
    shock_amount REAL NOT NULL,
    gross_output_change_total REAL NOT NULL,
    leontief_infinity_condition_estimate REAL NOT NULL,
    solvability_warning TEXT NOT NULL,
    interpretation_warning TEXT NOT NULL
);

INSERT INTO economic_input_output_audit_cases VALUES
('economic_input_output_audit','synthetic_three_sector_economy',3,450.0,763.099081201887,'manufacturing',1.951825177111,'manufacturing',25.0,48.795629500869,2.147504345667,'The Leontief matrix must be invertible and checked for numerical stability and plausibility.','Input-output results depend on fixed coefficients aggregation domestic/import boundaries price basis final-demand assumptions and capacity limits. Multipliers are not automatic policy conclusions.');
