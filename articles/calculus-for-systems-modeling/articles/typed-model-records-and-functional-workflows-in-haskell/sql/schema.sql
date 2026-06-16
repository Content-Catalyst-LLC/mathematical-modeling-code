DROP TABLE IF EXISTS typed_model_record_registry;
DROP TABLE IF EXISTS typed_model_output_records;

CREATE TABLE typed_model_record_registry (
    record_key TEXT PRIMARY KEY,
    record_name TEXT NOT NULL,
    computational_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO typed_model_record_registry VALUES
('parameter_record','Parameter record','Stores named parameters, units, ranges, and source notes.','Keeps model behavior tied to explicit assumptions.','Typed parameters do not prove empirical correctness.'),
('state_record','State record','Stores model state at a time or location.','Supports reproducible trajectory and stock-flow review.','State records should preserve units and time scale.'),
('solver_record','Solver record','Stores method, time step, tolerance, horizon, and status.','Connects numerical outputs to computational configuration.','Solver settings can change model results and should not be hidden.'),
('diagnostic_record','Diagnostic record','Stores warnings, convergence status, residuals, and review flags.','Keeps reliability evidence attached to outputs.','Diagnostics should be reviewed before interpretation.'),
('assumption_record','Assumption record','Stores modeling assumptions and validity notes.','Connects outputs to scope and interpretive boundaries.','Assumptions should not be buried in prose alone.'),
('claim_boundary','Claim boundary','Stores limits on what a model output can support.','Separates computation from responsible public interpretation.','Type safety does not replace human judgment.');

CREATE TABLE typed_model_output_records (
    output_id TEXT PRIMARY KEY,
    model_use TEXT NOT NULL,
    growth_rate REAL NOT NULL,
    carrying_capacity REAL NOT NULL,
    initial_stock REAL NOT NULL,
    time_step REAL NOT NULL,
    horizon REAL NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO typed_model_output_records VALUES
('teaching_logistic_record','governance_review',0.35,100.0,10.0,0.25,20.0,'Typed records improve structural review but do not prove empirical validity.');
