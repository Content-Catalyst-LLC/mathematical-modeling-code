DROP TABLE IF EXISTS linear_system_assumption_registry;
DROP TABLE IF EXISTS linear_system_audit_cases;

CREATE TABLE linear_system_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO linear_system_assumption_registry VALUES
('coefficient_matrix','Coefficient matrix','Stores coefficients of unknown variables in each equation.','Defines how modeled variables contribute to constraints observations or balances.','Coefficients must have documented units source and interpretation.'),
('unknown_vector','Unknown vector','Stores variables to be solved for.','Represents allocations flows parameters outputs or system states.','Algebraic values may require practical constraints such as nonnegativity or capacity limits.'),
('right_hand_side','Right-hand-side vector','Stores constants observations or targets.','Represents demand budget total observed value or required balance.','Targets may be uncertain contested infeasible or measured with error.'),
('consistency','Consistency','Indicates whether at least one solution exists.','Shows whether modeled constraints can be satisfied together.','Consistency does not prove real-world feasibility or model adequacy.'),
('rank_condition','Rank condition','Compares coefficient rank and augmented rank.','Reveals whether equations are independent redundant or contradictory.','Rank should be interpreted alongside equation meaning and data quality.'),
('solution_behavior','Solution behavior','Classifies the system as having no solution one solution or infinitely many solutions.','Helps identify conflict determinacy or remaining degrees of freedom.','A unique solution is conditional on the modeled assumptions and should not be equated with certainty.');

CREATE TABLE linear_system_audit_cases (
    system_name TEXT NOT NULL,
    equation_count INTEGER NOT NULL,
    unknown_count INTEGER NOT NULL,
    coefficient_rank INTEGER NOT NULL,
    augmented_rank INTEGER NOT NULL,
    consistent INTEGER NOT NULL,
    solution_behavior TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO linear_system_audit_cases VALUES
('three_constraint_resource_balance_system',3,3,3,3,1,'unique solution','Algebraic consistency does not guarantee practical feasibility.');
