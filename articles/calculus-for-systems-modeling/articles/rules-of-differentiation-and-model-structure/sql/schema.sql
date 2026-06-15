DROP TABLE IF EXISTS differentiation_rule_registry;
DROP TABLE IF EXISTS rule_review_warning;

CREATE TABLE differentiation_rule_registry (
    rule_key TEXT PRIMARY KEY,
    rule_name TEXT NOT NULL,
    formula_summary TEXT NOT NULL,
    model_structure TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

CREATE TABLE rule_review_warning (
    warning_key TEXT PRIMARY KEY,
    warning_name TEXT NOT NULL,
    interpretation TEXT NOT NULL
);

INSERT INTO differentiation_rule_registry VALUES
('sum_rule','Sum rule','D(f + g) = Df + Dg','Additive decomposition','Supports component-wise rate attribution.','Only reflects additive structure; hidden interactions require other rules.'),
('product_rule','Product rule','D(fg) = fDg + gDf','Interaction of factors','Separates local change into factor-specific contributions.','Both factors must be differentiable at the point of interpretation.'),
('quotient_rule','Quotient rule','D(f/g) = (gDf - fDg)/g^2','Ratio or normalized quantity','Explains how numerator and denominator drive ratio change.','Requires nonzero denominator and careful near-zero interpretation.'),
('chain_rule','Chain rule','D(f∘g) = (Df∘g)Dg','Nested process or transformation','Tracks how change propagates through linked mechanisms.','Every relevant link must be differentiable.'),
('implicit_differentiation','Implicit differentiation','For F(x,y)=0, dy/dx = -F_x/F_y under regularity conditions','Constraint relationship','Shows how variables co-adjust while maintaining a constraint.','Requires regularity conditions such as nonzero F_y.'),
('logarithmic_differentiation','Logarithmic differentiation','D log f = f''/f','Multiplicative or proportional structure','Supports growth-rate and elasticity interpretation.','Requires positivity and domain checks.');

INSERT INTO rule_review_warning VALUES
('causal_warning','Structural does not imply causal','A derivative decomposition identifies local pathways in the model but does not by itself prove causal interpretation.'),
('domain_warning','Domain required','Symbolic differentiation must respect the domain where the model is meaningful.'),
('denominator_warning','Near-zero denominator','Ratio derivatives can become unstable when denominators are small.'),
('composition_warning','Every link matters','A chain-rule pathway requires differentiability at every relevant link.');
