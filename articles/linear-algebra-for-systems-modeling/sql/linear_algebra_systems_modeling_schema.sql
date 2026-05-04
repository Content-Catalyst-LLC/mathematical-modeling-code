-- Linear Algebra for Systems Modeling schema
-- Stores matrix model metadata, vectors, matrices, outputs, and assumptions.

CREATE TABLE IF NOT EXISTS linear_models (
    model_id INTEGER PRIMARY KEY,
    model_name TEXT NOT NULL,
    model_family TEXT NOT NULL,
    purpose TEXT NOT NULL,
    interpretation_note TEXT
);

CREATE TABLE IF NOT EXISTS vectors (
    vector_id INTEGER PRIMARY KEY,
    model_id INTEGER NOT NULL,
    vector_name TEXT NOT NULL,
    component_name TEXT NOT NULL,
    component_index INTEGER NOT NULL,
    component_value REAL NOT NULL,
    unit TEXT,
    FOREIGN KEY (model_id) REFERENCES linear_models(model_id)
);

CREATE TABLE IF NOT EXISTS matrices (
    matrix_id INTEGER PRIMARY KEY,
    model_id INTEGER NOT NULL,
    matrix_name TEXT NOT NULL,
    matrix_role TEXT NOT NULL,
    interpretation_note TEXT,
    FOREIGN KEY (model_id) REFERENCES linear_models(model_id)
);

CREATE TABLE IF NOT EXISTS matrix_entries (
    entry_id INTEGER PRIMARY KEY,
    matrix_id INTEGER NOT NULL,
    row_label TEXT NOT NULL,
    column_label TEXT NOT NULL,
    row_index INTEGER NOT NULL,
    column_index INTEGER NOT NULL,
    entry_value REAL NOT NULL,
    FOREIGN KEY (matrix_id) REFERENCES matrices(matrix_id)
);

CREATE TABLE IF NOT EXISTS linear_model_outputs (
    output_id INTEGER PRIMARY KEY,
    model_id INTEGER NOT NULL,
    output_name TEXT NOT NULL,
    output_value REAL,
    interpretation_note TEXT,
    FOREIGN KEY (model_id) REFERENCES linear_models(model_id)
);

CREATE TABLE IF NOT EXISTS linear_algebra_assumptions (
    assumption_id INTEGER PRIMARY KEY,
    model_id INTEGER NOT NULL,
    assumption_text TEXT NOT NULL,
    confidence REAL,
    impact_if_wrong REAL,
    testing_method TEXT,
    FOREIGN KEY (model_id) REFERENCES linear_models(model_id)
);

INSERT INTO linear_models
(model_id, model_name, model_family, purpose, interpretation_note)
VALUES
(1, 'State Transition Teaching Model', 'matrix transition model', 'Represent repeated transformation of a system state vector.', 'Educational example for transition matrices and eigenstructure.'),
(2, 'Network Adjacency Teaching Model', 'network matrix model', 'Represent relational structure through weighted adjacency.', 'Educational example for infrastructure and systems networks.'),
(3, 'SVD Dimensionality Reduction Model', 'matrix decomposition model', 'Explore latent structure in high-dimensional observations.', 'Educational example for SVD and PCA-style workflows.');
