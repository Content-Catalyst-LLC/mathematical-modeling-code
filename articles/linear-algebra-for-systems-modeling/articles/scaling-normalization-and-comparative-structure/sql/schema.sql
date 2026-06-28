CREATE TABLE IF NOT EXISTS article_status (
  slug TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  status TEXT NOT NULL,
  systems_modeling_note TEXT
);

INSERT OR REPLACE INTO article_status (slug, title, status, systems_modeling_note)
VALUES ('scaling-normalization-and-comparative-structure', 'Scaling, Normalization, and Comparative Structure', 'planned', 'A treatment of unit differences, scale effects, and comparability.');
