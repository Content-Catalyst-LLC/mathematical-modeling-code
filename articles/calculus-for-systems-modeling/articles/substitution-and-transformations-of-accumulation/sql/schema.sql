DROP TABLE IF EXISTS substitution_assumption_registry;

CREATE TABLE substitution_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO substitution_assumption_registry VALUES
('original_variable','Original variable','Defines the variable over which accumulation was first expressed.','Clarifies the original scale of the modeled process.','Unclear original variables make transformed accumulation impossible to audit.'),
('transformed_variable','Transformed variable','Defines the new variable used for the change of variables.','Clarifies the new scale, clock, coordinate, or state representation.','A transformed variable without interpretation can obscure model meaning.'),
('scale_factor','Scale factor','The derivative of the transformation converts differentials between variables.','Preserves accumulated quantity across representations.','Omitting the scale factor usually changes units and accumulated totals.'),
('transformed_bounds','Transformed bounds','Original bounds must be mapped into bounds for the new variable.','Preserves interval meaning under transformation.','Keeping old bounds after changing variables mixes incompatible intervals.'),
('orientation_and_monotonicity','Orientation and monotonicity','The transformation may preserve orientation, reverse orientation, or require piecewise treatment.','Prevents path-dependent or nonmonotonic transformations from being misread.','Nonmonotonic transformations may require splitting the interval or adding state information.');
