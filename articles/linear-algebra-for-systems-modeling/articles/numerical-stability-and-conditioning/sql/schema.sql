CREATE TABLE IF NOT EXISTS article_status (
  slug TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  status TEXT NOT NULL,
  systems_modeling_note TEXT
);

INSERT OR REPLACE INTO article_status (slug, title, status, systems_modeling_note)
VALUES ('numerical-stability-and-conditioning', 'Numerical Stability and Conditioning', 'planned', 'A treatment of ill-conditioning, precision, scaling, and computational reliability.');
