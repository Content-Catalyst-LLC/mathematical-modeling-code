DROP TABLE IF EXISTS sensitivity_governance_registry;
DROP TABLE IF EXISTS sensitivity_records;

CREATE TABLE sensitivity_governance_registry (
    registry_key TEXT PRIMARY KEY,
    registry_name TEXT NOT NULL,
    analytical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO sensitivity_governance_registry VALUES
('parameter_record','Parameter record','Documents baseline value, unit, source, and tested range.','Keeps model outputs tied to the assumptions that produced them.','Parameter values should not be treated as fixed truths without evidence.'),
('local_sensitivity','Local sensitivity','Measures output response near a baseline parameter value.','Identifies influential assumptions around a reference scenario.','Local sensitivity may miss nonlinear or threshold behavior.'),
('elasticity','Elasticity','Normalizes sensitivity as relative output response to relative parameter change.','Supports comparison across parameters with different units or magnitudes.','Elasticity depends on the chosen baseline and output metric.'),
('parameter_sweep','Parameter sweep','Evaluates outputs across defined parameter values or ranges.','Shows how conclusions change across plausible assumptions.','Sweep conclusions apply only over the tested range.'),
('robustness_classification','Robustness classification','Labels whether a conclusion is stable, conditional, sensitive, or fragile.','Supports claim boundaries and model governance.','Robustness depends on the tested parameter domain.'),
('fragility_warning','Fragility warning','Flags threshold crossings, reversals, or unstable regions.','Prevents overconfident interpretation near critical regimes.','Fragile conclusions require careful communication and review.');

CREATE TABLE sensitivity_records (
    record_id TEXT PRIMARY KEY,
    parameter_name TEXT NOT NULL,
    baseline_value REAL NOT NULL,
    lower_bound REAL NOT NULL,
    upper_bound REAL NOT NULL,
    sensitivity_status TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO sensitivity_records VALUES
('growth_rate_sensitivity','growth_rate',0.35,0.20,0.50,'sensitive','conclusion may depend strongly on growth-rate assumptions');
INSERT INTO sensitivity_records VALUES
('capacity_sensitivity','carrying_capacity',100.0,75.0,125.0,'sensitive','capacity scale strongly affects final stock interpretation');
INSERT INTO sensitivity_records VALUES
('initial_stock_sensitivity','initial_stock',10.0,5.0,20.0,'stable','output variation is limited across this synthetic range');
