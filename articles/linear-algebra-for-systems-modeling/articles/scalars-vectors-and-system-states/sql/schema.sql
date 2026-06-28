CREATE TABLE IF NOT EXISTS article_status (
  slug TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  status TEXT NOT NULL,
  systems_modeling_note TEXT
);

INSERT OR REPLACE INTO article_status (slug, title, status, systems_modeling_note)
VALUES ('scalars-vectors-and-system-states', 'Scalars, Vectors, and System States', 'planned', 'A foundation for understanding how multiple quantities form a state representation.');
