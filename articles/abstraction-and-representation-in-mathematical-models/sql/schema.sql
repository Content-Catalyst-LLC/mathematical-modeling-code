-- Representation governance schema for "Abstraction and Representation in Mathematical Models."

DROP TABLE IF EXISTS representation_review;
DROP TABLE IF EXISTS scenario_parameter;
DROP TABLE IF EXISTS representation_choice;
DROP TABLE IF EXISTS representation_form;
DROP TABLE IF EXISTS target_system;

CREATE TABLE target_system (
    target_id INTEGER PRIMARY KEY,
    article_slug TEXT NOT NULL,
    target_name TEXT NOT NULL,
    target_description TEXT NOT NULL,
    intended_use TEXT NOT NULL
);

CREATE TABLE representation_form (
    form_id INTEGER PRIMARY KEY,
    representation_form TEXT NOT NULL,
    emphasizes TEXT NOT NULL,
    useful_for TEXT NOT NULL,
    limitation TEXT NOT NULL
);

CREATE TABLE representation_choice (
    choice_id INTEGER PRIMARY KEY,
    target_feature TEXT NOT NULL,
    abstraction TEXT NOT NULL,
    formal_representation TEXT NOT NULL,
    preserved_structure TEXT NOT NULL,
    omitted_detail TEXT NOT NULL,
    review_question TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('active', 'review', 'revise', 'archive'))
);

CREATE TABLE scenario_parameter (
    scenario TEXT PRIMARY KEY,
    initial_stock REAL NOT NULL CHECK (initial_stock >= 0),
    capacity REAL NOT NULL CHECK (capacity > 0),
    inflow REAL NOT NULL CHECK (inflow >= 0),
    demand REAL NOT NULL CHECK (demand >= 0),
    loss_rate REAL NOT NULL CHECK (loss_rate >= 0),
    periods INTEGER NOT NULL CHECK (periods > 0),
    description TEXT
);

CREATE TABLE representation_review (
    review_id INTEGER PRIMARY KEY,
    choice_id INTEGER NOT NULL,
    review_status TEXT NOT NULL CHECK (review_status IN ('pass', 'review', 'revise')),
    reviewer_note TEXT NOT NULL,
    FOREIGN KEY (choice_id) REFERENCES representation_choice(choice_id)
);

INSERT INTO target_system(article_slug, target_name, target_description, intended_use) VALUES
('abstraction-and-representation-in-mathematical-models', 'Resource system', 'A resource stock represented by inflow, demand, losses, and capacity.', 'Demonstrate abstraction and representation choices.');

INSERT INTO representation_form(representation_form, emphasizes, useful_for, limitation) VALUES
('Equation', 'Formal relationships', 'Closed-form reasoning and compact structure', 'May hide assumptions behind notation'),
('Recurrence relation', 'Stepwise change', 'Discrete-time simulation and update rules', 'Time-step choice can shape behavior'),
('Graph', 'Relationships among entities', 'Connectivity paths dependencies and flow', 'May hide internal node dynamics'),
('Probability model', 'Uncertainty and inference', 'Risk prediction measurement error and variation', 'Distributional assumptions may dominate'),
('Optimization model', 'Objectives and constraints', 'Resource allocation design and scheduling', 'Objective may omit values that matter'),
('Simulation', 'Executable process', 'Complex behavior and scenarios', 'Can be hard to validate and interpret');

INSERT INTO representation_choice(target_feature, abstraction, formal_representation, preserved_structure, omitted_detail, review_question, status) VALUES
('Stored resource', 'Aggregate stock', 'S_t', 'Accumulation and depletion over time', 'Spatial distribution quality ownership and access', 'Does aggregate storage answer the intended question?', 'active'),
('Resource additions', 'External inflow', 'I_t', 'Input to stock-flow balance', 'Seasonality stochastic hydrology upstream governance', 'Should inflow be stochastic or scenario-based?', 'review'),
('Resource use', 'Demand term', 'D_t', 'Outflow due to use', 'Heterogeneous users conservation behavior price response', 'Does demand need subgroup structure?', 'review'),
('Physical limit', 'Capacity constraint', '0 <= S_t <= K', 'Upper and lower feasibility limits', 'Operating rules emergency reserves safety margins', 'Is physical capacity the same as usable capacity?', 'review');

INSERT INTO scenario_parameter VALUES
('aggregate_baseline',80,100,8,6,0.015,60,'Reference aggregate stock-flow representation'),
('low_inflow',80,100,5,6,0.015,60,'Lower inflow scenario'),
('higher_losses',80,100,8,6,0.035,60,'Higher loss-rate scenario'),
('lower_capacity',70,75,8,6,0.015,60,'Lower capacity representation');
