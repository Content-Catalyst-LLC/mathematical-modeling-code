CREATE TABLE IF NOT EXISTS article_status (
  slug TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  status TEXT NOT NULL,
  systems_modeling_note TEXT
);

INSERT OR REPLACE INTO article_status (slug, title, status, systems_modeling_note)
VALUES ('compression-noise-and-informational-tradeoffs', 'Compression, Noise, and Informational Tradeoffs', 'planned', 'A critical article on what reduction preserves and what it loses.');
