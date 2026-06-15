DROP TABLE IF EXISTS integration_by_parts_assumption_registry;

CREATE TABLE integration_by_parts_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO integration_by_parts_assumption_registry VALUES
('choice_of_parts','Choice of parts','Defines which factor is differentiated and which factor is integrated.','Determines the interpretation of direct and residual accumulation.','An algebraically valid choice may still produce weak or misleading system interpretation.'),
('boundary_term','Boundary term','The endpoint contribution [uv] from a to b.','Shows how starting and ending product states shape the decomposition.','Boundary terms depend strongly on interval choice.'),
('residual_integral','Residual integral','The complementary accumulated product-change term.','Shows how change in the other factor contributes inside the interval.','Residual terms may be unstable if derivatives are noisy.'),
('unit_consistency','Unit consistency','Direct, boundary, and residual terms should share product units.','Prevents invalid decomposition claims.','Unit mismatch can make the decomposition meaningless.'),
('decomposition_residual','Decomposition residual','Difference between direct computation and boundary-minus-residual computation.','Audits numerical consistency and data reliability.','Large residuals may indicate numerical error, derivative error, missing terms, or inconsistent data.');
