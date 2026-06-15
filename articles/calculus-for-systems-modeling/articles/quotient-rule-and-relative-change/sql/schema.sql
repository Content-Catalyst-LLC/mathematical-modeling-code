DROP TABLE IF EXISTS quotient_rule_assumption_registry;

CREATE TABLE quotient_rule_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO quotient_rule_assumption_registry VALUES
('nonzero_denominator','Nonzero denominator','The quotient rule requires g(x) != 0.','Ensures the ratio and derivative are defined.','Near-zero denominators can create numerical and interpretive instability.'),
('numerator_effect','Numerator effect','The term f''(x)/g(x) isolates numerator-driven local change.','Shows how the ratio changes because the numerator changes.','Numerator improvement can be offset by denominator growth.'),
('denominator_effect','Denominator effect','The term -f(x)g''(x)/g(x)^2 isolates denominator-driven local change.','Shows how normalization changes the indicator.','Denominator change can dominate the ratio derivative.'),
('relative_rate_identity','Relative-rate identity','For positive f and g R''/R = f''/f - g''/g.','Explains ratio change through competing proportional rates.','Requires positivity and meaningful proportional interpretation.'),
('indicator_validity','Indicator validity','A quotient is mathematically valid only where defined.','A ratio is substantively useful only when the denominator is meaningful.','A ratio can be formal but poorly motivated as a systems indicator.');
