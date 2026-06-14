DROP TABLE IF EXISTS calculus_concept_registry;
DROP TABLE IF EXISTS approximation_step;

CREATE TABLE calculus_concept_registry (
    concept_key TEXT PRIMARY KEY,
    concept_name TEXT NOT NULL,
    historical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_note TEXT NOT NULL
);

CREATE TABLE approximation_step (
    step_key TEXT PRIMARY KEY,
    h REAL NOT NULL CHECK (h > 0),
    interpretation TEXT NOT NULL
);

INSERT INTO calculus_concept_registry VALUES
('infinity','Infinity','Raised foundational questions about infinite division motion and accumulation.','Appears in limiting processes long-run behavior refinement and asymptotic reasoning.','Do not confuse mathematical infinity with empirical measurement capacity.'),
('infinitesimal','Infinitesimal','Supported early reasoning about vanishingly small changes and differentials.','Supports intuition for local change marginal response and sensitivity.','Use formal limit interpretation or validated infinitesimal framework when precision matters.'),
('limit','Limit','Provided a rigorous foundation for derivatives integrals and convergence.','Connects approximation refinement local rates and numerical stability.','Check whether refined approximations stabilize and remain meaningful.'),
('difference_quotient','Difference Quotient','Connects average change over finite intervals to local derivative reasoning.','Used in finite differences rate estimation and numerical derivatives.','Step size affects accuracy noise sensitivity and interpretation.');

INSERT INTO approximation_step VALUES
('h_1',1.0,'Coarse average change interval.'),
('h_0_1',0.1,'Finer local approximation interval.'),
('h_0_01',0.01,'Small interval used for convergence review.'),
('h_0_001',0.001,'Very small interval; review numerical precision.');
