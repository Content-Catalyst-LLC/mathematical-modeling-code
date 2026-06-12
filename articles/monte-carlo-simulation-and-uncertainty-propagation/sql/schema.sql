-- Monte Carlo simulation and uncertainty propagation governance schema.

DROP TABLE IF EXISTS monte_carlo_component_guide;
DROP TABLE IF EXISTS monte_carlo_scenario;
DROP TABLE IF EXISTS monte_carlo_model_register;
DROP TABLE IF EXISTS monte_carlo_component_type;

CREATE TABLE monte_carlo_component_type (
    component_type TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    typical_failure TEXT NOT NULL
);

CREATE TABLE monte_carlo_model_register (
    record_id INTEGER PRIMARY KEY,
    record_key TEXT NOT NULL,
    component_type TEXT NOT NULL,
    uncertainty_structure TEXT NOT NULL,
    interpretation TEXT NOT NULL,
    review_question TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('active', 'review', 'revise', 'archive')),
    FOREIGN KEY (component_type) REFERENCES monte_carlo_component_type(component_type)
);

CREATE TABLE monte_carlo_scenario (
    scenario TEXT PRIMARY KEY,
    initial_stock_min REAL NOT NULL,
    initial_stock_max REAL NOT NULL,
    growth_rate_min REAL NOT NULL,
    growth_rate_max REAL NOT NULL,
    extraction_min REAL NOT NULL,
    extraction_max REAL NOT NULL,
    shock_probability_min REAL NOT NULL,
    shock_probability_max REAL NOT NULL,
    shock_fraction REAL NOT NULL,
    carrying_capacity REAL NOT NULL,
    steps INTEGER NOT NULL,
    replications INTEGER NOT NULL,
    depletion_threshold REAL NOT NULL,
    seed INTEGER NOT NULL,
    CHECK (initial_stock_min <= initial_stock_max),
    CHECK (growth_rate_min <= growth_rate_max),
    CHECK (extraction_min <= extraction_max),
    CHECK (shock_probability_min <= shock_probability_max),
    CHECK (shock_probability_min >= 0 AND shock_probability_max <= 1),
    CHECK (shock_fraction >= 0 AND shock_fraction <= 1),
    CHECK (carrying_capacity > 0),
    CHECK (steps > 0),
    CHECK (replications > 0)
);

CREATE TABLE monte_carlo_component_guide (
    component_type TEXT PRIMARY KEY,
    meaning TEXT NOT NULL,
    example TEXT NOT NULL,
    review_question TEXT NOT NULL
);

INSERT INTO monte_carlo_component_type VALUES
('input_uncertainty','Uncertain model input.','Input distributions are arbitrary or undocumented.'),
('sampling_design','Procedure for generating random draws.','Sampling design does not match uncertainty structure.'),
('random_seed_protocol','Reproducibility rule.','Seeds are not recorded.'),
('output_distribution','Distribution of model outputs.','Only averages are reported.'),
('risk_metric','Threshold-based output.','Threshold choice is unjustified.'),
('convergence_diagnostic','Replication adequacy check.','Monte Carlo estimates are unstable.'),
('sensitivity_diagnostic','Uncertainty attribution.','Drivers of risk are not identified.'),
('validation_diagnostic','Credibility check.','Sampling is mistaken for validation.');

INSERT INTO monte_carlo_model_register(record_key, component_type, uncertainty_structure, interpretation, review_question, status) VALUES
('input_distributions','input_uncertainty','uniform_ranges_for_stock_growth_extraction_and_shock_probability','Uncertain inputs are represented by bounded distributions','Are input ranges evidence-based and documented?','review'),
('sampling_protocol','sampling_design','pseudo_random_independent_draws_with_recorded_seed','Replications propagate uncertainty through the model','Are seed and replication count sufficient for reproducibility?','active'),
('threshold_metric','risk_metric','P_final_stock_less_than_or_equal_to_depletion_threshold','Risk is summarized as a depletion probability','Is the threshold appropriate for decision support?','review'),
('convergence_diagnostic','convergence_diagnostic','running_mean_and_threshold_probability_by_replication_count','Monte Carlo estimates should stabilize with more replications','Do output summaries converge adequately?','review'),
('dependence_assumption','validation_diagnostic','independent_input_sampling','Inputs are sampled independently unless otherwise specified','Is independence plausible for the model purpose?','review'),
('quantile_summary','output_distribution','p05_median_p95_final_stock','Output distributions are summarized by quantiles','Are tail summaries communicated responsibly?','active');

INSERT INTO monte_carlo_scenario VALUES
('baseline_uncertainty',65.0,75.0,0.14,0.22,5.0,8.0,0.02,0.08,0.12,100.0,50,1000,10.0,20260612),
('stress_uncertainty',60.0,75.0,0.10,0.20,7.0,11.0,0.08,0.18,0.22,100.0,50,1000,10.0,20260613);

INSERT INTO monte_carlo_component_guide VALUES
('input_uncertainty','Uncertain model input','bounded growth-rate distribution','Is distribution justified?'),
('sampling_design','Procedure for generating random draws','pseudo-random independent draws','Does design match uncertainty structure?'),
('random_seed_protocol','Reproducibility rule','recorded seed per scenario','Can results be rerun?'),
('output_distribution','Distribution of model outputs','final stock quantiles','Are quantiles and tails reported?'),
('risk_metric','Threshold-based output','P(final stock <= 10)','Is threshold meaningful?'),
('convergence_diagnostic','Replication adequacy check','running probability','Do estimates stabilize?'),
('sensitivity_diagnostic','Uncertainty attribution','input-output association','Which inputs drive risk?'),
('validation_diagnostic','Credibility check','distribution and plausibility review','Is uncertainty model credible?');
