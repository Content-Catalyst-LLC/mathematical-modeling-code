CREATE TABLE IF NOT EXISTS product_rule_model_run (
  run_id INTEGER PRIMARY KEY,
  run_name TEXT NOT NULL,
  purpose TEXT NOT NULL,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS factor_observation (
  observation_id INTEGER PRIMARY KEY,
  run_id INTEGER NOT NULL,
  time_value REAL NOT NULL,
  factor_a REAL NOT NULL,
  factor_b REAL NOT NULL,
  product_y REAL GENERATED ALWAYS AS (factor_a * factor_b) VIRTUAL,
  FOREIGN KEY (run_id) REFERENCES product_rule_model_run(run_id)
);

CREATE TABLE IF NOT EXISTS product_rule_decomposition (
  decomposition_id INTEGER PRIMARY KEY,
  run_id INTEGER NOT NULL,
  time_value REAL NOT NULL,
  a_prime REAL NOT NULL,
  b_prime REAL NOT NULL,
  direct_y_prime REAL NOT NULL,
  contribution_from_a REAL NOT NULL,
  contribution_from_b REAL NOT NULL,
  product_rule_y_prime REAL NOT NULL,
  residual REAL NOT NULL,
  FOREIGN KEY (run_id) REFERENCES product_rule_model_run(run_id)
);
