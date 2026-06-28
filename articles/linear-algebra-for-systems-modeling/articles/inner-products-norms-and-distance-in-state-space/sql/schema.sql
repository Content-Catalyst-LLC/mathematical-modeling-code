CREATE TABLE IF NOT EXISTS article_status (
  slug TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  status TEXT NOT NULL,
  systems_modeling_note TEXT
);

INSERT OR REPLACE INTO article_status (slug, title, status, systems_modeling_note)
VALUES ('inner-products-norms-and-distance-in-state-space', 'Inner Products, Norms, and Distance in State Space', 'planned', 'A treatment of similarity, magnitude, distance, and measurement in vector spaces.');
