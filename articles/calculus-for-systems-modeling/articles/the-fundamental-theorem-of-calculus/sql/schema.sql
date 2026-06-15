DROP TABLE IF EXISTS fundamental_theorem_assumption_registry;

CREATE TABLE fundamental_theorem_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO fundamental_theorem_assumption_registry VALUES
('rate_state_consistency','Rate-state consistency','If Q prime equals r, accumulated r over an interval should match Q(b)-Q(a).','Checks whether a modeled rate and state trajectory reconcile.','A large residual may indicate missing flows, measurement error, sign error, or numerical error.'),
('interval_bounds','Interval bounds','The theorem relates accumulated change to endpoint difference over a specific interval.','Keeps cumulative claims tied to declared start and end points.','Changing bounds changes both the integral and endpoint comparison.'),
('baseline_state','Baseline state','Recovered state requires a starting value when using accumulated rate.','Connects accumulation to stock-flow interpretation.','A wrong baseline shifts the recovered trajectory.'),
('unit_consistency','Unit consistency','Rate units times integration-variable units should match state units.','Prevents invalid reconciliation between rates and states.','Unit mismatch can create false residuals or false agreement.'),
('numerical_tolerance','Numerical tolerance','Approximate integration may not exactly equal endpoint difference.','Supports transparent computational audit.','Tolerance should reflect grid size, method, smoothness, noise, and measurement uncertainty.');
