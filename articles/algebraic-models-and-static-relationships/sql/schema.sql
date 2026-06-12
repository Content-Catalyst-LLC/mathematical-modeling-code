-- Algebraic models and static relationships governance schema.

DROP TABLE IF EXISTS static_relationship_guide;
DROP TABLE IF EXISTS static_allocation_scenario;
DROP TABLE IF EXISTS algebraic_relationship_register;
DROP TABLE IF EXISTS relationship_type;

CREATE TABLE relationship_type (
    relationship_type TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    typical_failure TEXT NOT NULL
);

CREATE TABLE algebraic_relationship_register (
    relationship_id INTEGER PRIMARY KEY,
    relationship_key TEXT NOT NULL,
    relationship_type TEXT NOT NULL,
    expression TEXT NOT NULL,
    interpretation TEXT NOT NULL,
    domain_or_constraint TEXT NOT NULL,
    review_question TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('active', 'review', 'revise', 'archive')),
    FOREIGN KEY (relationship_type) REFERENCES relationship_type(relationship_type)
);

CREATE TABLE static_allocation_scenario (
    scenario TEXT PRIMARY KEY,
    budget REAL NOT NULL CHECK (budget > 0),
    cost_a REAL NOT NULL CHECK (cost_a > 0),
    cost_b REAL NOT NULL CHECK (cost_b > 0),
    benefit_a REAL NOT NULL CHECK (benefit_a >= 0),
    benefit_b REAL NOT NULL CHECK (benefit_b >= 0),
    allocation_a REAL NOT NULL CHECK (allocation_a >= 0),
    allocation_b REAL NOT NULL CHECK (allocation_b >= 0),
    capacity_a REAL NOT NULL CHECK (capacity_a >= 0),
    capacity_b REAL NOT NULL CHECK (capacity_b >= 0),
    description TEXT
);

CREATE TABLE static_relationship_guide (
    relationship_type TEXT PRIMARY KEY,
    meaning TEXT NOT NULL,
    example TEXT NOT NULL,
    review_question TEXT NOT NULL
);

INSERT INTO relationship_type VALUES
('identity','Definition that should hold by construction.','Categories are incomplete or units are inconsistent.'),
('inequality','Constraint or bound defining feasibility.','Constraint source or enforcement is hidden.'),
('objective','Quantity being optimized or scored.','Value judgments are hidden in algebra.'),
('bounds','Lower and upper limits.','Bounds are assumed but presented as natural.'),
('ratio','Quantity divided by denominator.','Denominator effects are hidden.'),
('linear','Constant marginal effect relationship.','Linearity is assumed without evidence.'),
('nonlinear','Changing marginal effect relationship.','Form is chosen without mechanism or validation.');

INSERT INTO algebraic_relationship_register(relationship_key, relationship_type, expression, interpretation, domain_or_constraint, review_question, status) VALUES
('total_cost','identity','C = c_a*x_a + c_b*x_b','Total cost is the sum of option-specific costs.','x_a >= 0; x_b >= 0','Are costs complete and expressed in comparable units?','active'),
('budget_constraint','inequality','c_a*x_a + c_b*x_b <= B','Total modeled cost must not exceed budget.','B > 0','Is the budget a hard constraint or a policy assumption?','review'),
('benefit_objective','objective','V = b_a*x_a + b_b*x_b','Total modeled benefit is additive across allocations.','benefit units must be comparable','Does additive benefit omit equity risk or implementation limits?','review'),
('capacity_bounds','bounds','0 <= x_i <= K_i','Each allocation is bounded by option-specific capacity.','K_i >= 0','Are capacity bounds measured assumed or policy-defined?','review'),
('benefit_per_cost','ratio','r = V / C','Benefit per unit cost.','C > 0','Is the denominator stable and clearly interpreted?','review');

INSERT INTO static_allocation_scenario VALUES
('balanced_feasible',100,4,5,8,11,10,8,20,15,'Feasible balanced allocation'),
('budget_stress',80,4,5,8,11,12,8,20,15,'Scenario close to or beyond budget constraint'),
('capacity_stress',120,4,5,8,11,25,5,20,15,'Scenario violating capacity on option A'),
('high_benefit_b',100,4,5,8,14,8,10,20,15,'Scenario with higher modeled benefit for option B'),
('low_budget_high_benefit',70,4,5,9,15,8,8,20,15,'High benefit but budget-constrained scenario');

INSERT INTO static_relationship_guide VALUES
('identity','Definition that should hold by construction','total cost equals fixed plus variable cost','Are all components included and compatible?'),
('linear','Constant marginal effect','y = beta0 + beta1*x','Is constant marginal effect plausible?'),
('nonlinear','Changing marginal effect','y = a*x^b','Is the shape justified by mechanism or evidence?'),
('ratio','Comparison by denominator','cost per person','Is the denominator meaningful and stable?'),
('constraint','Feasibility or limit','c*x <= B','What is the source of the limit?'),
('objective','Quantity optimized or scored','max benefit','What values are embedded in the objective?'),
('equilibrium','Static balance condition','supply equals demand','Does the model omit adjustment path?');
