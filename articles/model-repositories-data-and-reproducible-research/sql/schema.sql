-- Model repositories, data, and reproducible research governance schema.

DROP TABLE IF EXISTS expected_repository_artifact;
DROP TABLE IF EXISTS repository_audit_register;
DROP TABLE IF EXISTS repository_layer_type;

CREATE TABLE repository_layer_type (
    repository_layer TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    typical_failure TEXT NOT NULL
);

CREATE TABLE repository_audit_register (
    record_id INTEGER PRIMARY KEY,
    record_key TEXT NOT NULL,
    repository_layer TEXT NOT NULL,
    artifact TEXT NOT NULL,
    modeling_role TEXT NOT NULL,
    review_question TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('active', 'review', 'revise', 'archive')),
    FOREIGN KEY (repository_layer) REFERENCES repository_layer_type(repository_layer)
);

CREATE TABLE expected_repository_artifact (
    artifact TEXT PRIMARY KEY,
    path TEXT NOT NULL,
    required INTEGER NOT NULL CHECK (required IN (0, 1)),
    purpose TEXT NOT NULL
);

INSERT INTO repository_layer_type VALUES
('documentation','Project explanation, setup, use instructions, and method notes.','Users cannot understand or rerun the project.'),
('data','Raw, processed, synthetic, restricted, and metadata records.','Inputs cannot be traced or interpreted.'),
('code','Executable model and audit workflows.','Model implementation is unavailable or unclear.'),
('metadata','Title, version, citation, tags, schema, and context.','Repository cannot be cited or cataloged.'),
('reproducibility','Run commands, environments, outputs, hashes, and manifests.','Results cannot be regenerated.'),
('validation','Tests, diagnostics, and model assessment records.','Successful execution is mistaken for validation.'),
('governance','Assumptions, intended use, limitations, and review status.','Model is reused beyond scope.'),
('licensing','Rights and restrictions for code, data, and documentation.','Reuse is legally or ethically ambiguous.');

INSERT INTO repository_audit_register(record_key, repository_layer, artifact, modeling_role, review_question, status) VALUES
('readme','documentation','README.md','Explains project purpose structure setup and run commands','Can a new analyst understand and run the repository?','review'),
('metadata','metadata','article-metadata.yml','Records title slug focus keyword tags and excerpt','Is repository metadata complete and consistent?','active'),
('data_provenance','data','data_provenance_notes_and_schemas','Documents data sources transformations and constraints','Can inputs be traced to their sources?','review'),
('run_manifest','reproducibility','reproducibility_manifest.json','Records execution context and output hashes','Can outputs be regenerated and checked?','active'),
('model_card','governance','model_repository_card.json','Summarizes purpose assumptions validation and use limits','Are intended use and limits visible?','review'),
('license_note','licensing','license_and_reuse_notes','Clarifies reuse rights for code data and documentation','Are reuse rights and restrictions clear?','review'),
('validation_record','validation','test_and_diagnostic_outputs','Preserves checks that support model claims','Do validation artifacts support the claimed result?','review');

INSERT INTO expected_repository_artifact VALUES
('README','README.md',1,'Project overview and run instructions'),
('metadata','article-metadata.yml',1,'Article and repository metadata'),
('Makefile','Makefile',1,'Repeatable workflow targets'),
('Python package','python',1,'Executable model and audit code'),
('R workflow','r',0,'Independent review workflow'),
('SQL schema','sql/schema.sql',0,'Structured governance tables'),
('data folder','data',1,'Data metadata and scenario files'),
('docs folder','docs',1,'Documentation and governance notes'),
('outputs folder','outputs',1,'Generated tables figures JSON and logs'),
('schemas folder','schemas',0,'Machine-readable validation schemas'),
('canvas manifest','canvas/canvas_manifest.json',0,'Catalyst Canvas governance metadata');
