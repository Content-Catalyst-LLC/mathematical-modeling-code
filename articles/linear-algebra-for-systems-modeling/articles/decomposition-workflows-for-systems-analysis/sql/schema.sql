CREATE TABLE IF NOT EXISTS article_status (
  slug TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  status TEXT NOT NULL,
  systems_modeling_note TEXT
);

INSERT OR REPLACE INTO article_status (slug, title, status, systems_modeling_note)
VALUES ('decomposition-workflows-for-systems-analysis', 'Decomposition Workflows for Systems Analysis', 'planned', 'A practical article on PCA, SVD, matrix factorization, exploratory decomposition, and model interpretation.');
