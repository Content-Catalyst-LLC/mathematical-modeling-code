DROP TABLE IF EXISTS reproducible_linear_algebra_governance_registry;
DROP TABLE IF EXISTS reproducible_linear_algebra_audit_cases;

CREATE TABLE reproducible_linear_algebra_governance_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    workflow_role TEXT NOT NULL,
    documentation_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO reproducible_linear_algebra_governance_registry VALUES
('matrix_construction','Matrix construction','Defines how source data become matrices and vectors.','Documents row meaning column meaning value meaning units zeros missingness and transformations.','A notebook is not reproducible if the matrix cannot be reconstructed from documented inputs.'),
('notebook_execution','Notebook execution','Defines whether the notebook can run from a clean state.','Records execution order required inputs generated outputs and stale-output controls.','A notebook that depends on hidden state is not a reliable reproducible artifact.'),
('environment_control','Environment control','Defines language versions packages numerical backends and runtime settings.','Supports reruns across machines and future maintenance.','Environment capture supports computation but does not guarantee model validity.'),
('randomness_control','Randomness control','Defines random seeds generators sampling methods and nondeterminism warnings.','Supports reruns for randomized algorithms simulations and sampling workflows.','Randomness must be controlled and disclosed when it affects outputs.'),
('validation_tests','Validation tests','Defines reference cases residual checks edge cases and domain checks.','Shows whether code and model outputs are credible under review.','Reproducibility without validation can reproduce the same error repeatedly.'),
('generated_outputs','Generated outputs','Defines tables figures logs JSON files reports and manifests created by the workflow.','Connects results to commands inputs code and metadata.','Manually edited outputs weaken traceability.'),
('version_control','Version control','Defines how code documentation assumptions and outputs change over time.','Supports audit trails review rollback and collaboration.','Version control records change but does not replace interpretation review.'),
('responsible_interpretation','Responsible interpretation','Defines how assumptions uncertainty validation status and model limits are communicated.','Prevents reproducible computation from being mistaken for complete truth.','A reproducible workflow still requires judgment about what the results mean.');

CREATE TABLE reproducible_linear_algebra_audit_cases (
    workflow_name TEXT NOT NULL,
    notebook_status TEXT NOT NULL,
    documentation_status TEXT NOT NULL,
    matrix_shape TEXT NOT NULL,
    matrix_meaning TEXT NOT NULL,
    data_provenance_status TEXT NOT NULL,
    environment_status TEXT NOT NULL,
    random_seed_status TEXT NOT NULL,
    validation_status TEXT NOT NULL,
    generated_outputs_status TEXT NOT NULL,
    residual_norm REAL NOT NULL,
    relative_residual REAL NOT NULL,
    reproducibility_score INTEGER NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO reproducible_linear_algebra_audit_cases VALUES
('reproducible_linear_algebra_workflow_audit','clean_execution_required_and_documented','readme_data_dictionary_method_notes_and_governance_report_required','2x2','synthetic_reference_system_for_reproducibility_validation','synthetic_data_documented_in_workflow','runtime_metadata_recorded','not_applicable_for_deterministic_reference_case','reference_solution_and_residual_check_passed','tables_json_and_reports_written_by_workflow',0.0,0.0,100,'Reproducibility means rerunnable and reviewable not automatically valid.');
