DROP TABLE IF EXISTS row_reduction_assumption_registry;
DROP TABLE IF EXISTS row_reduction_audit_cases;

CREATE TABLE row_reduction_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO row_reduction_assumption_registry VALUES
('row_equivalence','Row equivalence','Elementary row operations preserve the solution set.','Allows constraints to be transformed without changing feasible algebraic solutions.','Equivalent algebraic systems may become harder to interpret if original equation meanings are lost.'),
('pivot_selection','Pivot selection','Chooses leading entries for elimination.','Identifies independent constraint directions and controlled variables.','Small or unstable pivots may create numerical reliability issues.'),
('rank_detection','Rank detection','Counts pivot rows or independent constraint directions.','Reveals the effective number of independent modeled constraints.','Rank depends on tolerance in numerical computation and should be interpreted carefully.'),
('consistency_check','Consistency check','Compares coefficient rank and augmented rank.','Tests whether targets or right-hand-side values conflict with modeled relationships.','Consistency does not guarantee practical feasibility or model adequacy.'),
('free_variables','Free variables','Variables without pivots remain unconstrained by independent equations.','Represent degrees of freedom flexibility missing constraints or decision variables.','Free variables should be reviewed before choosing a solution.'),
('solution_verification','Solution verification','Substitutes computed values into the original system.','Checks solver output against original equations units and constraints.','Always verify against the original system not only the row-reduced form.');

CREATE TABLE row_reduction_audit_cases (
    system_name TEXT NOT NULL,
    equation_count INTEGER NOT NULL,
    unknown_count INTEGER NOT NULL,
    pivot_columns TEXT NOT NULL,
    coefficient_rank INTEGER NOT NULL,
    augmented_rank INTEGER NOT NULL,
    consistent INTEGER NOT NULL,
    solution_behavior TEXT NOT NULL,
    tolerance REAL NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO row_reduction_audit_cases VALUES
('three_constraint_resource_balance_system',3,3,'0,1,2',3,3,1,'unique solution',0.0000000001,'Row reduction reveals algebraic structure but feasibility requires review.');
