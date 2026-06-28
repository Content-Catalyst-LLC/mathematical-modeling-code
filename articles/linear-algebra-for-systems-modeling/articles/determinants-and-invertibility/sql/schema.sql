CREATE TABLE IF NOT EXISTS article_status (
  slug TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  status TEXT NOT NULL,
  systems_modeling_note TEXT
);

INSERT OR REPLACE INTO article_status (slug, title, status, systems_modeling_note)
VALUES ('determinants-and-invertibility', 'Determinants and Invertibility', 'planned', 'An article on volume, orientation, and whether a transformation can be reversed.');
