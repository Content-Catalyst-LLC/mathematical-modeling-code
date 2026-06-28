CREATE TABLE IF NOT EXISTS article_status (
  slug TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  status TEXT NOT NULL,
  systems_modeling_note TEXT
);

INSERT OR REPLACE INTO article_status (slug, title, status, systems_modeling_note)
VALUES ('machine-learning-and-linear-algebra', 'Machine Learning and Linear Algebra', 'planned', 'A bridge to vectors, embeddings, transformations, optimization, and model representation.');
