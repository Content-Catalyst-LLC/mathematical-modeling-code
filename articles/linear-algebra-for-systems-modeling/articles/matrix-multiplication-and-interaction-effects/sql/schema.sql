DROP TABLE IF EXISTS matrix_product_assumption_registry;
DROP TABLE IF EXISTS matrix_product_interaction_audit_cases;
CREATE TABLE matrix_product_assumption_registry (assumption_key TEXT PRIMARY KEY, assumption_name TEXT NOT NULL, mathematical_role TEXT NOT NULL, systems_modeling_role TEXT NOT NULL, review_warning TEXT NOT NULL);
INSERT INTO matrix_product_assumption_registry VALUES
('dimension_compatibility','Dimension compatibility','The inner dimensions of two matrices must match for multiplication.','The output layer of the first transformation must feed meaningfully into the input layer of the second.','Matching dimensions do not guarantee matching units or concepts.'),
('row_column_rule','Row-column rule','Each product entry is a dot product of one row and one column.','Each entry aggregates pathway contributions through intermediate components.','Intermediate indexes should have documented system meaning.'),
('composition_order','Composition order','In AB B acts first and A acts second.','Transformation sequence matters for system interpretation.','Reversing order can change meaning or be impossible.'),
('noncommutativity','Noncommutativity','Matrix multiplication usually satisfies AB not equal BA.','Process order pipeline order and pathway direction matter.','Do not swap products unless the transformation meaning permits it.'),
('indirect_effect','Indirect effect','Product entries sum contributions through intermediate indexes.','Captures mediated or multi-step system relationships.','Indirect effects require substantive validation.'),
('repeated_product','Repeated product','Matrix powers represent repeated application of a transformation.','Supports pathway transition and dynamic-system analysis.','Long-run interpretation requires stability and model-scope review.');
CREATE TABLE matrix_product_interaction_audit_cases (system_name TEXT NOT NULL, left_shape TEXT NOT NULL, right_shape TEXT NOT NULL, product_shape TEXT NOT NULL, product_matrix TEXT NOT NULL, reverse_product_available INTEGER NOT NULL, warning TEXT NOT NULL);
INSERT INTO matrix_product_interaction_audit_cases VALUES ('two_stage_demand_to_stress_interaction','2x3','3x2','2x2','1.040000,0.560000;0.585000,0.940000',1,'Matrix product interpretation requires order intermediate-layer unit and pathway review.');
