-- Scientific computing for modeling workflows governance schema.

DROP TABLE IF EXISTS workflow_component_guide;
DROP TABLE IF EXISTS resource_workflow_scenario;
DROP TABLE IF EXISTS scientific_computing_workflow_register;
DROP TABLE IF EXISTS workflow_stage_type;

CREATE TABLE workflow_stage_type (
    workflow_stage TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    typical_failure TEXT NOT NULL
);

CREATE TABLE scientific_computing_workflow_register (
    record_id INTEGER PRIMARY KEY,
    record_key TEXT NOT NULL,
    workflow_stage TEXT NOT NULL,
    computational_object TEXT NOT NULL,
    modeling_role TEXT NOT NULL,
    review_question TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('active', 'review', 'revise', 'archive')),
    FOREIGN KEY (workflow_stage) REFERENCES workflow_stage_type(workflow_stage)
);

CREATE TABLE resource_workflow_scenario (
    scenario TEXT PRIMARY KEY,
    initial_stock REAL NOT NULL CHECK (initial_stock >= 0),
    growth_rate REAL NOT NULL CHECK (growth_rate >= 0),
    carrying_capacity REAL NOT NULL CHECK (carrying_capacity > 0),
    extraction REAL NOT NULL CHECK (extraction >= 0),
    shock_probability REAL NOT NULL CHECK (shock_probability >= 0 AND shock_probability <= 1),
    shock_fraction REAL NOT NULL CHECK (shock_fraction >= 0 AND shock_fraction <= 1),
    steps INTEGER NOT NULL CHECK (steps > 0),
    seed INTEGER NOT NULL
);

CREATE TABLE workflow_component_guide (
    workflow_stage TEXT PRIMARY KEY,
    meaning TEXT NOT NULL,
    example TEXT NOT NULL,
    review_question TEXT NOT NULL
);

INSERT INTO workflow_stage_type VALUES
('data_intake','Data entry and validation.','Data provenance and schema are unclear.'),
('parameter_control','Scenario and configuration management.','Parameters are buried inside scripts.'),
('model_execution','Executable model logic.','Code diverges from mathematical specification.'),
('output_generation','Tables figures reports and output files.','Outputs cannot be traced.'),
('reproducibility','Rerun capability.','Run context is not documented.'),
('validation','Technical and substantive checks.','Successful execution is confused with validation.'),
('governance','Review and accountability.','Assumptions and limits are hidden.');

INSERT INTO scientific_computing_workflow_register(record_key, workflow_stage, computational_object, modeling_role, review_question, status) VALUES
('input_schema','data_intake','resource_scenario_fields','Defines required model inputs and units','Are all required fields documented and validated?','review'),
('configuration','parameter_control','scenario_configuration','Separates run-specific values from code','Can outputs be traced to active parameters?','active'),
('simulation_engine','model_execution','resource_update_loop','Implements the model state transition rule','Does code match the mathematical specification?','review'),
('output_index','output_generation','generated_output_catalog','Lists tables figures json and logs produced by the workflow','Can outputs be traced and inspected?','active'),
('run_manifest','reproducibility','manifest_json','Records command environment seed and outputs','Can another analyst rerun the workflow?','active'),
('validation_checks','validation','workflow_smoke_and_schema_checks','Documents technical and modeling checks','Do checks support the result being claimed?','review'),
('audit_card','governance','workflow_audit_card','Summarizes checks outputs and limitations','Are assumptions and use limits visible?','review');

INSERT INTO resource_workflow_scenario VALUES
('baseline',70.0,0.18,100.0,6.0,0.05,0.10,50,20260612),
('stress',70.0,0.15,100.0,9.0,0.12,0.20,50,20260613),
('recovery_policy',70.0,0.18,100.0,5.0,0.05,0.10,50,20260614);

INSERT INTO workflow_component_guide VALUES
('data_intake','Data entry and validation','input schema','Are inputs valid?'),
('parameter_control','Scenario and configuration management','configuration file','Can parameters be traced?'),
('model_execution','Executable model logic','simulation script','Does code match the model?'),
('output_generation','Tables figures reports and files','output index','Are outputs traceable?'),
('reproducibility','Rerun capability','run manifest','Can results be reproduced?'),
('validation','Technical and substantive checks','test report','Are claims supported?'),
('governance','Review and accountability','audit card','Are assumptions visible?');
