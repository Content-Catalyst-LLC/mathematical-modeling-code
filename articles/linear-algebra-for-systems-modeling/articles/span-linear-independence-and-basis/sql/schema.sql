CREATE TABLE IF NOT EXISTS article_status (
  slug TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  status TEXT NOT NULL,
  systems_modeling_note TEXT
);

INSERT OR REPLACE INTO article_status (slug, title, status, systems_modeling_note)
VALUES ('span-linear-independence-and-basis', 'Span, Linear Independence, and Basis', 'planned', 'A treatment of how systems can be generated, represented, and simplified through basis structure.');
