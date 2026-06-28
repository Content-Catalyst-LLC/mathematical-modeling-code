DROP TABLE IF EXISTS solution_space_assumption_registry;
DROP TABLE IF EXISTS solution_space_audit_cases;

CREATE TABLE solution_space_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO solution_space_assumption_registry VALUES
('variable_definition','Variable definition','Defines the unknown entries in the solution vector.','Controls what system quantities decisions flows or states are solved for.','Variables must have documented meaning units boundaries and validity conditions.'),
('constraint_definition','Constraint definition','Defines equations or inequalities restricting possible vectors.','Represents balances capacities observations budgets targets or rules.','Constraints should be classified as empirical physical institutional normative or assumed.'),
('rank_diagnostic','Rank diagnostic','Measures independent structure in the coefficient matrix.','Identifies how many independent constraints or directions the model contains.','Rank depends on matrix construction scaling numerical tolerance and data quality.'),
('nullity_diagnostic','Nullity diagnostic','Measures the dimension of the null space.','Identifies remaining degrees of freedom hidden directions or underdetermination.','Free directions may represent useful flexibility or missing information.'),
('consistency_check','Consistency check','Determines whether at least one solution satisfies all equations.','Identifies whether targets observations or constraints can coexist.','Inconsistency may reflect data error incompatible goals or unrealistic assumptions.'),
('feasible_solution_space','Feasible solution space','Restricts mathematical solutions to admissible vectors.','Connects equations to nonnegativity capacity budget probability or policy constraints.','Feasible solutions require separate review beyond algebraic consistency.');

CREATE TABLE solution_space_audit_cases (
    system_name TEXT NOT NULL,
    variable_count INTEGER NOT NULL,
    equation_count INTEGER NOT NULL,
    rank_value INTEGER NOT NULL,
    nullity_value INTEGER NOT NULL,
    likely_solution_structure TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO solution_space_audit_cases VALUES
('four_variable_three_constraint_system',4,3,3,1,'Positive-dimensional solution space if the system is consistent.','Rank and nullity describe mathematical freedom, not full feasibility.');
