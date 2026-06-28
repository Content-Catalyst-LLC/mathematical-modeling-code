CREATE TABLE IF NOT EXISTS article_status (
  slug TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  status TEXT NOT NULL,
  systems_modeling_note TEXT
);

INSERT OR REPLACE INTO article_status (slug, title, status, systems_modeling_note)
VALUES ('sparse-matrices-and-computational-efficiency', 'Sparse Matrices and Computational Efficiency', 'planned', 'A computational article on large systems with mostly empty structure.');
