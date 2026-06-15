DROP TABLE IF EXISTS separable_equation_assumption_registry;
CREATE TABLE separable_equation_assumption_registry (assumption_key TEXT PRIMARY KEY, assumption_name TEXT NOT NULL, mathematical_role TEXT NOT NULL, systems_modeling_role TEXT NOT NULL, review_warning TEXT NOT NULL);
INSERT INTO separable_equation_assumption_registry VALUES
('separability','Separability','Requires factoring the rate law into independent-variable and state-variable components.','Claims temporal and state effects can be decomposed cleanly.','Not every dynamic system has a separable structure.'),
('state_domain','State domain','Defines where division by the state-dependent factor is valid.','Protects interpretation near equilibrium and singular values.','Separating variables can hide excluded states.'),
('initial_condition','Initial condition','Selects one solution from a family of trajectories.','Anchors the scenario to a starting state.','Arbitrary starting values can mislead.'),
('parameter_values','Parameter values','Control growth, decay, capacity, loss, and adjustment.','Represent estimates or scenario choices.','Parameter uncertainty should be tested.'),
('simple_dynamic_law','Simple dynamic law','Defines mechanism of change in compact form.','Explains growth, decay, recovery, saturation, or input-loss balance.','Simplicity can hide thresholds, delays, and interactions.'),
('numerical_comparison','Numerical comparison','Compares analytical solutions with discrete solver approximations.','Supports reproducibility and solver-error review.','Solver agreement with an equation does not validate real-world fit.');
