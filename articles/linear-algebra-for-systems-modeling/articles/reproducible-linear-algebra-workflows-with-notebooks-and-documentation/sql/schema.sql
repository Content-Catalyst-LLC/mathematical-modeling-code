CREATE TABLE IF NOT EXISTS article_status (
  slug TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  status TEXT NOT NULL,
  systems_modeling_note TEXT
);

INSERT OR REPLACE INTO article_status (slug, title, status, systems_modeling_note)
VALUES ('reproducible-linear-algebra-workflows-with-notebooks-and-documentation', 'Reproducible Linear Algebra Workflows with Notebooks and Documentation', 'planned', 'A workflow article on documentation, code, outputs, metadata, and reproducibility.');
