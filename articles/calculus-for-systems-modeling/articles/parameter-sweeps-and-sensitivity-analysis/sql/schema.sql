DROP TABLE IF EXISTS parameter_sensitivity_registry;
DROP TABLE IF EXISTS parameter_sweep_design;

CREATE TABLE parameter_sensitivity_registry (
    sensitivity_key TEXT PRIMARY KEY,
    sensitivity_name TEXT NOT NULL,
    analytical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO parameter_sensitivity_registry VALUES
('one_at_a_time_sweep','One-at-a-time sweep','Varies one parameter while holding others fixed.','Supports intuition, debugging, and simple communication.','Can miss parameter interactions and depends on baseline values.'),
('grid_sweep','Grid sweep','Evaluates combinations of parameter values.','Reveals interactions, thresholds, and response surfaces.','Computational cost grows quickly with parameter dimension.'),
('local_sensitivity','Local sensitivity','Estimates response near a baseline parameter value.','Identifies influential parameters around a chosen scenario.','Should not be generalized beyond the local neighborhood.'),
('global_sensitivity','Global sensitivity','Assesses influence across broader ranges or distributions.','Ranks uncertain drivers and interaction effects.','Requires justified ranges, sampling design, and interpretation discipline.'),
('robustness_review','Robustness review','Checks whether conclusions persist across plausible assumptions.','Separates robust conclusions from fragile claims.','Robustness only applies to tested ranges and model structures.'),
('fragility_review','Fragility review','Identifies thresholds, reversals, and assumption-dependent conclusions.','Helps narrow claims and prioritize further data collection.','Fragility is a warning for interpretation, not automatic model rejection.');

CREATE TABLE parameter_sweep_design (
    parameter_name TEXT PRIMARY KEY,
    baseline_value REAL NOT NULL,
    minimum_value REAL NOT NULL,
    maximum_value REAL NOT NULL,
    unit_note TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO parameter_sweep_design VALUES
('growth_rate',0.35,0.18,0.55,'per time unit','Growth-rate sensitivity depends on time horizon and baseline assumptions.');
INSERT INTO parameter_sweep_design VALUES
('carrying_capacity',100.0,80.0,150.0,'state units','Capacity sensitivity should not be generalized beyond the tested range.');
INSERT INTO parameter_sweep_design VALUES
('initial_value',10.0,5.0,25.0,'state units','Initial conditions can affect transients and threshold crossing.');
