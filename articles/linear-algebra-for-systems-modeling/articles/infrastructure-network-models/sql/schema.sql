CREATE TABLE IF NOT EXISTS article_status (
  slug TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  status TEXT NOT NULL,
  systems_modeling_note TEXT
);

INSERT OR REPLACE INTO article_status (slug, title, status, systems_modeling_note)
VALUES ('infrastructure-network-models', 'Infrastructure Network Models', 'planned', 'An applied article on roads, energy systems, water systems, logistics, and interdependence.');
