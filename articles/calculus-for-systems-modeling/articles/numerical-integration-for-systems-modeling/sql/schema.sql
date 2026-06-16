DROP TABLE IF EXISTS numerical_integration_assumption_registry;
CREATE TABLE numerical_integration_assumption_registry (
  assumption_key TEXT PRIMARY KEY,
  assumption_name TEXT NOT NULL,
  mathematical_role TEXT NOT NULL,
  systems_modeling_role TEXT NOT NULL,
  review_warning TEXT NOT NULL
);
INSERT INTO numerical_integration_assumption_registry VALUES
('integrand_definition','Integrand definition','Defines the rate density intensity or field being integrated.','Clarifies whether accumulation represents flow exposure burden energy mass risk or change.','The integrand should have clear units and system meaning.'),
('integration_rule','Integration rule','Defines how sampled values are converted into local area or total contribution.','Controls whether rectangles trapezoids Simpson-style weights or another quadrature method are used.','The rule should be documented and matched to sampling structure.'),
('spacing','Spacing','Defines time step grid width cell area or interval widths used in accumulation.','Controls how much each sampled value contributes to the total.','Irregular spacing should be handled explicitly.'),
('conservation_check','Conservation check','Compares stock change to integrated net flow.','Helps identify missing flows unit inconsistency or model structure problems.','Synthetic checks do not guarantee empirical validity.');
