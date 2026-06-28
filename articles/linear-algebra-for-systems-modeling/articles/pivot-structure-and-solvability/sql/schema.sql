DROP TABLE IF EXISTS pivot_structure_assumption_registry;
DROP TABLE IF EXISTS pivot_structure_audit_cases;

CREATE TABLE pivot_structure_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO pivot_structure_assumption_registry VALUES
('pivot_position','Pivot position','Marks a leading nonzero entry in echelon or reduced echelon form.','Identifies independent structure in the modeled constraint system.','Pivot meaning should be connected back to original rows and columns.'),
('pivot_column','Pivot column','Indicates a variable column controlled by independent constraints.','Shows which unknowns are determined or basic under the model structure.','A pivot variable is determined algebraically not necessarily valid practically.'),
('free_column','Free column','Indicates a variable column without a pivot.','Represents remaining degrees of freedom flexibility or under-specification.','Free variables require interpretation before choosing a solution.'),
('rank_count','Rank count','Counts pivot positions in the coefficient matrix.','Measures the effective number of independent constraint directions.','Rank depends on numerical tolerance in floating-point workflows.'),
('augmented_pivot','Augmented-column pivot','Indicates a contradiction in the augmented system.','Reveals incompatible targets or constraints.','Inconsistency may signal data error impossible targets or omitted variables.'),
('solvability_condition','Solvability condition','A system is solvable when rank(A) equals rank([A|b]).','Shows whether targets are reachable under modeled relationships.','Algebraic solvability does not guarantee feasibility legitimacy or adequacy.');

CREATE TABLE pivot_structure_audit_cases (
    system_name TEXT NOT NULL,
    equation_count INTEGER NOT NULL,
    unknown_count INTEGER NOT NULL,
    pivot_columns TEXT NOT NULL,
    free_columns TEXT NOT NULL,
    coefficient_rank INTEGER NOT NULL,
    augmented_rank INTEGER NOT NULL,
    consistent INTEGER NOT NULL,
    solution_behavior TEXT NOT NULL,
    tolerance REAL NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO pivot_structure_audit_cases VALUES
('three_constraint_resource_balance_system',3,3,'0,1,2','none',3,3,1,'unique solution',0.0000000001,'Pivot structure reveals algebraic solvability but feasibility requires review.');
