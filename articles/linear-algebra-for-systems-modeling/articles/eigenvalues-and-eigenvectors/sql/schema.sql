CREATE TABLE IF NOT EXISTS article_status (
  slug TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  status TEXT NOT NULL,
  systems_modeling_note TEXT
);

INSERT OR REPLACE INTO article_status (slug, title, status, systems_modeling_note)
VALUES ('eigenvalues-and-eigenvectors', 'Eigenvalues and Eigenvectors', 'planned', 'A foundation for persistent directions, scaling, and structural modes.');
