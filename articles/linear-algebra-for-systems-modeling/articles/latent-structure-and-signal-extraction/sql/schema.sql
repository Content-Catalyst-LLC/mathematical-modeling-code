CREATE TABLE IF NOT EXISTS article_status (
  slug TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  status TEXT NOT NULL,
  systems_modeling_note TEXT
);

INSERT OR REPLACE INTO article_status (slug, title, status, systems_modeling_note)
VALUES ('latent-structure-and-signal-extraction', 'Latent Structure and Signal Extraction', 'planned', 'An article on separating signal, pattern, and noise in high-dimensional systems.');
