DROP TABLE IF EXISTS reproducibility_governance_registry;
DROP TABLE IF EXISTS workflow_output_register;

CREATE TABLE reproducibility_governance_registry (
    workflow_key TEXT PRIMARY KEY,
    workflow_name TEXT NOT NULL,
    computational_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO reproducibility_governance_registry VALUES
('r_markdown_report','R Markdown report','Combines prose, equations, code, tables, and figures in an executable report.','Supports statistical reporting, sensitivity summaries, and analytical appendices.','Rendered reports should be regenerated from source, not manually patched.'),
('jupyter_notebook','Jupyter notebook','Supports interactive computation, visualization, and exploratory modeling.','Helps explain numerical methods, simulations, and model diagnostics step by step.','Notebook state can drift; clean reruns and exported outputs are needed.'),
('parameter_record','Parameter record','Stores parameter names, values, units, ranges, sources, and assumption notes.','Keeps model outputs tied to the configuration that produced them.','Parameter records do not prove empirical correctness.'),
('output_register','Output register','Lists generated tables, figures, reports, JSON files, and logs.','Makes artifacts traceable to source workflows.','Outputs should be regenerated from code and documented.'),
('smoke_test','Smoke test','Checks whether a workflow runs and writes expected artifacts.','Supports repository maintenance and executable scaffolding.','A smoke test does not prove mathematical validity.'),
('governance_queue','Governance queue','Collects warnings, assumptions, unresolved diagnostics, and review items.','Keeps interpretation limits visible across the workflow.','Governance queues support human review but do not replace it.');

CREATE TABLE workflow_output_register (
    artifact_name TEXT PRIMARY KEY,
    artifact_type TEXT NOT NULL,
    artifact_path TEXT NOT NULL,
    source_or_generated TEXT NOT NULL,
    review_role TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO workflow_output_register VALUES
('parameter_records','csv','data/parameter_records.csv','source','documents parameter names values units sources and ranges','Parameter records do not prove empirical correctness.');
INSERT INTO workflow_output_register VALUES
('workflow_artifacts','json','outputs/json/workflow_artifacts.json','generated','stores structured reproducibility metadata','Structured metadata must remain synchronized with generated outputs.');
INSERT INTO workflow_output_register VALUES
('reproducibility_audit','markdown','outputs/reports/reproducibility_audit.md','generated','summarizes run status artifacts and warnings','Audit summaries support review but do not replace inspection.');
