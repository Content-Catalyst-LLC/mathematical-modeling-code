CREATE TABLE IF NOT EXISTS article_status (
  slug TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  status TEXT NOT NULL,
  systems_modeling_note TEXT
);

INSERT OR REPLACE INTO article_status (slug, title, status, systems_modeling_note)
VALUES ('visualization-of-vectors-transformations-and-state-spaces', 'Visualization of Vectors, Transformations, and State Spaces', 'planned', 'A workflow article on making linear structure visible.');
