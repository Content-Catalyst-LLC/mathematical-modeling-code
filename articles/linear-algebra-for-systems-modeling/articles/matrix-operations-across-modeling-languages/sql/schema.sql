CREATE TABLE IF NOT EXISTS article_status (
  slug TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  status TEXT NOT NULL,
  systems_modeling_note TEXT
);

INSERT OR REPLACE INTO article_status (slug, title, status, systems_modeling_note)
VALUES ('matrix-operations-across-modeling-languages', 'Matrix Operations Across Modeling Languages', 'planned', 'A practical article on implementing core matrix workflows across the companion code stack.');
