DROP TABLE IF EXISTS antiderivative_recovery_assumption_registry;

CREATE TABLE antiderivative_recovery_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO antiderivative_recovery_assumption_registry VALUES
('rate_definition','Rate definition','The antiderivative recovers accumulation from a specified rate function.','Clarifies what flow or marginal quantity is being accumulated.','If the rate omits important inflows or outflows, the recovered quantity is wrong.'),
('initial_condition','Initial condition','The constant of integration is fixed by a baseline value.','Selects one recovered state trajectory from the family of possible antiderivatives.','Uncertain baselines shift the entire recovered trajectory.'),
('unit_consistency','Unit consistency','Accumulating a rate over its variable should recover the intended quantity unit.','Prevents invalid flow-to-stock or marginal-to-total conversions.','Unit mismatch can invalidate the accumulation.'),
('time_step_method','Time step and method','Numerical antiderivatives depend on the accumulation rule and grid spacing.','Supports reproducible recovery from discrete data.','Coarse, irregular, or noisy data can distort recovered accumulation.'),
('domain_interval','Domain interval','Recovery is valid only over the interval where the rate model is valid.','Prevents extrapolating accumulated quantities beyond supported conditions.','Accumulation across unsupported intervals can create false cumulative claims.');
