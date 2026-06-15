DROP TABLE IF EXISTS improper_integral_assumption_registry;

CREATE TABLE improper_integral_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO improper_integral_assumption_registry VALUES
('limiting_process','Limiting process','Defines how the improper boundary is approached.','Clarifies whether the model uses an infinite horizon, singular endpoint, or both.','A reported value without a limiting process is not an auditable improper integral.'),
('convergence_evidence','Convergence evidence','Documents why the defining limit is finite.','Supports responsible interpretation of cumulative totals.','Numerical stability alone may not prove convergence.'),
('truncation_cutoff','Truncation cutoff','Records the finite cutoff used for numerical approximation.','Keeps computational approximation separate from infinite-horizon interpretation.','A cutoff can hide material tail contribution if not tested.'),
('tail_behavior','Tail behavior','Describes how the integrand behaves far from the finite starting point.','Determines long-run accumulation and convergence.','A rate that approaches zero may still diverge.'),
('model_validity_boundary','Model validity boundary','Identifies whether the mathematical limit extends beyond the credible model domain.','Prevents idealized singularities or infinite horizons from being overinterpreted.','Divergence may indicate a model-domain problem rather than a literal infinite real-world quantity.');
