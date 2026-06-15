DROP TABLE IF EXISTS chain_rule_assumption_registry;

CREATE TABLE chain_rule_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO chain_rule_assumption_registry VALUES
('domain_compatibility','Domain compatibility','The image of the inner function must lie in the domain of the outer function.','Ensures that the composite pathway is meaningful.','A formal composition can fail if intermediate values leave the valid domain.'),
('differentiable_links','Differentiable links','Every link in the pathway must be differentiable at the relevant point.','Supports local sensitivity propagation through the pathway.','Thresholds, clipping, discontinuities, and branches can break differentiability.'),
('pathway_interpretation','Pathway interpretation','The total derivative is a product or composition of local derivative maps.','Allows analysts to identify amplification, damping, and sign reversal along the pathway.','A pathway derivative is not automatically causal proof.'),
('local_validity','Local validity','A chain-rule derivative is evaluated at a specific operating point.','Prevents local sensitivity from being overstated as a global relationship.','Composite sensitivities can change across regimes, thresholds, and boundaries.'),
('implementation_warning','Implementation warning','Automatic differentiation applies chain-rule logic to implemented code.','Supports reproducible computational derivatives.','The derivative of code is not automatically the derivative of the real-world system.');
